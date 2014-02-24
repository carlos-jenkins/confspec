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

from .utils import error


providers = {}


class FormatProvider(object):
    """
    Abstract base class for format providers.
    Format providers allow to import and export in a particular format.
    """

    @classmethod
    def do_import(cls, cfmg, string):
        """
        Interpret a string encoded in the format provided by this object and
        import the configuration within.

        This function must be implemented by any subclass.

        :param ConfigMg cfmg: The Config Manager object handling the
         configuration specification. See :class:`confspec.manager.ConfigMg`.
        :param str string: The string with a configuration encoded in the
         format provided by this object to be imported.
        """
        raise NotImplementedError()

    @classmethod
    def do_export(cls, cfmg):
        """
        Export given configuration state as a string encoded in format provided
        by this object.

        This function must be implemented by any subclass.

        :param ConfigMg cfmg: The Config Manager object handling the
         configuration specification. See :class:`confspec.manager.ConfigMg`.
        :rtype: A string with the configuration encoded in format provided by
         this object.
        """
        raise NotImplementedError()


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
                    error(
                        'Parse error, ignoring line {} "{}".'.format(
                            lnum, line
                        )
                    )
                    continue

                key = match.group('key')

                # Consider only the sections and keys in the specification
                if not section in categories or not key in keys:
                    error('Ignoring "{}" in [{}].'.format(key, section))
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
                    error(msg)
                    continue

                # Everything ok, try to set the value of the property
                try:
                    cfmg.set(key, match.group('value').strip())
                except Exception as e:
                    if not cfmg._safe:
                        raise e
                    error()
                continue

        @classmethod
        def do_export(cls, cfmg):
            """
            INI writer implementation.

            See :meth:`FormatProvider.do_export`.
            """
            categories = cfmg._categories

            output = []
            for category in sorted(categories.keys()):

                # Write category
                output.append('[{}]'.format(category))

                options = sorted(categories[category], key=lambda x: x.key)
                for option in options:

                    # Write a comment for option if available
                    if option.comment:
                        output.append('; {}'.format(comment))

                    # Write option
                    output.append(
                        '{} = {}'.format(option.key, option.value)
                    )
                output.append('')

            # Compile all lines
            return '\n'.join(output)

    providers['ini'] = INIFormatProvider

except Exception:
    pass


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
                if not category in categories:
                    error('Ignoring unknown category "{}".'.format(category))
                    continue

                # Iterate options
                for key, value in options.items():

                    # Consider only known keys
                    if not key in keys:
                        error('Ignoring unknown key "{}".'.format(key))
                        continue

                    # Check if key belongs to the category we are in
                    if keys[key].category != category:
                        msg = (
                            'Key "{}" should belong to category "{}", '
                            'found in "{}" instead.'.format(
                                key, keys[key].category, section
                            )
                        )
                        if not cfmg._safe:
                            raise SyntaxError(msg)
                        error(msg)
                        continue

                    # Everything ok, try to set the value of the option
                    try:
                        cfmg.set(key, match.group('value').strip())
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

            output = None

            # Create dictionary
            as_dict = {
                cat : {
                    opt.key : opt.repr() for opt in cfmg.categories[cat]
                } for cat in cfmg.categories
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


try:
    class DictFormatProvider(FormatProvider):
        @classmethod
        def do_import(cls, cfmg, string):
            pass

        @classmethod
        def do_export(cls, cfmg):
            pass

    providers['dict'] = DictFormatProvider

except Exception:
    pass
