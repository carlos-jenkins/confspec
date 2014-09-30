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

For a more in-depth documentation visit the project home page at:

   http://confspec.readthedocs.org/


Installation
============

::

   pip install confspec


Development
===========

   https://github.com/carlos-jenkins/confspec

Run code QA:

::

   pip install tox
   tox


Documentation
=============

User guide and API Reference can be found in:

   http://confspec.readthedocs.org/

To build it from source execute:

::

   pip install sphinx sphinx_rtd_theme
   cd doc/
   make html


TODO
====

- Finish (start) to write tutorial and improve documentation.
- Improve Coverage.
- Add to file system ConfigOpt's a ``create`` keyword.


Possible Improvements
=====================

- Add a XML format provider.
- Add a YAML format provider.
- Add a SQLite format provider.
- Add capability for plugins to register custom ``ConfigOption`` subclasses.
- Add integration with ``argparse``.
