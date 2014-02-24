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
    def do_import(cls, cfgm, string):
        """
        Interpret a string encoded in the format provided by this object and
        import the configuration within.

        This function must be implemented by any subclass.

        :param dict categories: The configuration dictionary that maps
         categories with list of :class:`confspec.options.ConfigOpt` instances
         that belongs to that category.
        :param dict keys: The configuration dictionary that maps keys with
         :class:`confspec.options.ConfigOpt` instances.
        :param str string: The string with a configuration encoded in the
         format provided by this object to be imported.
        """
        raise NotImplementedError()

    @classmethod
    def do_export(cls, cfgm):
        """
        Export given configuration state as a string encoded in format provided
        by this object.

        This function must be implemented by any subclass.

        :param dict categories: The configuration dictionary that maps
         categories with list of :class:`confspec.options.ConfigOpt` instances
         that belongs to that category.
        :param dict keys: The configuration dictionary that maps keys with
         :class:`confspec.options.ConfigOpt` instances.
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
        def do_import(cls, cfgm, string):
            """
            INI parser implementation.

            See :meth:`FormatProvider.do_import`.
            """
            keys = cfgm._keys
            categories = cfgm._categories
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
                        raise ValueError(
                            'Cannot parse line {} : "{}"'.format(lnum, line)
                        )
                    error(
                        'Parse error, ignoring line {} "{}"'.format(
                            lnum, line
                        )
                    )
                    continue

                key = match.group('key')

                # Consider only the sections and keys in the specification
                if not section in categories or not key in keys:
                    error('Ignoring "{}" in [{}]'.format(key, section))
                    continue

                # Check if key belongs to the section we are in
                if keys[key].category != section:
                    msg = (
                        'Property "{}" should belong to "{}", '
                        'found in "{}"'.format(
                            key, keys[key].category, section
                        )
                    )
                    if not cfmg._safe:
                        raise ValueError(msg)
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
        def do_export(cls, cfgm):
            """
            INI writer implementation.

            See :meth:`FormatProvider.do_export`.
            """
            categories = cfgm._categories

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
    #from json import loads, dumps

    class JSONFormatProvider(FormatProvider):
        """
        JSON format provider.

        This provider uses Python's json module.
        """

        @classmethod
        def do_import(cls, cfgm, string):
            pass

        @classmethod
        def do_export(cls, cfgm):
            pass

    providers['json'] = JSONFormatProvider

except Exception:
    pass


try:
    class DictFormatProvider(FormatProvider):
        @classmethod
        def do_import(cls, cfgm, string):
            pass

        @classmethod
        def do_export(cls, cfgm):
            pass

    providers['dict'] = DictFormatProvider

except Exception:
    pass
