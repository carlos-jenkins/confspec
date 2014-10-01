.. toctree::

==========
User Guide
==========

.. contents:: Table of Contents
   :local:

.. warning::

   Work in progress!


Basics
======

Reading and writing configuration files
+++++++++++++++++++++++++++++++++++++++

``confspec`` can handle your configuration files for you. Just specify the list
of files in the ``files`` keyword in the :class:`confspec.manager.ConfigMg`
constructor.

Before going into the code example there is three more keyword you need to know:

:format: The format of your configuration files.
:create: Try to create the configuration files if they don't exists.
:load: Load files immediately.

.. code:: pycon

   >>> from confspec import *
   >>> spec = [
   ...     ConfigFloat(key='myfloat', default=1.0),
   ...     ConfigHexadecimal(key='myhex', default=0xFF),
   ... ]
   >>> # Let's create the manager
   ...
   >>> confmg = ConfigMg(
   ...     spec,
   ...     format='ini',
   ...     create=False,
   ...     load=False,
   ...     files=[
   ...         '/etc/myapp/default.ini',
   ...         '~/.myapp/config.ini'
   ...     ]
   ... )
   >>> # Now let's read the files
   ...
   >>> confmg.load()
   ERROR:root:Traceback (most recent call last):
     File "confspec/manager.py", line 214, in load
       # Import file (if exists, if not, fail - raise)
   IOError: [Errno 2] No such file or directory: '/etc/myapp/default.ini'

   ERROR:root:Traceback (most recent call last):
     File "confspec/manager.py", line 214, in load
       # Import file (if exists, if not, fail - raise)
   IOError: [Errno 2] No such file or directory: '/home/user/.myapp/config.ini'

   >>> # Of course, a bunch of error just got logged
   ... # (no exception raised, we will se why later) because both files do not
   ... # exists.
   ... # We're going to write the current configuration to the last file
   ... # (the user file)
   ...
   >>> confmg.save()
   >>> from os.path import expanduser
   >>> with open(expanduser('~/.myapp/config.ini'), 'r') as cfg:
   ...     print(cfg.read())
   ...
   [general]
   myfloat = 1.0
   myhex = 0xff
   >>> confmg.load()
   ERROR:root:Traceback (most recent call last):
     File "confspec/manager.py", line 214, in load
       # Import file (if exists, if not, fail - raise)
   IOError: [Errno 2] No such file or directory: '/etc/myapp/default.ini'

In our example ``/etc/myapp/default.ini`` doesn't exists. Normally, this is
created or distributed as part of the package or the operating system policy.
The idea begin it is to provide some system defaults (that override in-program
defaults). On top of it there is a user file that holds the user configuration.

Finally, let's see what happens when you change the ``create`` and ``load``
keywords, please do note the changed values in the specification:

.. code:: pycon

   >>> from confspec import *
   >>> spec = [
   ...     ConfigFloat(key='myfloat', default=3.3),  # See new default
   ...     ConfigHexadecimal(key='myhex', default=0xEE),  # See new default
   ... ]
   >>> confmg = ConfigMg(
   ...     spec,
   ...     format='ini',  # Note, this is the default
   ...     create=True,  # Note, this is the default
   ...     load=True,  # Note, this is the default
   ...     files=[
   ...         '/etc/myapp/default.ini',
   ...         '~/.myapp/config.ini'
   ...     ]
   ... )
   ERROR:root:Traceback (most recent call last):
     File "confspec/manager.py", line 208, in load
       if not exists(directory):
     File "/usr/lib/python2.7/os.py", line 157, in makedirs
       mkdir(name, mode)
   OSError: [Errno 13] Permission denied: '/etc/myapp'

   >>> # Note that confspec tried to create the system configuration file, but
   ... # it doesn't have permission to create the folder. But that's ok.
   ...
   >>> confmg
   [general]
   myfloat :: 1.0
   myhex   :: 0xff
   >>> # Note that the current configuration is different from the defaults
   ... # provided in the specification. That's because the user config file
   ... # was loaded.


Validate semantics of your options
++++++++++++++++++++++++++++++++++

The main issue with using Python's :py:class:`configparser.ConfigParser`
exclusively to handle an application configuration is that it only provides
parsing for your option values. There is no semantic validation of the
value. With *semantic validation* I mean that the parsed value makes sense for
the application.

For example, if for whatever reason I have an ``age`` option, we can assume
it's an integer. But does it make sense to have a negative age? Or similarly,
does it make sense to have an age over 9000? No.

