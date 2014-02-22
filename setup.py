#!/usr/bin/env python

from distutils.core import setup

setup(
    name='confspec',
    version='1.0',
    description='Configuration Specification Manager',
    author='Carlos Jenkins',
    author_email='carlos@jenkins.co.cr',
    url='http://confspec.readthedocs.org/',
    packages=['confspec'],
    package_dir={'': 'lib'},
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
    ],
)

