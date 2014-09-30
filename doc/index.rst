=====================
``confspec`` homepage
=====================

``confspec`` is a Python library - framework that allows an application to
handle all it's configuration options easily and with safety.

With ``confspec`` you don't need to worry about parsing, importing or exporting
configuration files. Nor casting or trying to parse, convert or interpret
datatypes for each option. It will even handle the process to try to identify
if the option is semantically valid and how to react when your options change.

To use ``confspec`` you need to:

#. Define a specification for your options.
#. Create a manager to handle it.
#. Enjoy life. Now you just need to care about reading and changing your
   options. ``confspec`` will take care of reading, parsing, interpreting,
   validating, notifying, writing, exporting, importing, etc.


For the fist step, to create a configuration specification, we create a list
of :class:`confspec.options.ConfigOpt` subclasses:

.. code:: pycon

   >>> from confspec import *
   >>> spec = [
   ...     ConfigInt(key='myint', default=1),
   ...     ConfigBoolean(key='myboolean', default=True),
   ... ]
   >>> spec
   [1, True]


For the second step, we create a :class:`confspec.manager.ConfigMg` manager
object with that specification:

.. code:: pycon

   >>> confmg = ConfigMg(spec)
   >>> confmg.set('myint', 2)
   >>> confmg.get('myint')
   2
   >>> confmg.get('myboolean')
   True


The manager object is the resposible to read from files, write, export, import,
notify, etc when one of your options change.

Finally, enjoy:

.. code:: pycon

   >>> # We now create a proxy object to make setting and
   ... # reading configuration options easier
   ...
   >>> conf = confmg.get_proxy()
   >>> conf.myint
   2
   >>> conf.myint = 3
   >>> conf.myint
   3
   >>> # We can export the current state of the configuration
   ...
   >>> spec[0].comment = 'This is my int!'
   >>> print(confmg.do_export('ini'))
   [general]
   myboolean = True
   ; This is my int!
   myint = 3


As a final demo, we define a validator. Normally you don't set the validator
like this, you use the ``validator`` keyword in the constructor of the
:class:`confspec.options.ConfigOpt`. For a full list of validators check the
:doc:`API Reference <content/reference>`.

.. code:: pycon

   >>> spec[0].validator = is_one_of([1,2,3])
   >>> conf.myint = 4
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "confspec/manager.py", line 341, in __setattr__
       self.__dict__['cfmg'].set(name, value)
     File "confspec/manager.py", line 280, in set
       self._keys[key].value = value
     File "confspec/options.py", line 113, in value
       self._key, parsed
   ValueError: [myint] cannot accept <4>. Could not be validated.
   >>> conf.myint
   3


And much more, much more.  For a more in-depth review check the
`Documentation`_ below.


Features
========

- Type safety for each configuration option.

  - "That option is an int".
  - "That option is a boolean".
  - "That option is a Date".

- Semantic safety for each configuration option.

  - "That option is an odd int".
  - "That option is a positive int".
  - "That option is an int, but it can only be 1, 4 or 7."
  - "That option is a Date, but needs to be between 1920 and 1940."

- Stackable configuration layers:

  - System (default layer, or predefined, with safe values).
  - As many user layers as required (enviroment, user, etc). Options in the top
    layer overrides the one in the bottom.
  - Import multiple configuration files.

- Application wide configuration. You will always have at hand your
  configuration.

- Publisher / listener pattern (callbacks):

  - Know and react when an option is changed.

- Automatic writeback:

  - Always write to the top configuration file the current state of the
    configuration when it changes.

- Safe state:

  - Configuration is always in a safe state. It cannot get corrupted. Options
    will change state only if the new value is validated.

- Multiple Import / Export formats. ``confspec`` can import and export current
  configuration from JSON, INI and Python dicionaries.
  XML, YAML and other could be easily added.

- User defined custom configuration options.

  - Do you want to save a color? Don't worry, you just need to define a new
    configuration options type. (Note: Colors are supported already).

In addition, ``confspec`` is:

- Available for both Python 2.7 and Python 3+.

- Extensively tested. See coverage statistics.

- Continuously checked using Travis CI.


Documentation
=============

.. toctree::
   :maxdepth: 2

   content/tutorial
   content/reference
