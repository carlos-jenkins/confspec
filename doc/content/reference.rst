.. toctree::

==========================
``confspec`` API Reference
==========================

.. todolist::

.. contents:: Table of Contents
   :local:


User's API Reference
====================

Configuration Manager
---------------------

.. currentmodule:: confspec.manager

.. autosummary::
   :nosignatures:

   ConfigMg

.. autoclass:: ConfigMg
   :members:


Configuration Options
---------------------

.. currentmodule:: confspec.options

.. autosummary::
   :nosignatures:

   ConfigOpt

.. autoclass:: ConfigOpt
   :members:


Validator Functions
-------------------

.. currentmodule:: confspec.validation

.. autosummary::
   :nosignatures:

   endswith
   endswith_igncase
   greater_than
   greater_than_eq
   has_substring
   has_substring_igncase
   in_range
   is_even
   is_odd
   is_one_of
   is_subset_of
   lower_than
   lower_than_eq
   multiple_of
   negative
   positive
   startswith
   startswith_igncase


.. automodule:: confspec.validation
   :members:


Developer's API Reference
=========================

Format Providers
----------------

.. currentmodule:: confspec.providers

.. autosummary::
   :nosignatures:

   FormatProvider
   INIFormatProvider
   JSONFormatProvider
   DictFormatProvider

.. autoclass:: FormatProvider
   :members:

.. autoclass:: INIFormatProvider
   :members:

.. autoclass:: JSONFormatProvider
   :members:

.. autoclass:: DictFormatProvider
   :members:


Utilities
---------

.. currentmodule:: confspec.utils

.. autosummary::
   :nosignatures:

   _error
   error
   first_line

.. automodule:: confspec.utils
   :members:
   :private-members:
