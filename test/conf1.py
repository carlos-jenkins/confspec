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

from confspec import *

spec = [
    ConfigString(
        key='name',
        default='Unknown',
        validator=non_empty(),
        category='person',
        comment='The name of the person.'
    ),
    ConfigDecimal(
        key='age',
        default=18,
        validator=in_range(0, 110),
        category='person',
        comment='The age of the person.'
    ),
    ConfigBoolean(
        key='drinks',
        default=False,
        validator=None,
        category='person',
        comment='Person drinks alcohol.',
    ),
    ConfigFloat(
        key='height',
        default=1.0,
        validator=in_range(0.05, 2.72),
        category='person',
        comment='The person height (in meters).',
    ),
    ConfigList(
        key='langs',
        default=[],
        validator=all_validate_to(is_one_of(
            ['C', 'Java', 'Python', 'PHP', 'Go']
        )),
        category='person',
        comment='Programming languages the person knows.'
    ),
]


confmg = ConfigMg(
    spec,
    files=['~/.confspec/confspec.ini'],
    format='ini',
    create=True,
    notify=False,
    writeback=True,
    safe=True,
    load=True
)


conf = confmg.get_proxy()