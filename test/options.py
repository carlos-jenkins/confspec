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
Module listing ConfigOpt.
"""

from confspec.options import *  # noqa
from confspec.validation import *  # noqa

__all__ = ['options']


# ConfigOpt instances for testing
options = {
    'ConfigOpt': None,
    'ConfigList': None,
    'ConfigString': None,
    'ConfigText': None,
    'ConfigLine': None,
    'ConfigInt': ConfigInt(
        key='configint',
        default=99,
        validator=multiple_of(3),
        category='testcategory',
        comment='ConfigInt Test.',
    ),
    'ConfigDecimal': None,
    'ConfigOctal': None,
    'ConfigHexadecimal': None,
    'ConfigBoolean': ConfigBoolean(
        key='configboolean',
        default=True,
        validator=None,
        category='testcategory',
        comment='ConfigBoolean Test.',
    ),
    'ConfigFloat': ConfigFloat(
        key='configfloat',
        default=3.14,
        validator=in_range(-100.0, 100.0),
        category='testcategory',
        comment='ConfigFloat Test.',
    ),
    'ConfigDateTime': None,
    'ConfigDate': None,
    'ConfigTime': None,
    'ConfigMap': None,
    'ConfigClass': None,
    'ConfigPath': None,
    'ConfigFile': None,
    'ConfigDir': None,
    'ConfigColor': None,
    'ConfigFont': None,
    'ConfigListString': None,
    'ConfigListText': None,
    'ConfigListLine': None,
    'ConfigListInt': None,
    'ConfigListDecimal': None,
    'ConfigListOctal': None,
    'ConfigListHexadecimal': None,
    'ConfigListBoolean': None,
    'ConfigListFloat': None,
    'ConfigListDateTime': None,
    'ConfigListDate': None,
    'ConfigListTime': None,
    'ConfigListMap': None,
    'ConfigListClass': None,
    'ConfigListPath': None,
    'ConfigListFile': None,
    'ConfigListDir': None,
    'ConfigListColor': None,
    'ConfigListFont': None,
}

# List of ConfigOpt instances (config spec)
spec = [v for v in options.values() if v is not None]
