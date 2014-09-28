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
Test confspec.providers.ini module.
"""

from __future__ import absolute_import, division, print_function

from pytest import raises

from confspec.manager import ConfigMg
from confspec.providers.ini import INIFormatProvider

from ..options import spec


input_str = """\
[collectionconfigopts]
; ConfigListInt Test.
configlistint = [1, 2, 3, 4, 5]

[entityconfigopts]
; ConfigBoolean Test.
configboolean = True
; ConfigFloat Test.
configfloat = 100.0
; ConfigInt Test.
configint = 0
"""

bad_inputs = [
    # Bad input
    ("""[entityconfigopts]\nddsasd;;===asda===""", SyntaxError),
    # Unknown category and key
    ("""[foobar]\nfoo = 100""", None),
    # Known key in wrong category
    ("""[collectionconfigopts]\nconfigint = 99""", SyntaxError),
    # Setting a bad value
    ("""[entityconfigopts]\nconfigint = abc""", ValueError),
]


def test_INIFormatProvider():

    mgr = ConfigMg(spec)
    INIFormatProvider.do_import(mgr, input_str)
    output_str = INIFormatProvider.do_export(mgr)
    print(output_str)
    assert input_str == output_str

    # Check bad input (default safe=True)
    mgr._safe = True
    for bad, exc in bad_inputs:
        INIFormatProvider.do_import(mgr, bad)

    # Check bad input (safe=False)
    mgr._safe = False
    for bad, exc in bad_inputs:
        if exc is not None:
            with raises(exc):
                INIFormatProvider.do_import(mgr, bad)
