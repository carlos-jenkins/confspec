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
Test confspec.providers.json module.
"""

from __future__ import absolute_import, division, print_function

# from pytest import raises

from confspec.manager import ConfigMg
from confspec.providers.json import JSONFormatProvider

from ..options import spec


input_str = """\
{
    "collectionconfigopts": {
        "configlistint": [
            1,
            2,
            3,
            4,
            5
        ]
    },
    "entityconfigopts": {
        "configboolean": true,
        "configfloat": 100.0,
        "configint": 0
    }
}
"""

bad_inputs = [
    # Bad input
    """dasdsdaddP{,,},11""",
    # Valid JSON, not object
    """100""",
    # First level keys are no categories
    """{"foo": 100}""",
    # Unknown category
    """{"mynonexistantcategory": {"foo": 100}}""",
    # Unknown key
    """{"collectionconfigopts": {"configint": "abc"}}""",
    # Known key in wrong category
    """{"entityconfigopts": {"unknownkey": 99}""",
    # Setting a bad value
    """{"collectionconfigopts": {"configint": 99}}""",
]


def test_JSONFormatProvider():

    mgr = ConfigMg(spec)
    JSONFormatProvider.do_import(mgr, input_str)
    output_str = JSONFormatProvider.do_export(mgr)
    print('Expected output:')
    print(output_str)
    assert input_str.strip() == output_str.strip()

    # Check bad input (default safe=True)
    mgr._safe = True
    for bad in bad_inputs:
        JSONFormatProvider.do_import(mgr, bad)

    # Check bad input (safe=False)
    # mgr._safe = False
    # for bad in bad_inputs:
    #     with raises(Exception):
    #         JSONFormatProvider.do_import(mgr, bad)
