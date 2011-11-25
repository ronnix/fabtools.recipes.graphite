Description
===========

`Fabric <http://fabfile.org/>`_ task to install `graphite <http://graphite.wikidot.com/>`_, using `fabtools <http://github.com/ronnix/fabtools>`_.

How to use
==========

Import the task in your project's ``fabfile.py`` to make it available::

    from fabtools.recipes.graphite import install_graphite

Then you can call it from the ``fab`` command::

    fab install_graphite
