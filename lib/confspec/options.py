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
import sys
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
            key=None,
            default=None,
            validator=None,
            category='general',
            comment='',
            **kwargs):

        # Private attributes
        self._key = None
        self._value = None
        self.category = self._valid_key(category)
        self.comment = first_line(comment)

        # Validate and set attributes
        self.validator = validator
        self.key = key
        self.value = default

        super(ConfigOpt, self).__init__(**kwargs)

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
            if not self.validator(parsed):
                raise ValueError(
                    '[{}] cannot accept [{}]. Could not be validated.'.format(
                        self._key, parsed
                    )
                )
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

    def repr(self, value):
        """
        Abstract function that must transform the internal representation of
        the configuration option into a form that can be parsed back.

        This function must be implemented by any subclass.

        :param value: A internal representation of the configuration options.
        :rtype: A representation of the configuration option.
        """
        raise NotImplementedError()

    def __delattr__(self, name):
        raise TypeError('Cannot delete configuration keys.')

    def __repr__(self):
        return str(self.repr(self._value))

    def __str__(self):
        return repr(self)

    def __cmp__(self, other):
        if hasattr(other, 'key'):
            return cmp(self.key, other.key)


# -----------------------------------------------------------------------------
# Base datatypes ConfigOpt's
# -----------------------------------------------------------------------------

class ConfigString(ConfigOpt):
    """
    Configuration option of type quoted string with backslash interpretation.

    Internal representation of the object is the ``str`` itself.

    .. inheritance-diagram:: ConfigString
       :parts: 1

    :param cleaner: A cleaner function that will be used post parsing to clean
     or transform the raw string. If ``None`` is given (the default), no
     transformation will be done.
    :type cleaner: function or None
    """

    def __init__(self, cleaner=None, **kwargs):
        self._cleaner = cleaner
        super(ConfigString, self).__init__(**kwargs)

    def parse(self, value):
        """
        Override of :meth:`ConfigOpt.parse` that interprets value to string.
        """
        if sys.version_info >= (3, 0):
            method = 'unicode_escape'
        else:
            method = 'string_escape'

        value = value.decode(method)

        if self._cleaner is not None:
            return self._cleaner(str(value))
        return str(value)

    def repr(self, value):
        """
        Override of :meth:`ConfigOpt.repr` that returns the quoted
        representation of the internal string.
        """
        return repr(value)


class ConfigText(ConfigOpt):
    """
    Configuration option of type unrestricted text.

    Internal representation of the object is a ``str``.

    .. inheritance-diagram:: ConfigText
       :parts: 1

    :param cleaner: A cleaner function that will be used post parsing to clean
     or transform the raw string. If ``None`` is given (the default), no
     transformation will be done.
    :type cleaner: function or None
    """

    def __init__(self, cleaner=None, **kwargs):
        self._cleaner = cleaner
        super(ConfigText, self).__init__(**kwargs)

    def parse(self, value):
        """
        Override of :meth:`ConfigOpt.parse` that converts value to string.
        """
        if self._cleaner is not None:
            return self._cleaner(str(value))
        return str(value)

    def repr(self, value):
        """
        Override of :meth:`ConfigOpt.repr` that returns the internal string.
        """
        return value


class ConfigLine(ConfigOpt):
    """
    Configuration option of type one line of text.

    Internal representation of the object is a ``str``.

    .. inheritance-diagram:: ConfigText
       :parts: 1

    :param cleaner: A cleaner function that will be used post parsing to clean
     or transform the raw string. By default, :func:`confspec.utils.first_line`
     is used. If ``None`` is given, no transformation will be done.
    :type cleaner: function or None
    """

    def __init__(self, cleaner=first_line, **kwargs):
        self._cleaner = cleaner
        super(ConfigText, self).__init__(**kwargs)

    def parse(self, value):
        """
        Override of :meth:`ConfigOpt.parse` that converts value to string.
        """
        if self._cleaner is not None:
            return self._cleaner(str(value))
        return str(value)

    def repr(self, value):
        """
        Override of :meth:`ConfigOpt.repr` that returns the internal string.
        """
        return value


