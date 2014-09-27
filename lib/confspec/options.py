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
Module for configuration options.
"""

from __future__ import absolute_import, division, print_function

import re
import ast
import keyword
import logging as log
from datetime import datetime, date, time
from os.path import exists, isfile, isdir, abspath
from inspect import isclass

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

        # Save kwargs
        self._kwargs = kwargs

        super(ConfigOpt, self).__init__()

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
                    '[{}] cannot accept <{}>. Could not be validated.'.format(
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

    def __lt__(self, other):
        if hasattr(other, 'key'):
            return self.key < other.key


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
        value = ast.literal_eval(value)

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


class ConfigLine(ConfigText):
    """
    Configuration option of type one line of text.

    Internal representation of the object is a ``str``.

    .. inheritance-diagram:: ConfigLine
       :parts: 1

    :param cleaner: A cleaner function that will be used post parsing to clean
     or transform the raw string. By default, :func:`confspec.utils.first_line`
     is used. If ``None`` is given, no transformation will be done.
    :type cleaner: function or None
    """

    def __init__(self, cleaner=first_line, **kwargs):
        super(ConfigLine, self).__init__(cleaner=cleaner, **kwargs)


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

        raise ValueError('Cannot parse <{}> as bool.'.format(value))

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
# Time related ConfigOpt's
# -----------------------------------------------------------------------------

class ConfigDateTime(ConfigOpt):
    """
    Configuration option of type date and time
    (year, month, day, hour, minute and second).

    Internal representation of the object is a Python
    :py:class:`datetime.datetime` object.

    .. inheritance-diagram:: ConfigDateTime
       :parts: 1

    :param str tformat: Format to be used by
     :py:meth:`datetime.datetime.strftime` to export the internal datetime. By
     default ISO 8601 format is used. Also, this format is used by
     :py:meth:`datetime.datetime.strptime` to parse given time strings.
    """

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
    """
    Configuration option of type date (year, month and day).

    Internal representation of the object is a Python
    :py:class:`datetime.date` object.

    .. inheritance-diagram:: ConfigDate
       :parts: 1

    :param str tformat: Format to be used by
     :py:meth:`datetime.date.strftime` to export the internal date. By default
     ISO 8601 format is used. Also, this format is used by
     :py:meth:`datetime.datetime.strptime` to parse given time strings.
    """

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
    """
    Configuration option of type time (hour, minute and second).

    Internal representation of the object is a Python
    :py:class:`datetime.time` object.

    .. inheritance-diagram:: ConfigTime
       :parts: 1

    :param str tformat: Format to be used by
     :py:meth:`datetime.time.strftime` to export the internal time. By
     default ISO 8601 format is used. Also, this format is used by
     :py:meth:`datetime.datetime.strptime` to parse given time strings.
    """

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
# Mapping ConfigOpt's
# -----------------------------------------------------------------------------

class ConfigMap(ConfigOpt):
    """
    Configuration option of type generic mapping.

    Use this configuration when you want to store a key to something and
    retrieve it's associated value in your Software.

    Internal representation of the object is a Python tuple of
    ``(key , value)``.

    .. inheritance-diagram:: ConfigMap
       :parts: 1

    :param dict table: Mapping dictionary to lookup keys.
    """

    def __init__(self, table, **kwargs):
        self._table = table
        super(ConfigMap, self).__init__(**kwargs)

    @ConfigOpt.value.getter
    def value(self):
        return self._value[1]

    def parse(self, value):
        """
        Override of :meth:`ConfigOpt.parse` that lookups the given key and, if
        found, returns it's associated value.
        """
        if value in self._table:
            return (value, self._table[value])
        raise ValueError('Cannot parse <{}>. Unknown key.'.format(value))

    def repr(self, value):
        """
        Override of :meth:`ConfigOpt.repr` that returns the key associated with
        the given value.
        """
        tkey, tvalue = value

        if tkey not in self._table:
            raise ValueError(
                'Cannot find representation of <{}>. Unknown key.'.format(tkey)
            )

        if tvalue != self._table[tkey]:
            raise ValueError((
                'Value mismatch for key <{}>. '
                'Value changed or map changed?'
            ).format(tkey))

        return tkey


class ConfigClass(ConfigMap):
    """
    Configuration option of type Python Class.

    Use this configuration when you want to store a class name in the
    configuration and be able to retrive the Class in Software. This
    configuration option uses :class:`ConfigMap` to lookup between class name
    and the class itself.

    Internal representation of the object is a Python tuple of
    ``(class_name , class)``.

    .. inheritance-diagram:: ConfigClass
       :parts: 1

    :param list classes: List of Python classes.
    """

    def __init__(self, classes, **kwargs):
        table = {}
        for c in classes:
            table[c.__name__] = c
        super(ConfigClass, self).__init__(self, table=table, **kwargs)


# -----------------------------------------------------------------------------
# File System ConfigOpt's
# -----------------------------------------------------------------------------

class ConfigPath(ConfigOpt):
    """
    Configuration option of type file system element.

    Use this configuration when you want to store any file system path in
    configuration.

    Internal representation of the object is a Python string as a absolute
    file system path using :py:func:`os.path.abspath`.

    .. inheritance-diagram:: ConfigPath
       :parts: 1

    :param function checker: Aditional checker function to be used by the
     parser. By default :py:func:`os.path.exists` is used.
    """

    def __init__(self, checker=exists, **kwargs):
        self._checker = checker
        super(ConfigPath, self).__init__(**kwargs)

    def parse(self, value):
        """
        Override of :meth:`ConfigOpt.parse` that apply
        :py:func:`os.path.abspath` and ``checker`` (if not None) to the given
        value.
        """
        value = abspath(value)
        if self._checker is not None and self._checker(value):
            return value
        raise ValueError('Cannot verify <{}>. Not found.'.format(value))

    def repr(self, value):
        """
        Override of :meth:`ConfigOpt.repr` that returns the internal path
        string.
        """
        return value


class ConfigFile(ConfigPath):
    """
    Configuration option of type file system file.

    Use this configuration when you want to store any file system file path in
    configuration.

    Internal representation of the object is a Python string as a absolute
    file system path using :py:func:`os.path.abspath`.

    .. inheritance-diagram:: ConfigFile
       :parts: 1

    :param function checker: Aditional checker function to be used by the
     parser. By default :py:func:`os.path.isfile` is used.
    """

    def __init__(self, checker=isfile, **kwargs):
        super(ConfigFile, self).__init__(checker=checker, **kwargs)


class ConfigDir(ConfigPath):
    """
    Configuration option of type file system directory.

    Use this configuration when you want to store any file system directory
    path in configuration.

    Internal representation of the object is a Python string as a absolute
    file system path using :py:func:`os.path.abspath`.

    .. inheritance-diagram:: ConfigDir
       :parts: 1

    :param function checker: Aditional checker function to be used by the
     parser. By default :py:func:`os.path.isdir` is used.
    """

    def __init__(self, checker=isdir, **kwargs):
        super(ConfigFile, self).__init__(checker=checker, **kwargs)


# -----------------------------------------------------------------------------
# Miscellaneous ConfigOpt's
# -----------------------------------------------------------------------------

class ConfigColor(ConfigOpt):
    """
    Configuration option of type RGB color using CSS-like notation ``#RRGGBB``.

    Internal representation of the object is a Python ``tuple`` of 3 ``int``.

    .. inheritance-diagram:: ConfigColor
       :parts: 1
    """

    def parse(self, value):
        """
        Override of :meth:`ConfigOpt.parse` that converts CSS-like color
        encoded string (``#RRGGBB``) into a ``tuple`` of 3 ``int``.
        """
        value = value.strip()

        if value[0] == '#':
            value = value[1:]
        if len(value) != 6:
            raise ValueError((
                'Color <{}> could not be parsed. Colors '
                'must be in #RRGGBB format.'
            ).format(value))

        r, g, b = map(
            lambda x: int(x, 16),
            [value[:2], value[2:4], value[4:]]
        )
        return (r, g, b)

    def repr(self, value):
        """
        Override of :meth:`ConfigOpt.repr` that returns a RGB color encoded
        using CSS-like notation ``#RRGGBB``.
        """
        return '#{:02x}{:02x}{:02x}'.format(*value).upper()


class ConfigFont(ConfigOpt):
    """
    Configuration option of type font using notation ``Times New Roman 12``.

    Internal representation of the object is a ``Pango.FontDescription`` and
    thus requires PyGObject. Dependencies on PyGObject are lazy-loaded in order
    to allow ``confspec`` to omit dependency on it. If you do not plan to use
    this configuration option you do not require to have PyGObject.

    .. inheritance-diagram:: ConfigFont
       :parts: 1
    """

    fonts = []
    """
    List of system font names.
    """

    def __init__(self, **kwargs):

        # Lazy load list of system fonts
        if not ConfigFont.fonts:

            # Lazy load dependencies
            from gi.repository.PangoCairo import FontMap as pcfm
            from gi.repository.Pango import FontMap as pfm

            fonts = pfm.list_families(pcfm.get_default())
            ConfigFont.fonts = sorted([f.get_name() for f in fonts])

        super(ConfigFont, self).__init__(**kwargs)

    def parse(self, value):
        """
        Override of :meth:`ConfigOpt.parse` that converts a font description
        string using notation ``Times New Roman 12`` to a
        ``Pango.FontDescription`` object. For parsing to be successful, given
        font must exists on system. For that see :attr:`ConfigFont.fonts`
        (lazy loaded, create any instance of ConfigFont first).
        """

        from gi.repository.Pango import FontDescription

        font = FontDescription.from_string(value)
        name = font.get_family()

        if name not in ConfigFont.fonts:
            raise ValueError('Unknown font <{}>.'.format(name))

        if font.get_size == 0:
            font.set_size(12 * 1024)

        return font

    def repr(self, value):
        """
        Override of :meth:`ConfigOpt.repr` that returns a font description
        string using notation ``Times New Roman 12``.
        """
        return value.to_string()


# -----------------------------------------------------------------------------
# Collection ConfigOpt's
# -----------------------------------------------------------------------------

class ConfigList(ConfigOpt):
    """
    Base mix-in class that allows to define lists of configuration options.

    Internal representation of the object is a Python ``list``.

    Please note that this class is an abstract class and cannot be used by
    itself. To make a configuration option of type list of another atomic
    configuration option do:

    .. code:: python

       class ConfigListMine(ConfigList, ConfigMine):
            pass

    .. inheritance-diagram:: ConfigList
       :parts: 1

    :param bool strict: If strict is True all elements in the list must parse
     and validate. If False, unparseable / unvalidated elements are silently
     ignored.
    """

    def __init__(self, strict=True, **kwargs):

        self._strict = strict

        # Find element parsing and representation provider
        self._provider = None
        for p in self.__class__.__bases__:
            if p != ConfigList and issubclass(p, ConfigOpt):
                self._provider = p
                break

        super(ConfigList, self).__init__(**kwargs)

    def _parse_elements(self, elements):
        """
        Parse given elements using current parsing provider.

        :param list elements: List of elements to parse.
        :rtype: A list of parsed elements. Note that this function take into
         account the ``strict`` flag and thus, if disabled, the lenght of the
         returned list could be less than the lenght of the given one.
        """
        result = []
        for e in elements:
            try:
                parsed = self._provider.parse(self, e)
                result.append(parsed)
            except Exception as e:
                if self._strict:
                    raise e
                log.error(
                    'Cannot parse/validate element <{}>.'.format(e)
                )
        return result

    def parse(self, value):
        """
        Override of :meth:`ConfigOpt.parse` that parses a list of arbitrary
        items which in turn are parsed by whatever :class:`ConfigOpt`
        based-parent is found in current class parents (bases).
        """
        if type(value) is list:
            return self._parse_elements(value)

        # Parse list
        value = value.strip()
        if (value[0], value[-1]) != ('[', ']'):
            raise ValueError('Cannot parse <{}> as list.'.format(value))

        # Check if empty list
        value = value[1:-1].strip()
        if not value:
            return []

        fragments = [v.strip() for v in value.split(',')]
        return self._parse_elements(fragments)

    def repr(self, value):
        """
        Override of :meth:`ConfigOpt.repr` that returns a list of element
        represented using whatever :class:`ConfigOpt` based-parent is found in
        current class parents (bases).
        """
        return map(
            lambda element: self._provider.repr(self, element),
            value
        )

    def __repr__(self):
        elem_repr = self.repr(self._value)
        return '[{}]'.format(', '.join(elem_repr))


class ConfigListString(ConfigList, ConfigString):
    """
    List of :class:`ConfigString` configuration option.

    .. inheritance-diagram:: ConfigListString
       :parts: 1
    """
    pass


class ConfigListText(ConfigList, ConfigText):
    """
    List of :class:`ConfigText` configuration option.

    .. inheritance-diagram:: ConfigListText
       :parts: 1
    """
    pass


class ConfigListLine(ConfigList, ConfigLine):
    """
    List of :class:`ConfigLine` configuration option.

    .. inheritance-diagram:: ConfigListLine
       :parts: 1
    """
    pass


class ConfigListInt(ConfigList, ConfigInt):
    """
    List of :class:`ConfigInt` configuration option.

    .. inheritance-diagram:: ConfigListInt
       :parts: 1
    """
    pass


class ConfigListDecimal(ConfigList, ConfigDecimal):
    """
    List of :class:`ConfigDecimal` configuration option.

    .. inheritance-diagram:: ConfigListDecimal
       :parts: 1
    """
    pass


class ConfigListOctal(ConfigList, ConfigOctal):
    """
    List of :class:`ConfigOctal` configuration option.

    .. inheritance-diagram:: ConfigListOctal
       :parts: 1
    """
    pass


class ConfigListHexadecimal(ConfigList, ConfigHexadecimal):
    """
    List of :class:`ConfigHexadecimal` configuration option.

    .. inheritance-diagram:: ConfigListHexadecimal
       :parts: 1
    """
    pass


class ConfigListBoolean(ConfigList, ConfigBoolean):
    """
    List of :class:`ConfigBoolean` configuration option.

    .. inheritance-diagram:: ConfigListBoolean
       :parts: 1
    """
    pass


class ConfigListFloat(ConfigList, ConfigFloat):
    """
    List of :class:`ConfigFloat` configuration option.

    .. inheritance-diagram:: ConfigListFloat
       :parts: 1
    """
    pass


class ConfigListDateTime(ConfigList, ConfigDateTime):
    """
    List of :class:`ConfigDateTime` configuration option.

    .. inheritance-diagram:: ConfigListDateTime
       :parts: 1
    """
    pass


class ConfigListDate(ConfigList, ConfigDate):
    """
    List of :class:`ConfigDate` configuration option.

    .. inheritance-diagram:: ConfigListDate
       :parts: 1
    """
    pass


class ConfigListTime(ConfigList, ConfigTime):
    """
    List of :class:`ConfigTime` configuration option.

    .. inheritance-diagram:: ConfigListTime
       :parts: 1
    """
    pass


class ConfigListMap(ConfigList, ConfigMap):
    """
    List of :class:`ConfigMap` configuration option.

    .. inheritance-diagram:: ConfigListMap
       :parts: 1
    """
    pass


class ConfigListClass(ConfigList, ConfigClass):
    """
    List of :class:`ConfigClass` configuration option.

    .. inheritance-diagram:: ConfigListClass
       :parts: 1
    """
    pass


class ConfigListPath(ConfigList, ConfigPath):
    """
    List of :class:`ConfigPath` configuration option.

    .. inheritance-diagram:: ConfigListPath
       :parts: 1
    """
    pass


class ConfigListFile(ConfigList, ConfigFile):
    """
    List of :class:`ConfigFile` configuration option.

    .. inheritance-diagram:: ConfigListFile
       :parts: 1
    """
    pass


class ConfigListDir(ConfigList, ConfigDir):
    """
    List of :class:`ConfigDir` configuration option.

    .. inheritance-diagram:: ConfigListDir
       :parts: 1
    """
    pass


class ConfigListColor(ConfigList, ConfigColor):
    """
    List of :class:`ConfigColor` configuration option.

    .. inheritance-diagram:: ConfigListColor
       :parts: 1
    """
    pass


class ConfigListFont(ConfigList, ConfigFont):
    """
    List of :class:`ConfigFont` configuration option.

    .. inheritance-diagram:: ConfigListFont
       :parts: 1
    """
    pass


# Export ConfigOpt subclasses only
__all__ = [
    key for key, value in dict(locals()).items()
    if isclass(value) and issubclass(value, ConfigOpt)
]
