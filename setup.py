#!/usr/bin/env python

from setuptools import setup

setup(
    name='confspec',
    version='1.1',
    description='Configuration Specification Manager',
    author='Carlos Jenkins',
    author_email='carlos@jenkins.co.cr',
    url='http://confspec.readthedocs.org/',
    packages=['confspec'],
    package_dir={'': 'lib'},
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
    ],
    test_suite='test',
    setup_requires=[
        'flake8'
    ]
)
