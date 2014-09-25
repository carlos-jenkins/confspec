#!/usr/bin/env python

from setuptools import setup

with open('README.rst') as fd:
    long_description = fd.read()


setup(
    # Main
    name='confspec',
    version='1.2.1',
    packages=['confspec'],
    package_dir={'': 'lib'},

    # Extra metadata
    author='Carlos Jenkins',
    author_email='carlos@jenkins.co.cr',
    url='http://confspec.readthedocs.org/',
    description='Configuration Specification Manager',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
