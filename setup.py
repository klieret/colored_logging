#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='colorlog',
      description='Color for the python3 logging module',
      author='klieret',
      author_email='klieret@users.noreply.github.com',
      maintainer='klieret',
      maintainer_email'klieret@users.noreply.github.com',
      url='https://github.com/klieret/python-colorlog',
      packages=['colorlog'],
      install_requires=['typing'],
      license='GNU Lesser General Public License v3.0',
      classifiers = [
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        ]
      )

