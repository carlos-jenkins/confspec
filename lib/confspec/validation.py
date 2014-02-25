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


# -----------------------------------------------------------------------------
# Integer and float validation
# -----------------------------------------------------------------------------

def positive():
    """
    Validate that the given number is positive. Note that zero is neither
    positive or negative.

    >>> f = positive()
    >>> f(0)
    False
    >>> f(5)
    True
    >>> f(-5)
    False
    >>> f(45.5)
    True

    :rtype: A validator function.
    """
    def validator(num):
        return num > 0
    return validator


def negative():
    """
    Validate that the given number is negative. Note that zero is neither
    positive or negative.

    >>> f = negative()
    >>> f(0)
    False
    >>> f(5)
    False
    >>> f(-5)
    True
    >>> f(45.5)
    False

    :rtype: A validator function.
    """
    def validator(num):
        return num < 0
    return validator


def greater_than(lower):
    """
    Validate that the given number is greater than a given lower number.

    >>> f = greater_than(10)
    >>> f(10)
    False
    >>> f(20)
    True
    >>> f(5)
    False
    >>> f(-5)
    False
    >>> f(45.5)
    True

    :param lower: The lower bound to compare against.
    :type lower: int or float
    :rtype: A validator function.
    """
    def validator(num):
        return num > lower
    return validator


def greater_than_eq(lower):
    """
    Validate that the given number is greater or equal than a given lower
    number.

    >>> f = greater_than_eq(10)
    >>> f(10)
    True
    >>> f(20)
    True
    >>> f(5)
    False
    >>> f(-5)
    False
    >>> f(45.5)
    True

    :param lower: The lower bound to compare against.
    :type lower: int or float
    :rtype: A validator function.
    """
    def validator(num):
        return num >= lower
    return validator


def lower_than(upper):
    """
    Validate that the given number is less than a given upper number.

    >>> f = lower_than(10)
    >>> f(10)
    False
    >>> f(20)
    False
    >>> f(5)
    True
    >>> f(-5)
    True
    >>> f(45.5)
    False

    :param upper: The upper bound to compare against.
    :type upper: int or float
    :rtype: A validator function.
    """
    def validator(num):
        return num < upper
    return validator


def lower_than_eq(upper):
    """
    Validate that the given number is less or equal than a given upper number.

    >>> f = lower_than_eq(10)
    >>> f(10)
    True
    >>> f(20)
    False
    >>> f(5)
    True
    >>> f(-5)
    True
    >>> f(45.5)
    False

    :param upper: The upper bound to compare against.
    :type upper: int or float
    :rtype: A validator function.
    """
    def validator(num):
        return num <= upper
    return validator


def in_range(bottom, top):
    """
    Validate that a number is in the given range.

    >>> f = in_range(-10, 100)
    >>> f(-10)
    True
    >>> f(100)
    True
    >>> f(50)
    True
    >>> f(200)
    False
    >>> f(-20)
    False
    >>> f(55.85)
    True

    :param bottom: bottom interval delimiter.
    :type bottom: int or float
    :param top: top interval delimiter.
    :type top: int or float
    :rtype: A validator function.
    """
    def validator(num):
        if bottom <= num <= top:
            return True
        return False
    return validator


def multiple_of(multi):
    """
    Validate that the given number is multiple of the given multiple.

    >>> f = multiple_of(10)
    >>> f(10)
    True
    >>> f(100)
    True
    >>> f(20)
    True
    >>> f(35)
    False
    >>> f(4)
    False
    >>> f = multiple_of(5.2)
    >>> f(10.4)
    True

    :param multi: Multiple to check against.
    :type multi: int or float
    :rtype: A validator function.
    """
    def validator(num):
        return (num % multi) == 0
    return validator


def is_even():
    """
    Validate that the given number is even.

    >>> f = is_even()
    >>> f(10)
    True
    >>> f(2)
    True
    >>> f(0)
    True
    >>> f(-1)
    False
    >>> f(3)
    False
    >>> f(2.0)
    True

    :rtype: A validator function.
    """
    def validator(num):
        return (num % 2) == 0
    return validator


def is_odd():
    """
    Validate that the given number is odd.

    >>> f = is_odd()
    >>> f(3)
    True
    >>> f(-1)
    True
    >>> f(10)
    False
    >>> f(2)
    False
    >>> f(0)
    False
    >>> f(2.0)
    False

    :rtype: A validator function.
    """
    def validator(num):
        return (num % 2) == 1
    return validator


# -----------------------------------------------------------------------------
# Collections validation
# -----------------------------------------------------------------------------

def is_one_of(options):
    """
    Validate that the given attribute is member of the given list.

    >>> f = is_one_of(['foo', 'bar'])
    >>> f('ham')
    False
    >>> f('foo')
    True
    >>> f('Foo')
    False
    >>> f = is_one_of([10, 15, 20])
    >>> f(20)
    True

    :param list options: The options that the attribute can be.
    :rtype: A validator function.
    """
    def validator(item):
        return item in options
    return validator


def is_subset_of(main):
    """
    Validate that the given set is subset of the main given set.

    >>> f = is_subset_of(set(['a', 'b', 'c', 'd']))
    >>> f(set(['b', 'd']))
    True
    >>> f(set(['a', 'b', 'c', 'd']))
    True
    >>> f(set(['a', 'f']))
    False

    :param set main: The main set to compare to.
    :rtype: A validator function.
    """
    def validator(sub):
        return sub <= main
    return validator


# -----------------------------------------------------------------------------
# String validation
# -----------------------------------------------------------------------------

def has_substring(string):
    """
    Validate that the given substring is part of the given string.

    >>> f = has_substring('foobarhamjam')
    >>> f('arham')
    True
    >>> f('barham')
    True
    >>> f('FOO')
    False
    >>> f('JAMHAM')
    False

    :param str string: Main string to compare against.
    :rtype: A validator function.
    """
    def validator(substring):
        return substring in string
    return validator


def has_substring_igncase(string):
    """
    Validate that the given substring is part of the given string but ignoring
    case.

    >>> f = has_substring_igncase('foobarhamjam')
    >>> f('ArHaM')
    True
    >>> f('BARham')
    True
    >>> f('FOO')
    True
    >>> f('JAMHAM')
    False

    :param str string: Main string to compare against.
    :rtype: A validator function.
    """
    string = string.lower()

    def validator(substring):
        return substring.lower() in string
    return validator


def startswith(prefix):
    """
    Validate that the given string has the given prefix.

    >>> f = startswith('_p')
    >>> f('_parameter')
    True
    >>> f('_program')
    True
    >>> f('_peter')
    True
    >>> f('john')
    False
    >>> f('disk')
    False

    :param str prefix: The prefix to verify.
    :rtype: A validator function.
    """
    def validator(string):
        return string.startswith(prefix)
    return validator


def startswith_igncase(prefix):
    """
    Validate that the given string has the given prefix but ignoring case.

    >>> f = startswith_igncase('_p')
    >>> f('_Parameter')
    True
    >>> f('_Program')
    True
    >>> f('_peter')
    True
    >>> f('john')
    False
    >>> f('disk')
    False

    :param str prefix: The prefix to verify.
    :rtype: A validator function.
    """
    prefix = prefix.lower()

    def validator(string):
        return string.lower().startswith(prefix)
    return validator


def endswith(suffix):
    """
    Validate that the given string has the given suffix.

    >>> f = endswith('ix_')
    >>> f('My prefix_')
    True
    >>> f('My suffix_')
    True
    >>> f('Other thing')
    False

    :param str suffix: The suffix to verify.
    :rtype: A validator function.
    """
    def validator(string):
        return string.endswith(suffix)
    return validator


def endswith_igncase(suffix):
    """
    Validate that the given string has the given suffix but ignoring case.

    >>> f = endswith_igncase('ix_')
    >>> f('My PREFIX_')
    True
    >>> f('My suffix_')
    True
    >>> f('Other THING')
    False

    :param str suffix: The suffix to verify.
    :rtype: A validator function.
    """
    suffix = suffix.lower()

    def validator(string):
        return string.lower().endswith(suffix)
    return validator