class ConfigInt(ConfigOpt):
    """
    Configuration option of type integer.

    Internal representation of the object is a Python ``int``.

    .. inheritance-diagram:: ConfigInt
       :parts: 1

    :param int base: The radix to be used to interpret a string while parsing
     as defined in :py:func:`int`. ``0`` (zero) means to interpret the string
     exactly as an integer literal so that the actual base is guessed from
     options 2, 8, 10, or 16.
    :param str sformat: Format to be used by :py:func:`print` to export the
     internal integer.
    """

    def __init__(self, base=0, sformat=None, **kwargs):
        self._base = base
        self._sformat = sformat
        super(ConfigInt, self).__init__(**kwargs)

    def parse(self, value):
        """
        Override of :meth:`ConfigOpt.parse` that parses an integer using radix
        specified by ``base``.
        """
        if type(value) is int:
            return value

        return int(value, self._base)

    def repr(self, value):
        """
        Override of :meth:`ConfigOpt.repr` that returns a formatted version of
        the internal integer using ``sformat`` if defined, otherwise returns
        the internal integer.
        """
        if self._sformat is not None:
            return self._sformat.format(value)
        return value


class ConfigDecimal(ConfigInt):
    """
    Configuration option of type decimal.

    Internal representation of the object is a Python ``int``.

    Note that the default parameters ``base`` is overridden.

    .. inheritance-diagram:: ConfigDecimal
       :parts: 1
    """

    def __init__(self, base=10, **kwargs):
        kwargs['base'] = base
        super(ConfigDecimal, self).__init__(**kwargs)


class ConfigOctal(ConfigInt):
    """
    Configuration option of type octal.

    Internal representation of the object is a Python ``int``.

    Note that the default parameters ``base`` and ``sformat`` are overridden.

    .. inheritance-diagram:: ConfigOctal
       :parts: 1
    """

    def __init__(self, base=8, sformat='0{:o}', **kwargs):
        kwargs['base'] = base
        kwargs['sformat'] = sformat
        super(ConfigOctal, self).__init__(**kwargs)


class ConfigHexadecimal(ConfigInt):
    """
    Configuration option of type hexadecimal.

    Internal representation of the object is a Python ``int``.

    Note that the default parameters ``base`` and ``sformat`` are overridden.

    .. inheritance-diagram:: ConfigHexadecimal
       :parts: 1
    """

    def __init__(self, base=16, sformat='0x{:x}', **kwargs):
        kwargs['base'] = base
        kwargs['sformat'] = sformat
        super(ConfigHexadecimal, self).__init__(**kwargs)


class ConfigBoolean(ConfigOpt):
    """
    Configuration option of type boolean.

    Internal representation of the object is a Python ``bool``.

    .. inheritance-diagram:: ConfigBoolean
       :parts: 1
    """

    def __init__(self, **kwargs):
        super(ConfigBoolean, self).__init__(**kwargs)

    def parse(self, value):
        """
        Override of :meth:`ConfigOpt.parse` that parses a boolean:

        - Strings ``'false'``, ``'no'``, ``'0'`` and ``'off'`` are considered
          ``False``.
        - Strings ``'true'``, ``'yes'``, ``'1'`` and ``'on'`` are considered
          ``True``.

        Comparison ignores case.
        """
        if type(value) is bool:
            return value

        value = value.lower().strip()
        if value in ['true', 'yes', '1', 'on']:
            return True
        if value in ['false', 'no', '0', 'off']:
            return False

        raise ValueError('Cannot parse "{}" as bool.'.format(value))

    def repr(self, value):
        """
        Override of :meth:`ConfigOpt.repr` that returns ``True`` or
        ``False`` depending of the internal value.
        """
        return value


class ConfigFloat(ConfigOpt):
    """
    Configuration option of type floating point number.

    Internal representation of the object is a Python ``float``.

    .. inheritance-diagram:: ConfigFloat
       :parts: 1

    :param str sformat: Format to be used by :py:func:`print` to export the
     internal float.
    """

    def __init__(self, sformat=None, **kwargs):
        self._sformat = sformat
        super(ConfigFloat, self).__init__(**kwargs)

    def parse(self, value):
        """
        Override of :meth:`ConfigOpt.parse` that parses an floting point number
        using Python's :py:func:`float` function.
        """
        if type(value) is float:
            return value

        return float(value)

    def repr(self, value):
        """
        Override of :meth:`ConfigOpt.repr` that returns a formatted version of
        the internal float using ``sformat`` if defined, otherwise returns the
        internal float.
        """
        if self._sformat is not None:
            return self._sformat.format(value)
        return value