Adding the fact that :py:class:`configparser.ConfigParser` only support a
few datatypes:
:py:meth:`configparser.ConfigParser.getint`,
:py:meth:`configparser.ConfigParser.getfloat`,
:py:meth:`configparser.ConfigParser.getboolean`; you will end up doing this:

- Get value as string.
- Parse the value yourself.
- Check if it make sense.

``confspec`` handle all this graciously, in particular, semantic validation
is straightforward, you just need to specify a validation function in the
specification of your options:

.. code:: pycon

   >>> def valid_age(age):
   ...     return age > 1 and age < 110
   ...
   >>> from confspec import *
   >>> spec = [
   ...     ConfigInt(
   ...         key='age',
   ...         default=18,
   ...         validator=valid_age,
   ...     ),
   ... ]
   >>> confmg = ConfigMg(spec)
   >>> confmg
   [general]
   age :: 18
   >>> confmg.set('age', 30)
   >>> confmg
   [general]
   age :: 30
   >>> confmg.set('age', 9000 + 1)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "confspec/manager.py", line 289, in set
       self._keys[key].value = value
     File "confspec/options.py", line 129, in value
       self._key, parsed
   ValueError: [age] cannot accept <9001>. Could not be validated.
   >>> confmg
   [general]
   age :: 30

A validation function is just a function that receives the parsed value and
returns ``True`` if the value is semantically valid, or ``False`` otherwise.

``confspec`` already include a good selection of validation functions in the
:mod:`confspec.validation` module. For a complete list of validation functions
check :doc:`API Reference <reference>`. In our example, we can use the
:func:`confspec.validation.in_range` function instead:

.. code:: pycon

   >>> myvalidator = in_range(1, 110)
   >>> myvalidator(10)
   True

And with it, we can define our specification like this:

.. code:: pycon

   >>> from confspec import *
   >>> spec = [
   ...     ConfigInt(
   ...         key='age',
   ...         default=18,
   ...         validator=in_range(1, 110),
   ...     ),
   ... ]

As you have noted, all ``confspec`` validation function are higher-order
functions, which means that they are functions that returns another function.
This allows to parametrize them. Many of this functions are generic enough
to work with different data types, for example:

.. code:: pycon

   >>> from time import sleep
   >>> from datetime import datetime
   >>> past = datetime.now(); sleep(1)
   >>> present = datetime.now(); sleep(1)
   >>> future = datetime.now(); sleep(1)
   >>> from confspec import *
   >>> f = in_range(past, future)
   >>> f(present)
   True

To implement your own validation functions as higher-order functions check the
section `Writing your own validation functions`_.


Enabling configuration change writeback
+++++++++++++++++++++++++++++++++++++++

Writeback is a feature that updates the user configuration file each time
a configuration option is changed. To enable writeback set the ``writeback``
keyword in the :class:`confspec.manager.ConfigMg` constructor
(the default is ``True``) or change it using
:meth:`confspec.manager.ConfigMg.enable_writeback`.

.. code:: pycon

   >>> from confspec import *
   >>> spec = [
   ...     ConfigText(key='mytxt', default='Default Value'),
   ...     ConfigDate(key='mydate', default='2014-09-30'),
   ... ]
   >>> confmg = ConfigMg(
   ...     spec,
   ...     writeback=True,  # This is the default
   ...     files=['~/.myapp/config.ini']
   ... )
   >>> confmg._files
   ['/home/user/.myapp/config.ini']

We defined a specification and a manager, not let's see what happens when
we change an option:

.. code:: pycon

   >>> def cat(f):
   ...     with open(f, 'r') as fd:
   ...         print(fd.read())
   ...
   >>> cat(confmg._files[0])
   [general]
   mydate = 2014-09-30
   mytxt = Default Value
   >>> conf = confmg.get_proxy()
   >>> conf.mytxt = 'My new value!'
   >>> cat(confmg._files[0])
   [general]
   mydate = 2014-09-30
   mytxt = My new value!

The file is updated each time a configuration option change.

There are a few exceptions to the writeback:

- During file loading using :meth:`confspec.manager.ConfigMg.load`.
- During manual import using :meth:`confspec.manager.ConfigMg.do_import`.

In both situation the writeback is temporarily disabled because in normal
conditions this operations implies that many configuration options will change
(and thus it would trigger many writes to disk). In this situation, if you want
to writeback the changes in the configuration to the user file call
:meth:`confspec.manager.ConfigMg.save` manually after the ``load`` or the
``do_import``.


