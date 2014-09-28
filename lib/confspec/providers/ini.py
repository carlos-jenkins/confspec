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
INI format provider for confspec.
"""

from __future__ import absolute_import, division, print_function

import logging as log
from traceback import format_exc

from . import FormatProvider, providers


__all__ = ['INIFormatProvider']


try:
    import re

    class INIFormatProvider(FormatProvider):
        """
        INI format provider.

        Note that ``confspec`` uses it's own parser and reader implementation.
        """

        section_regex = r'^\[ *(?P<section>\w+) *]$'
        """Regular expression that matches sections."""
        _compiled_section_regex = re.compile(section_regex)

        property_regex = r'^ *(?P<key>\w+) *= *(?P<value>.+)$'
        """Regular expression that matches properties."""
        _compiled_property_regex = re.compile(property_regex)

        @classmethod
        def do_import(cls, cfmg, string):
            """
            INI parser implementation.

            See :meth:`FormatProvider.do_import`.
            """
            keys = cfmg._keys
            categories = cfmg._categories
            section = 'general'

            for lnum, line in enumerate(string.split('\n'), 1):
                line = line.strip()

                # Ignore comments and empty lines
                if not line or line.startswith(';'):
                    continue

                # Change section we are if a new section is found
                match = cls._compiled_section_regex.match(line)
                if match:
                    section = match.group('section')
                    continue

                # Parse a property
                match = cls._compiled_property_regex.match(line)
                if not match:
                    if not cfmg._safe:
                        raise SyntaxError(
                            'Cannot parse line {} : "{}".'.format(lnum, line)
                        )
                    log.error(
                        'Parse error, ignoring line {} "{}".'.format(
                            lnum, line
                        )
                    )
                    continue

                key = match.group('key')

                # Consider only the sections and keys in the specification
                if section not in categories or key not in keys:
                    log.error('Ignoring "{}" in [{}].'.format(key, section))
                    continue

                # Check if key belongs to the section we are in
                if keys[key].category != section:
                    msg = (
                        'Property "{}" should belong to section "[{}]", '
                        'found in "[{}]" instead.'.format(
                            key, keys[key].category, section
                        )
                    )
                    if not cfmg._safe:
                        raise SyntaxError(msg)
                    log.error(msg)
                    continue

                # Everything ok, try to set the value of the property
                try:
                    cfmg.set(key, match.group('value').strip())
                except Exception as e:
                    if not cfmg._safe:
                        raise e
                    log.error(format_exc())

        @classmethod
        def do_export(cls, cfmg):
            """
            INI writer implementation.

            See :meth:`FormatProvider.do_export`.
            """
            categories = cfmg._categories

            output = []
            for category in sorted(categories):

                # Write category
                output.append('[{}]'.format(category))

                options = sorted(categories[category])
                for option in options:

                    # Write a comment for option if available
                    if option.comment:
                        output.append('; {}'.format(option.comment))

                    # Write option
                    formatted = '{} = {}'.format(
                        option.key, repr(option)
                    )
                    output.append(formatted)
                output.append('')

            # Compile all lines
            return '\n'.join(output)

    providers['ini'] = INIFormatProvider

except Exception:
    log.error(format_exc())
