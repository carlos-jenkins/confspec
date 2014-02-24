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

providers = {}

class FormatProvider(object):
    """
    Abstract base class for format providers.
    Format providers allow to import and export in a particular format.
    """

    @classmethod
    def do_import(self, categories, keys, string):
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
    def do_export(self, categories, keys):
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
    from configparser import SafeConfigParse
    from io import StringIO

    class INIFormatProvider(FormatProvider):
        @classmethod
        def do_import(self, categories, keys, string):
            pass

        @classmethod
        def do_export(self, categories, keys):
            pass

    providers['ini'] = INIFormatProvider

except ImportError:
    pass


try:
    from json import loads, dumps

    class JSONFormatProvider(FormatProvider):
        @classmethod
        def do_import(self, categories, keys, string):
            pass

        @classmethod
        def do_export(self, categories, keys):
            pass

    providers['json'] = JSONFormatProvider

except ImportError:
    pass


try:
    class DictFormatProvider(FormatProvider):
        @classmethod
        def do_import(self, categories, keys, string):
            pass

        @classmethod
        def do_export(self, categories, keys):
            pass

    providers['dict'] = DictFormatProvider

except ImportError:
    pass