Adding and enabling configuration change callbacks
++++++++++++++++++++++++++++++++++++++++++++++++++

Configuration change callbacks allows the application to be notified when
a value change. Callbacks are set per configuration key and as many as needed.

This is called a Listener - Publisher design pattern
(Publisher - Subscriber, Observer Pattern, etc, pick one).

Let's start our example creating a specification, a manager and a proxy, like
always:

.. code:: pycon

   >>> from os.path import expanduser
   >>> home = expanduser('~')
   >>> from confspec import *
   >>> spec = [
   ...     ConfigDir(key='myhome', default=home),
   ...     ConfigDateTime(key='mydate', default='2014-09-30T17:40:20'),
   ... ]
   >>> confmg = ConfigMg(spec)
   >>> conf = confmg.get_proxy()

We're going to need a helper function that tell us what time is it in ISO 8601
format (default used by ``confspec`` time configuration options).

.. code:: pycon

   >>> from datetime import datetime
   >>> def now():
   ...     return datetime.now().replace(microsecond=0).isoformat()
   ...
   >>> now()
   '2014-09-30T17:46:38'

Now let's register our change listener, or "callback", and enable
notifications:

.. code:: pycon

   >>> def mycallback(key, old_value, value):
   ...     print('New value for {}: was {}, now it is {}'.format(
   ...         key, old_value, value
   ...     ))
   ...
   >>> confmg.register_listener(mycallback, 'mydate')
   True
   >>> confmg.enable_notify(True)
   >>> conf.mydate
   datetime.datetime(2014, 9, 30, 17, 40, 20)
   >>> conf.mydate = now()
   New value for mydate: was 2014-09-30 18:11:57, now it is 2014-09-30T18:13:38

Note: Instead of using :meth:`confspec.manager.ConfigMg.enable_notify`, you
can set the ``notify`` keywork in the :class:`confspec.manager.ConfigMg`
constructor if you want to enable notification from the beginning.

As a final note beware if you call :meth:`confspec.manager.ConfigMg.load` or
:meth:`confspec.manager.ConfigMg.do_import` when the notifications are enabled,
as they will be triggered for each time a configuration option change.


Manually exporting configuration to other formats
+++++++++++++++++++++++++++++++++++++++++++++++++

You can export your configuration to any of the supported formats:

.. code:: pycon

   >>> from confspec import *
   >>> ConfigMg.supported_formats
   ['json', 'dict', 'ini']

Let's start our example creating a specification and a manager, like
always:

.. code:: pycon

   >>> from confspec import *
   >>> spec = [
   ...     ConfigTime(key='mytime', default='17:40:20'),
   ...     ConfigDate(key='mydate', default='2014-09-30'),
   ... ]
   >>> confmg = ConfigMg(spec)

Now, you just need to call the method
:meth:`confspec.manager.ConfigMg.do_export`:

.. code:: pycon

   >>> confmg
   [general]
   mydate :: 2014-09-30
   mytime :: 17:40:20
   >>> print(confmg.do_export())
   [general]
   mydate = 2014-09-30
   mytime = 17:40:20

   >>> print(confmg.do_export(format='ini'))
   [general]
   mydate = 2014-09-30
   mytime = 17:40:20

   >>> print(confmg.do_export(format='json'))
   {
       "general": {
           "mydate": "2014-09-30",
           "mytime": "17:40:20"
       }
   }
   >>> print(confmg.do_export(format='dict'))
   {'general': {'mydate': '2014-09-30', 'mytime': '17:40:20'}}

Note: As you may have noted, the representation of the ``ConfigMg`` object is
actually the configuration exported in a pseudo-INI-inspired format.

In a similar way, you can import configuration using the
:meth:`confspec.manager.ConfigMg.do_import` method, providing the formatted
string with the configuration and the format.


Group configuration options in categories
+++++++++++++++++++++++++++++++++++++++++

Complete example with the basics
++++++++++++++++++++++++++++++++

Intermediate topics
===================

Understanding and using collection options
++++++++++++++++++++++++++++++++++++++++++

Using more advanced configuration options
+++++++++++++++++++++++++++++++++++++++++

Toggling configuration manager safe mode
++++++++++++++++++++++++++++++++++++++++


Advanced topics
===============

Writing your own validation functions
+++++++++++++++++++++++++++++++++++++

Defining a new option type
++++++++++++++++++++++++++

Creating a new collection type based on previous option
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

Writing you own format provider (import and export configuration)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
