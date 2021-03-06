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
Python dictionary format provider for confspec.
"""

from __future__ import absolute_import, division, print_function

import logging as log
from traceback import format_exc
from pprint import pformat

from . import FormatProvider, providers


__all__ = ['DictFormatProvider']


class DictFormatProvider(FormatProvider):
    """
    Python dictionary format provider.

    .. warning:: This provider uses :py:func:`eval` function.
       Use with care.
    """

    @classmethod
    def do_import(cls, cfmg, string):
        """
        Python dictionary parser implementation.

        See :meth:`FormatProvider.do_import`.
        """

        keys = cfmg._keys
        categories = cfmg._categories

        # Evaluate string
        try:
            as_dict = eval(string)
        except Exception as e:
            if not cfmg._safe:
                raise e
            log.error(format_exc())
            return

        # Check datatype
        if type(as_dict) != dict:
            msg = 'Cannot evaluate string as dictionary.'
            if not cfmg._safe:
                raise SyntaxError(msg)
            log.error(msg)
            return

        # Iterate categories
        for category, options in as_dict.items():

            # Check datatype
            if type(options) != dict:
                if not cfmg._safe:
                    raise SyntaxError(
                        'Malformed category "{}".'.format(category)
                    )
                log.error(
                    'Ignoring malformed category "{}".'.format(category)
                )
                continue

            # Consider only the categories included in the specification
            if category not in categories:
                log.error(
                    'Ignoring unknown category "{}".'.format(category)
                )
                continue

            # Iterate options
            for key, value in options.items():

                # Consider only known keys
                if key not in keys:
                    log.error('Ignoring unknown key "{}".'.format(key))
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
                    log.error(msg)
                    continue

                # Everything ok, try to set the value of the option
                try:
                    cfmg.set(key, value)
                except Exception as e:
                    if not cfmg._safe:
                        raise e
                    log.error(format_exc())

    @classmethod
    def do_export(cls, cfmg):
        """
        Python dictionary writer implementation.

        See :meth:`FormatProvider.do_export`.
        """
        categories = cfmg._categories

        output = None

        # Create dictionary
        # FIXME: Add support for comments?
        as_dict = {
            cat: {
                opt.key: opt.repr(opt._value) for opt in categories[cat]
            } for cat in categories
        }

        output = pformat(as_dict)
        return output

providers['dict'] = DictFormatProvider
