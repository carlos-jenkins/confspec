========
confspec
========

.. image:: https://pypip.in/py_versions/confspec/badge.png
   :target: https://pypi.python.org/pypi/confspec/
   :alt: Supported Python versions

.. image:: https://pypip.in/version/confspec/badge.png?text=version
   :target: https://pypi.python.org/pypi/confspec/
   :alt: Latest Version

.. image:: https://pypip.in/download/confspec/badge.png
   :target: https://pypi.python.org/pypi/confspec/
   :alt: Downloads

.. image:: https://pypip.in/license/confspec/badge.png
   :target: https://pypi.python.org/pypi/confspec/
   :alt: License

.. image:: https://pypip.in/status/confspec/badge.png
   :target: https://pypi.python.org/pypi/confspec/
   :alt: Status

.. image:: https://travis-ci.org/carlos-jenkins/confspec.svg?branch=master
   :target: https://travis-ci.org/carlos-jenkins/confspec
   :alt: Continuous Integration

.. image:: https://coveralls.io/repos/carlos-jenkins/confspec/badge.png
   :target: https://coveralls.io/r/carlos-jenkins/confspec
   :alt: Coverage


About
=====

``confspec`` is a Python library / framework that allows an application to
handle all it's configuration options easily and with safety.

With ``confspec`` you don't need to worry about parsing files, casting or
trying to parse / convert / interpret datatypes, try to identify if the option
is semantically valid and how to react when your options change.

``confspec`` could be understood as a ``ConfigParser`` with steroids, because
it provides:

- Type safety for each configuration option.

  - "That option is an int".
  - "That option is a boolean".
  - "That option is a Date".

- Semantic safety for each configuration option.

  - "That option is a odd int".
  - "That option is a positive int".
  - "That option is a int, but it can only be 1, 4 or 7."
  - "That option is a Data, but needs to be between 1920 and 1940."

- Stackable configuration layers:

  - System (default layer, or predefined, with safe values).
  - as many user layers as required (enviroment, user, etc). Options in the top
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

You just need to write the configuration specification for you application and
``confspec`` will handle everything.


Installation
============

::

    pip install confspec


Documentation
=============

User guide and API Reference can be found in:

    http://confspec.readthedocs.org/

To build it from source execute:

::

    pip install sphinx
    cd doc/
    make html


Development
===========

    https://github.com/carlos-jenkins/confspec

Run code QA:

::

    pip install tox
    tox


TODO
====

- Write user guide, more documentation and tutorial.
- Improve Coverage.


Possible Improvements
=====================

- Add a XML format provider.
- Add a YAML format provider.
- Add capability to define a list of validation functions for each
  ``ConfigOption``.
- Add capability for plugins to register custom ``ConfigOption`` subclasses.
- Add integration with ``argparse``.

