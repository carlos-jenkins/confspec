#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Carlos Jenkins <carlos@jenkins.co.cr>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

# Load development requirements
with open('requirements.dev.txt', 'r') as fd:
    tests_require = fd.read().split()

# Load long description
with open('README.rst', 'r') as fd:
    long_description = fd.read()


class Tox(TestCommand):
    """
    Test command for setup.py - tox integration.
    """

    user_options = [('tox-args=', 'a', 'Arguments to pass to tox')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)


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

    # Integration
    tests_require=tests_require,
    cmdclass={'test': Tox},
)
