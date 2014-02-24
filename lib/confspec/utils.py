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

from __future__ import print_function

from sys import stderr
from traceback import format_exc


def _error(exc=None):
    """
    Custom error printing function for confspec.

    Messages or traceback are printed to :py:obj:`sys.stderr` using the
    following template:

    ::

      * confspec:
      *   <traceback or message>
      *

    User can change the format and way in which the error is printed or logged
    by replacing this function:

    >>> from confspec.utils import error
    >>> error('This is an error')
    * confspec:
    *   This is an error
    >>> def myerror(exc=None):
    ...     print('~~ My Error:\\n~~ {}'.format(exc))
    ...
    >>> import confspec.utils
    >>> confspec.utils._error = myerror
    >>> error('This is an error')
    ~~ My Error:
    ~~ This is an error

    :param exc: Error message to display. If ``None``, last traceback is
     printed using :py:func:`traceback.format_exc`.
    :type exc: str or None
    """
    if exc is None:
        exc = format_exc()
    print('* confspec:', file=stderr)
    for line in exc.split('\n'):
        print('*  ', line, file=stderr)


def error(exc=None):
    """
    Wrapper function for :func:`_error`.

    ``confspec`` modules use this function in order to allow user to change
    the way errors are displayed and logged. See :func:`_error` for more
    information.

    :param str exc: Error message to display.
    """
    _error(exc)


def first_line(text):
    """
    Return the first line of a text.

    >>> from confspec.utils import first_line
    >>> text = \"\"\"
    ...
    ...
    ...     The First Line
    ... Second Line
    ...   Third Line
    ... \"\"\"
    >>>
    >>> first_line(text)
    'The First Line'

    :param str text: Any text.
    :rtype: The first line in the text.
    """
    return text.strip().split('\n')[0].strip()
