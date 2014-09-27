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
JSON format provider for confspec.
"""

from __future__ import absolute_import, division, print_function

from . import FormatProvider, providers
from ..utils import error


try:
    from json import loads, dumps

    class JSONFormatProvider(FormatProvider):
        """
        JSON format provider.

        This provider uses Python's json module.
        """

        @classmethod
        def do_import(cls, cfmg, string):
            """
            JSON parser implementation.

            See :meth:`FormatProvider.do_import`.
            """

            keys = cfmg._keys
            categories = cfmg._categories

            # Parse JSON
            try:
                as_dict = loads(string)
            except Exception as e:
                if not cfmg._safe:
                    raise e
                error()
                return

            # Parse type
            if type(as_dict) != dict:
                msg = 'Cannot parse JSON as dictionary.'
                if not cfmg._safe:
                    raise SyntaxError(msg)
                error(msg)
                return

            # Iterate categories
            for category, options in as_dict.items():

                # Check datatype
                if type(options) != dict:
                    if not cfmg._safe:
                        raise SyntaxError(
                            'Malformed category "{}".'.format(category)
                        )
                    error(
                        'Ignoring malformed category "{}".'.format(category)
                    )
                    continue

                # Consider only the categories included in the specification
                if category not in categories:
                    error('Ignoring unknown category "{}".'.format(category))
                    continue

                # Iterate options
                for key, value in options.items():

                    # Consider only known keys
                    if key not in keys:
                        error('Ignoring unknown key "{}".'.format(key))
                        continue

                    # Check if key belongs to the category we are in
                    if keys[key].category != category:
                        msg = (
                            'Key "{}" should belong to category "{}", '
                            'found in "{}" instead.'.format(
                                key, keys[key].category, category
                            )
                        )
                        if not cfmg._safe:
                            raise SyntaxError(msg)
                        error(msg)
                        continue

                    # Everything ok, try to set the value of the option
                    try:
                        cfmg.set(key, value)
                    except Exception as e:
                        if not cfmg._safe:
                            raise e
                        error()
                    continue

        @classmethod
        def do_export(cls, cfmg):
            """
            JSON writer implementation.

            See :meth:`FormatProvider.do_export`.
            """
            categories = cfmg._categories

            output = None

            # Create dictionary
            as_dict = {
                cat: {
                    opt.key: opt.repr(opt._value) for opt in categories[cat]
                } for cat in categories
            }

            # Try to convert dictionary to JSON
            try:
                output = dumps(as_dict, indent=4, sort_keys=True)
            except Exception as e:
                if not cfmg._safe:
                    raise e
                error()

            return output

    providers['json'] = JSONFormatProvider

except Exception:
    pass