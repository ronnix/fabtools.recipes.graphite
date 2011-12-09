"""
Fabtools recipe to install graphite

http://graphite.wikidot.com/
"""
import os.path

from fabric.api import *
import fabtools
from fabtools.python import virtualenv
from fabtools.files import is_file
from fabtools import require


# Default data retention policy:
# - 10 sec precision for 6 hours
# - 1 min precision for 1 week
# - 10 min precision for 5 years
STORAGE_SCHEMA = """\
[stats]
priority = 110
pattern = .*
retentions = 10:2160,60:10080,600:262974
"""


@task
def install_graphite(target_dir='/opt/graphite', local_port=6000,
                     server_name='graphite', port=80):
    """
    Install graphite
    """
    require.directory(target_dir, owner=env.user, use_sudo=True)
    require.python.virtualenv(target_dir)

    with virtualenv(target_dir):

        # Required Python packages
        require.python.packages([
            'whisper',
            'carbon',
            'graphite-web',
            'django',
            'django-tagging',
            'gunicorn',
            'simplejson',
        ], virtualenv=target_dir)

        # Require a recent libcairo
        require.deb.ppa('ppa:xorg-edgers/ppa')
        require.deb.package('libcairo2-dev')

        # Require pycairo (which doesn't follow standard packaging practices)
        if not fabtools.python.is_installed('pycairo'):
            require.file(url='http://cairographics.org/releases/py2cairo-1.10.0.tar.bz2')
            run('tar xjf py2cairo-1.10.0.tar.bz2')
            with cd('py2cairo-1.10.0'):
                run('python waf configure --prefix="%s"' % target_dir)
                run('python waf build')
                run('python waf install')

        # Carbon config file
        with cd('conf'):
            if not is_file('carbon.conf'):
                run('cp carbon.conf.example carbon.conf')
            require.file('storage-schemas.conf', contents=STORAGE_SCHEMA)

        # Web app local settings
        require.file('webapp/graphite/local_settings.py', contents='')

        # Initialize DB
        if not is_file('webapp/graphite/storage/graphite.db'):
            with cd('webapp/graphite'):
                run('python manage.py syncdb --noinput')

    # Run the Carbon daemon
    server = os.path.join(target_dir, 'bin', 'carbon-cache.py')
    require.supervisor.process('carbon',
        command='%s --debug start' % server,
        directory=target_dir,
        user=env.user
        )

    # Run the Django web app
    require.supervisor.process('graphite',
        command='%s -b 127.0.0.1:%d "%s"' % (
            os.path.join(target_dir, 'bin', 'gunicorn_django'),
            int(local_port),
            os.path.join(target_dir, 'webapp', 'graphite', 'settings.py')),
        directory=os.path.join(target_dir, 'webapp', 'graphite'),
        user=env.user
        )

    # Configure web server
    require.nginx.server()
    require.nginx.proxied_site(server_name, port=port,
        docroot=os.path.join(target_dir, 'webapp', 'content'),
        proxy_url='http://127.0.0.1:%d' % int(local_port)
        )
