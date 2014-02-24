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

import re
import keyword

from .utils import first_line


class ConfigOpt(object):
    """
    Base configuration option ``{Key : Value}`` object.

    :param str key: Key of the configuration.
    :param default: Default value of the configuration. This value is treated
     like any other value and thus is parsed and validated prior to set it.
    :param function validator: A optinal validator function.
    :param str category: The category of the configuration option.
    """

    def __init__(
            self,
            key=None, default=None,
            validator=None,
            category='general',
            comment=''):

        # Private attributes
        self._key = None
        self._value = None
        self.category = self._valid_key(category)
        self.comment = first_line(comment)

        # Validate and set attributes
        self.validator = validator
        self.key = key
        self.value = default

    def _valid_key(self, new_key):
        """
        Validate a key so it can be used as a Python variable/attribute name.
        """
        if not isinstance(new_key, str):
            raise ValueError('Key must be a string.')
        new_key = new_key.strip()
        if not new_key:
            raise ValueError('String must not be empty.')
        if not re.match('[_A-Za-z][_a-zA-Z0-9]*$', new_key) or \
                keyword.iskeyword(new_key):
            raise ValueError('Invalid key name.')
        return new_key

    @property
    def key(self):
        """
        Key of this configuration option.
        """
        return self._key

    @key.setter
    def key(self, new_key):
        if self._key is not None:
            raise AttributeError('Cannot change key once set.')
        self._key = self._valid_key(new_key)

    @property
    def value(self):
        """
        Value (internal representation) associated to this configuration
        option.
        """
        return self._value

    @value.setter
    def value(self, raw):
        parsed = self.parse(raw)
        if self.validator is not None:
            self.validator(parsed)
        self._value = parsed

    def parse(self, value):
        """
        Abstract function that musts parse a string representation of the
        configuration option and store the result as the internal
        representation of it.

        This function must be implemented by any subclass. Is left to the
        subclasses the option to interpret any other datatypes besides string,
        but at least string must be supported.

        :param str value: A string representation of the configuration option.
        """
        raise NotImplementedError()

    def repr(self):
        """
        Abstract function that must transform the internal representation of
        the configuration option into a string.

        This function must be implemented by any subclass.

        :rtype: A string representation of the configuration option.
        """
        raise NotImplementedError()

    def __delattr__(self, name):
        raise TypeError('Cannot delete configuration keys.')

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.repr()
