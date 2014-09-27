.. toctree::

==========================
``confspec`` API Reference
==========================

.. contents:: Table of Contents
   :local:


User's API Reference
====================

Configuration Manager
+++++++++++++++++++++

.. currentmodule:: confspec.manager

.. autosummary::
   :nosignatures:

   ConfigMg

.. autoclass:: ConfigMg
   :members:


Configuration Options
+++++++++++++++++++++

.. contents:: Categories
   :local:

.. currentmodule:: confspec.options


Base Abstract Class
-------------------

.. autosummary::
   :nosignatures:

   ConfigOpt

.. autoclass:: ConfigOpt
   :members:


Basic Datatypes Options
-----------------------

.. autosummary::
   :nosignatures:

   ConfigString
   ConfigText
   ConfigLine
   ConfigInt
   ConfigDecimal
   ConfigOctal
   ConfigHexadecimal
   ConfigBoolean
   ConfigFloat

.. autoclass:: ConfigString
   :members:

.. autoclass:: ConfigText
   :members:

.. autoclass:: ConfigLine
   :members:

.. autoclass:: ConfigInt
   :members:

.. autoclass:: ConfigDecimal
   :members:

.. autoclass:: ConfigOctal
   :members:

.. autoclass:: ConfigHexadecimal
   :members:

.. autoclass:: ConfigBoolean
   :members:

.. autoclass:: ConfigFloat
   :members:


Time Options
------------

.. autosummary::
   :nosignatures:

   ConfigDateTime
   ConfigDate
   ConfigTime

.. autoclass:: ConfigDateTime
   :members:

.. autoclass:: ConfigDate
   :members:

.. autoclass:: ConfigTime
   :members:


Mapping Options
---------------

.. autosummary::
   :nosignatures:

   ConfigMap
   ConfigClass

.. autoclass:: ConfigMap
   :members:

.. autoclass:: ConfigClass
   :members:


File System Options
-------------------

.. autosummary::
   :nosignatures:

   ConfigPath
   ConfigFile
   ConfigDir

.. autoclass:: ConfigPath
   :members:

.. autoclass:: ConfigFile
   :members:

.. autoclass:: ConfigDir
   :members:


Miscellaneous Options
---------------------

.. autosummary::
   :nosignatures:

   ConfigColor
   ConfigFont

.. autoclass:: ConfigColor
   :members:

.. autoclass:: ConfigFont
   :members:


Collection Options
------------------

.. autosummary::
   :nosignatures:

   ConfigList
   ConfigListString
   ConfigListText
   ConfigListLine
   ConfigListInt
   ConfigListDecimal
   ConfigListOctal
   ConfigListHexadecimal
   ConfigListBoolean
   ConfigListFloat
   ConfigListDateTime
   ConfigListDate
   ConfigListTime
   ConfigListMap
   ConfigListClass
   ConfigListPath
   ConfigListFile
   ConfigListDir
   ConfigListColor
   ConfigListFont

.. autoclass:: ConfigList
   :members:

.. autoclass:: ConfigListString
   :members:

.. autoclass:: ConfigListText
   :members:

.. autoclass:: ConfigListLine
   :members:

.. autoclass:: ConfigListInt
   :members:

.. autoclass:: ConfigListDecimal
   :members:

.. autoclass:: ConfigListOctal
   :members:

.. autoclass:: ConfigListHexadecimal
   :members:

.. autoclass:: ConfigListBoolean
   :members:

.. autoclass:: ConfigListFloat
   :members:

.. autoclass:: ConfigListDateTime
   :members:

.. autoclass:: ConfigListDate
   :members:

.. autoclass:: ConfigListTime
   :members:

.. autoclass:: ConfigListMap
   :members:

.. autoclass:: ConfigListClass
   :members:

.. autoclass:: ConfigListPath
   :members:

.. autoclass:: ConfigListFile
   :members:

.. autoclass:: ConfigListDir
   :members:

.. autoclass:: ConfigListColor
   :members:

.. autoclass:: ConfigListFont
   :members:


Validator Functions
+++++++++++++++++++

.. contents:: Categories
   :local:

.. currentmodule:: confspec.validation


Integer and Float Validation
----------------------------

.. autosummary::
   :nosignatures:

   positive
   negative
   greater_than
   greater_than_eq
   lower_than
   lower_than_eq
   in_range
   multiple_of
   is_even
   is_odd

.. autofunction:: positive

.. autofunction:: negative

.. autofunction:: greater_than

.. autofunction:: greater_than_eq

.. autofunction:: lower_than

.. autofunction:: lower_than_eq

.. autofunction:: in_range

.. autofunction:: multiple_of

.. autofunction:: is_even

.. autofunction:: is_odd


Collection Validation
---------------------

.. autosummary::
   :nosignatures:

   is_one_of
   is_subset_of
   all_validate_to
   empty
   non_empty

.. autofunction:: is_one_of

.. autofunction:: is_subset_of

.. autofunction:: all_validate_to

.. autofunction:: empty

.. autofunction:: non_empty


String Validation
-----------------

.. autosummary::
   :nosignatures:

   has_substring
   has_substring_igncase
   startswith
   startswith_igncase
   endswith
   endswith_igncase

.. autofunction:: has_substring

.. autofunction:: has_substring_igncase

.. autofunction:: startswith

.. autofunction:: startswith_igncase

.. autofunction:: endswith

.. autofunction:: endswith_igncase


Developer's API Reference
=========================

Format Providers
++++++++++++++++

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
+++++++++

.. currentmodule:: confspec.utils

.. autosummary::
   :nosignatures:

   _error
   error
   first_line

.. automodule:: confspec.utils
   :members:
   :private-members:
