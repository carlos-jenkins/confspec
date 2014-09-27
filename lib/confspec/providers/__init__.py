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
Module for import/export format providers.
"""

from __future__ import absolute_import, division, print_function


__all__ = ['providers', 'FormatProvider']


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


from .ini import *  # noqa
from .json import *  # noqa
from .dict import *  # noqa
