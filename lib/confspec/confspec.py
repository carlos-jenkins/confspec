class ConfigMg(object):

    supported_formats = ['ini', 'json', 'dict']

    def __init__(self, spec, files=tuple(), format='ini',
            create=True, notify=False, writeback=True):

        # Register spec and check uniqueness
        self._spec = spec
        self._keys = {s.key: s for s in spec}
        if len(self._keys) != len(spec):
            raise AttributeError('Keys are not unique.')

        # Register format
        if format not in ConfigMg.supported_formats:
            raise AttributeError('Unknown format \'{}\''.format(format))
        self._format = format

        # Register flags
        self._create = create
        self._notify = notify
        self._writeback = writeback

        # Create map of listeners
        self._listeners = {}
        for key in self._keys.keys():
            self._listeners[key] = []

    def enable_notify(self, enable):
        """
        Enable global notification of configuration changes.
        """
        self._notify = enable

    def enable_writeback(self, enable):
        """
        Enable automatic writeback to file when current configuration changes.
        """
        self._writeback = enable

    def register_listener(self, func, key):
        """
        Register a listener for given key.
        """
        listeners = self._listeners[key]
        if not func in listeners:
            listeners.append(func)
            return True
        return False

    def unregister_listener(self, func, key):
        """
        Unregister a listener for given key.
        """
        listeners = self._listeners[key]
        if func in listeners:
            del listeners.index(func)
            return True
        return False

    def save(self):
        """
        Export current configuration to the top file in the file stack.
        """
        pass

    def load(self):
        """
        Import all files in the file stack.
        """
        pass

    def do_import(self, conf, format='ini'):
        """
        Import - validate a configuration written in a standard format.
        Supported formats: Auto, INI, JSON, Python dict.
        """
        pass

    def do_export(self, format='ini'):
        """
        Export current configuration as a standard format.
        Supported formats: INI, JSON, Python dict.
        """
        pass

    def get(self, key):
        """
        Get a config key.
        """
        pass

    def set(self, key, value):
        """
        Validate and set a config key.
        """
        pass

    def get_proxy(self):
        """
        Return a proxy object for current configuration specification.
        """
        return ConfigProxy(self)


class ConfigProxy(object):
    """
    Proxy object for application configuration.
    """

    def __init__(self, cfmg):
        self.cfmg = cfmg

    def __delattr__(self, name):
        raise TypeError('Cannot delete configuration keys.')

    def __getattr__(self, name):
        if name in self.cfmg.get_keys():
            return self.cfmg.get(name)
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name in self.cfmg.get_keys():
            return self.cfmg.set(name, value)
        raise AttributeError(name)


class ConfigKey(object):

    def __init__(self, key=None, default=None, validator=None):

        # Private attributes
        self._key = None
        self._value = None

        # Validate and set attributes
        self.validator = validator
        self.key = key
        self.value = default

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_key):
        if not isinstance(new_key, str):
            raise ValueError('Key must be a string.')
        if not new_key:
            raise ValueError('String must not be empty.')
        if self._key is not None:
            raise AttributeError('Cannot change key once set.')

        self._key = new_key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, raw):
        parsed = self.parse(raw)
        if self.validator is not None:
            self.validator(parsed)
        self._value = parsed

    def __delattr__(self, name):
        raise TypeError('Cannot delete configuration keys.')

    def parse(self, value):
        raise NotImplementedError()

