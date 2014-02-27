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

from os import makedirs
from os.path import isfile, exists, expanduser, abspath, dirname

from .utils import error
from .providers import providers


class ConfigMg(object):
    """
    Configuration manager object.

    :param spec: List of instances of subclasses of
     :class:`confspec.options.ConfigOpt`.

    :param files: A list of paths to configuration files. Files are read in the
     given order. The last file is considered the user file. Example:
     ``['/etc/myapp.conf', '~/.myapp/myapp.conf']``

    :param format: The format to export to and import from. Supported formats
     are given by :attr:`ConfigMg.supported_formats`.

    :param bool create: If a file in ``files`` doesn't exists, try to
     create it with the current configuration state exported using the format
     specified by ``format``. Note that if ``safe`` is not enabled and the file
     cannot be created (in case of insufficient permissions, for example) then
     an exception will be raised.

    :param bool notify: Enable notification of configuration changes to the
     registered listeners. Unless required, it is recommended to leave disabled
     this option when configuration files are being imported, and enable it
     later using :meth:`enable_notify`.

    :param bool writeback: Enable writeback mechanism that calls :meth:`save`
     when the user changes the state of the configuration. This setting is
     ignored by :meth:`do_import` so importing (and thus altering the state of
     the configuration) doesn't trigger a file write for each key value change.
     This feature can be enabled or disabled at any time using
     :meth:`enable_writeback`.

    :param bool safe: Enable safe mode. When safe mode is enabled all
     exceptions happening within all methods are written to
     :py:obj:`sys.stderr` instead of raised. Exceptions can happen when a file
     cannot be created, when a file cannot be imported (no read permissions,
     parse error) or when notifying a listener about a option change, among
     others. This feature can be enabled or disabled at any time using
     :meth:`enable_safe`.

    :param bool load: Automatically call :meth:`load` when the configuration
     manager is created.
    """

    supported_formats = providers.keys()
    """
    Supported format to export configuration held by the configuration manager.
    """

    def __init__(
            self, spec, files=tuple(), format='ini',
            create=True, notify=False, writeback=True, safe=True, load=True):

        # Register spec and check uniqueness
        self._spec = spec
        self._keys = {s.key: s for s in spec}
        if len(self._keys) != len(spec):
            raise AttributeError('Keys are not unique.')

        # Register file stack
        self._files = [abspath(expanduser(f)) for f in files]

        # Register format
        if format not in ConfigMg.supported_formats:
            raise AttributeError('Unknown format \'{}\''.format(format))
        self._format = format

        # Register flags
        self._create = create
        self._notify = notify
        self._writeback = writeback
        self._safe = safe

        # Create map of listeners
        self._listeners = {}

        # Create categories map
        self._categories = {}
        for s in self._spec:
            if s.category in self._categories:
                self._categories[s.category].append(s)
            else:
                self._categories[s.category] = [s]

        # Create proxy
        self._proxy = ConfigProxy(self)

        # Load configuration files
        if load:
            self.load()

    def enable_notify(self, enable):
        """
        Enable global notification of configuration changes.
        See :class:`ConfigMg`.
        """
        self._notify = enable

    def enable_writeback(self, enable):
        """
        Enable automatic writeback to file when current configuration changes.
        See :class:`ConfigMg`.
        """
        self._writeback = enable

    def enable_safe(self, enable):
        """
        Enable safe mode. See :class:`ConfigMg`.
        """
        self._safe = enable

    def register_listener(self, func, key):
        """
        Register a listener for given key.
        """
        if func is None or not hasattr(func, '__call__'):
            return False

        if not key in self._listeners:
            self._listeners[key] = []

        listeners = self._listeners[key]
        if not func in listeners:
            listeners.append(func)
            return True
        return False

    def unregister_listener(self, func, key):
        """
        Unregister a listener previously registered for the given key.
        """
        if not key in self._listeners:
            return False

        listeners = self._listeners[key]
        if func in listeners:
            del listeners[listeners.index(func)]
            return True
        return False

    def save(self):
        """
        Export current configuration and write it to the last file in the
        file stack.
        """
        if len(self._files) > 0:
            try:
                with open(self._files[-1], 'w') as f:
                    f.write(self.do_export(format=self._format))
            except Exception as e:
                if not self._safe:
                    raise e
                else:
                    error()

    def load(self):
        """
        Import all files in the file stack.
        """
        for fn in self._files:
            try:
                # Ignore directories
                if exists(fn) and not isfile(fn):
                    raise Exception(
                        'Cannot import non-file "{}".'.format(fn)
                    )

                # Create file if requested and file doesn't exists
                if not exists(fn) and self._create:
                    directory = dirname(fn)
                    if not exists(directory):
                        makedirs(directory)
                    with open(fn, 'w') as f:
                        f.write(self.do_export())
                    continue

                # Import file if exists
                with open(fn, 'r') as f:
                    self.do_import(f.read())

            except Exception as e:
                if not self._safe:
                    raise e
                else:
                    error()

    def do_import(self, conf, format=None):
        """
        Import and validate a configuration written in a standard format.

        :param str conf: A string with a configuration encoded in the specified
         format.
        :param format: See :attr:`ConfigMg.supported_formats`.
         If ``None`` (the default) the format specified in the constructor is
         used.
        :type format: str or None
        """
        if format is None:
            format = self._format

        # Disable write back
        writeback = self._writeback
        self._writeback = False

        # Try to import
        try:
            providers[format].do_import(self, conf)
        finally:
            # Restore writeback setting
            self._writeback = writeback

    def do_export(self, format=None):
        """
        Export current configuration as a standard format.

        :param format: See :attr:`ConfigMg.supported_formats`.
         If ``None`` (the default) the format specified in the constructor is
         used.
        :type format: str or None
        :rtype: A string with the configuration encoded in the specified
         format.
        """
        if format is None:
            format = self._format

        return providers[format].do_export(self)

    def get(self, key):
        """
        Get the value of a config key.
        """
        return self._keys[key].value

    def set(self, key, value):
        """
        Validate and set a config key.
        """
        # Get old value and compare
        old_value = self.get(key)
        if value == old_value:
            return

        # Set and validate new value
        self._keys[key].value = value

        # Writeback if enabled
        if self._writeback:
            self.save()

        # Notify all listeners of the change
        if self._notify:
            for listener in self._listeners[keys]:
                try:
                    listener(key, old_value, value)
                except Exception as e:
                    if not self._safe:
                        raise e
                    else:
                        error()

    def get_proxy(self):
        """
        Return a proxy object for current configuration specification.
        """
        return self._proxy

    def __str__(self):
        return repr(self)

    def __repr__(self):

        # Largest key
        key_len = max(map(len, [opt.key for opt in self._spec]))
        key_format = '{{:<{}}} :: {{}}'.format(key_len)

        result = []
        categories = self._categories
        for category in sorted(categories):
            options = sorted(categories[category])
            result.append('[{}]'.format(category))
            for option in options:
                result.append(
                    key_format.format(option.key, option.repr())
                )
        return '\n'.join(result)


class ConfigProxy(object):
    """
    Proxy object for application configuration.
    """

    def __init__(self, cfmg):
        self.__dict__['cfmg'] = cfmg

    def __delattr__(self, name):
        raise TypeError('Cannot delete configuration keys.')

    def __getattr__(self, name):
        return self.__dict__['cfmg'].get(name)

    def __setattr__(self, name, value):
        self.__dict__['cfmg'].set(name, value)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return repr(self.__dict__['cfmg'])
