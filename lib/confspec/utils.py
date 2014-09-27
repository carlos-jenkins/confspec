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
Module for utility functions.
"""

from __future__ import absolute_import, division, print_function


__all__ = ['first_line']


def first_line(text):
    """
    Return the first line of a text.

    >>> from confspec.utils import first_line
    >>> text = \"\"\"
    ...
    ...
    ...     The First Line
    ... Second Line
    ...   Third Line
    ... \"\"\"
    >>>
    >>> first_line(text)
    'The First Line'

    :param str text: Any text.
    :rtype: The first line in the text.
    """
    return text.strip().split('\n')[0].strip()
