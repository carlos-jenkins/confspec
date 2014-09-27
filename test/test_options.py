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

"""
Test confspec.options module.
"""

from __future__ import absolute_import, division, print_function

from pytest import raises

from .options import options


# -----------------------------------------------------------------------------
# Base classes
# -----------------------------------------------------------------------------

def test_ConfigOpt():
    # FIXME IMPLEMENT
    pass


def test_ConfigList():
    # FIXME IMPLEMENT
    pass


# -----------------------------------------------------------------------------
# Entity classes
# -----------------------------------------------------------------------------

def test_ConfigString():
    # FIXME IMPLEMENT
    pass


def test_ConfigText():
    # FIXME IMPLEMENT
    pass


def test_ConfigLine():
    # FIXME IMPLEMENT
    pass


def test_ConfigInt():
    opt = options['ConfigInt']

    assert opt.value == 99

    # Test parsing and repr
    for value in ['33', -33, 0]:
        opt.value = value
        assert opt.value == int(value)

    # Check non parsing
    for nonint in ['foobar', '', 'AAA', 'bool', '3.0', 6.0]:
        with raises(ValueError):
            opt.value = nonint

    # Check multiple
    for nonmultiple in [-20, 4, 0.1]:
        with raises(ValueError):
            opt.value = nonmultiple


def test_ConfigDecimal():
    # FIXME IMPLEMENT
    pass


def test_ConfigOctal():
    # FIXME IMPLEMENT
    pass


def test_ConfigHexadecimal():
    # FIXME IMPLEMENT
    pass


def test_ConfigBoolean():
    opt = options['ConfigBoolean']

    assert opt.value is True

    # Assert all false options with case diference
    for false in ['false', 'no', '0', 'off']:
        opt.value = false
        assert opt.value is False
        opt.value = false.upper()
        assert opt.value is False
        opt.value = '    {}    '.format(false)
        assert opt.value is False

    # Assert all true options with case diference
    for true in ['true', 'yes', '1', 'on']:
        opt.value = true
        assert opt.value is True
        opt.value = true.upper()
        assert opt.value is True
        opt.value = '    {}    '.format(true)
        assert opt.value is True

    # Check non parsing
    for nonbool in ['foobar', '', 'AAA', 'bool']:
        with raises(ValueError):
            opt.value = nonbool


def test_ConfigFloat():
    opt = options['ConfigFloat']

    assert opt.value == 3.14

    # Test parsing and repr
    for value in ['3.14', -1.0, 44.145, '-11.44', '0', 10]:
        opt.value = value
        assert opt.value == float(value)
        opt.value = '    {}    '.format(value)
        assert opt.value == float(value)

    # Test sformat pasing and repr
    opt._sformat = '{:.2f}'
    for value in ['3.1415', -1.0145, 44.145, '-11.45644', 100.001]:
        opt.value = '    {}    '.format(value)
        assert opt.value != float(value)
        assert opt.value == float(
            opt._sformat.format(float(value))  # Test float strip
        )
    opt._sformat = None

    # Check non parsing
    for nonfloat in ['foobar', '', 'AAA', 'bool']:
        with raises(ValueError):
            opt.value = nonfloat

    # Check range
    for nonrange in [200.0, -200.0, 100.01]:
        with raises(ValueError):
            opt.value = nonrange


def test_ConfigDateTime():
    # FIXME IMPLEMENT
    pass


def test_ConfigDate():
    # FIXME IMPLEMENT
    pass


def test_ConfigTime():
    # FIXME IMPLEMENT
    pass


def test_ConfigMap():
    # FIXME IMPLEMENT
    pass


def test_ConfigClass():
    # FIXME IMPLEMENT
    pass


def test_ConfigPath():
    # FIXME IMPLEMENT
    pass


def test_ConfigFile():
    # FIXME IMPLEMENT
    pass


def test_ConfigDir():
    # FIXME IMPLEMENT
    pass


def test_ConfigColor():
    # FIXME IMPLEMENT
    pass


def test_ConfigFont():
    # FIXME IMPLEMENT
    pass


# -----------------------------------------------------------------------------
# Collection classes
# -----------------------------------------------------------------------------

def test_ConfigListString():
    # FIXME IMPLEMENT
    pass


def test_ConfigListText():
    # FIXME IMPLEMENT
    pass


def test_ConfigListLine():
    # FIXME IMPLEMENT
    pass


def test_ConfigListInt():
    # FIXME IMPLEMENT
    pass


def test_ConfigListDecimal():
    # FIXME IMPLEMENT
    pass


def test_ConfigListOctal():
    # FIXME IMPLEMENT
    pass


def test_ConfigListHexadecimal():
    # FIXME IMPLEMENT
    pass


def test_ConfigListBoolean():
    # FIXME IMPLEMENT
    pass


def test_ConfigListFloat():
    # FIXME IMPLEMENT
    pass


def test_ConfigListDateTime():
    # FIXME IMPLEMENT
    pass


def test_ConfigListDate():
    # FIXME IMPLEMENT
    pass


def test_ConfigListTime():
    # FIXME IMPLEMENT
    pass


def test_ConfigListMap():
    # FIXME IMPLEMENT
    pass


def test_ConfigListClass():
    # FIXME IMPLEMENT
    pass


def test_ConfigListPath():
    # FIXME IMPLEMENT
    pass


def test_ConfigListFile():
    # FIXME IMPLEMENT
    pass


def test_ConfigListDir():
    # FIXME IMPLEMENT
    pass


def test_ConfigListColor():
    # FIXME IMPLEMENT
    pass


def test_ConfigListFont():
    # FIXME IMPLEMENT
    pass
