from setuptools import setup, find_packages
import os

version = '0.1'

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='fabtools.recipes.graphite',
      version=version,
      description="Fabric task to install graphite",
      long_description=long_description,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Topic :: System :: Systems Administration",
        ],
      keywords='',
      author='Ronan Amicel',
      author_email='ronan.amicel@gmail.com',
      url='http://github.com/ronnix/fabtools.recipes.graphite',
      license='BSD',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['fabtools', 'fabtools.recipes'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'fabtools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
