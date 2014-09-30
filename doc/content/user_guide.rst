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
   ...     ConfigHexadecimal(key='myhex', default='0xFF'),
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
   ...     ConfigHexadecimal(key='myhex', default='0xEE'),  # See new default
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


Enabling configuration change writeback
+++++++++++++++++++++++++++++++++++++++

Adding and enabling configuration change callbacks
++++++++++++++++++++++++++++++++++++++++++++++++++

Manually exporting configuration to other formats
+++++++++++++++++++++++++++++++++++++++++++++++++

Toggling configuration manager safe mode
++++++++++++++++++++++++++++++++++++++++

Complete example with the basics
++++++++++++++++++++++++++++++++

Intermediate topics
===================

Understanding and using collection options
++++++++++++++++++++++++++++++++++++++++++

Using more advanced configuration options
+++++++++++++++++++++++++++++++++++++++++

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