# -----------------------------------------------------------------------------
# Collection ConfigOpt's
# -----------------------------------------------------------------------------

# TODO: Document from here.

class ConfigList(ConfigOpt):

    def __init__(self, **kwargs):
        super(ConfigList, self).__init__(**kwargs)

    def parse(self, value):
        if type(value) is list:
            return map(self.element_parse, value)

        # Parse list
        value = value.strip()
        if (value[0], value[-1]) != ('[', ']'):
            raise ValueError('Cannot parse "{}" as list.'.format(value))

        # Check if empty list
        value = value[1:-1].strip()
        if not value:
            return []

        fragments = [v.strip() for v in value.split(',')]
        return map(self.element_parse, fragments)

    def element_parse(self, element):
        return self.__class__.__bases__[-1].parse(self, element)

    def repr(self, value):
        return map(self.element_repr, value)

    def element_repr(self, element):
        return self.__class__.__bases__[-1].repr(self, element)

    def __repr__(self):
        return '[{}]'.format(
            ', '.join(map(self.element_repr, self._value))
        )


class ConfigListString(ConfigList, ConfigString):
    pass


class ConfigListText(ConfigList, ConfigText):
    pass


class ConfigListLine(ConfigList, ConfigLine):
    pass


class ConfigListInt(ConfigList, ConfigInt):
    pass


class ConfigListDecimal(ConfigList, ConfigDecimal):
    pass


class ConfigListOctal(ConfigList, ConfigOctal):
    pass


class ConfigListHexadecimal(ConfigList, ConfigHexadecimal):
    pass


class ConfigListBoolean(ConfigList, ConfigBoolean):
    pass


class ConfigListFloat(ConfigList, ConfigFloat):
    pass


class ConfigTable(ConfigOpt):

    def __init__(self, table, **kwargs):
        self._table = table
        super(ConfigTable, self).__init__(**kwargs)

    def parse(self, value):
        if value in self._table:
            return self._table[value]
        raise ValueError('Cannot parse "{}". Unknown value.'.format(value))

    def repr(self, value):
        for key, tvalue in self._table:
            if tvalue == value:
                return key
        raise ValueError('Cannot found item "{}" in table.'.format(value))


class ConfigClass(ConfigTable):

    def __init__(self, classes, **kwargs):
        table = {}
        for c in classes:
            table[c.__name__] = c
        super(ConfigClass, self).__init__(self, table=table, **kwargs)


# -----------------------------------------------------------------------------
# Time related ConfigOpt's
# -----------------------------------------------------------------------------

from datetime import datetime, date, time


class ConfigDateTime(ConfigOpt):
    def __init__(self, tformat='%Y-%m-%dT%H:%M:%S', **kwargs):
        super(ConfigDateTime, self).__init__(**kwargs)

    def parse(self, value):
        """
        Override of :meth:`ConfigOpt.parse` that converts value to a
        :py:class:`datetime.datetime` object.
        """
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, self._tformat)

    def repr(self, value):
        """
        Override of :meth:`ConfigOpt.repr` that returns a formatted string
        representation of the internal datetime object using given ``tformat``.
        """
        return value.strftime(self._tformat)


class ConfigDate(ConfigDateTime):
    def __init__(self, tformat='%Y-%m-%d', **kwargs):
        self._tformat = tformat
        super(ConfigDate, self).__init__(**kwargs)

    def parse(self, value):
        """
        Override of :meth:`ConfigDateTime.parse` that converts value to a
        :py:class:`datetime.date` object.
        """
        if isinstance(value, date):
            return value
        dt = super(ConfigDate, self).parse(value)
        return dt.date()


class ConfigTime(ConfigDateTime):
    def __init__(self, tformat='%H:%M:%S', **kwargs):
        self._tformat = tformat
        super(ConfigTime, self).__init__(**kwargs)

    def parse(self, value):
        """
        Override of :meth:`ConfigDateTime.parse` that converts value to a
        :py:class:`datetime.time` object.
        """
        if isinstance(value, time):
            return value
        dt = super(ConfigTime, self).parse(value)
        return dt.time()


# -----------------------------------------------------------------------------
# Miscellaneous ConfigOpt's
# -----------------------------------------------------------------------------

class ConfigColor(ConfigOpt):
    pass


class ConfigFont(ConfigOpt):
    pass
