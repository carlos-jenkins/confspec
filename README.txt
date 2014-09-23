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

- Stackable configuration layers:

 - System (default layer, or predefined, with safe values).
 - N user layers (enviroment, user... the top one overrides the lower).
 - Import multiple configuration files.

- Application wide configuration. You will always have at hand your
  configuration.

- Publisher / listener pattern:

 - Know and react when an option is changed.

- Configuration changed callbacks:

 - Always write to configuration files when the configuration changed in the
   program.

- Save state:

 - Configuration is always in a save state. I cannot get corrupted. Options
   will change state only if the new value is validated.

- Multiple Import / Export formats. ``confspec`` can import from JSON, INI and
  Python dicionaries. XML, YAML and other could be easily added.

You just need to write the configuration specification for you application and
``confspec`` will handle everything.


Installation
============

::

    sudo pip install confspec


Documentation
=============

User guide and API Reference can be found in:

    http://confspec.readthedocs.org/

To build it from source execute:

::

    sudo pip install sphinx
    cd doc/
    make html


Development
===========

    https://github.com/carlos-jenkins/confspec

Run code QA:

::

    sudo pip install flake8
    python setup.py flake8


TODO
====

- Write user guide, more documentation and tutorial.
- Add test suite.
- Setup Continuous Integration for that test suite.
- Setup CI to test all supported Python versions.
- Add capability to define a list of validation functions for each ConfigOption.
- Add capability for plugins to register ConfigOptions.
