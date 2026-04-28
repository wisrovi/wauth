API Reference
=============

This page provides comprehensive documentation for all public classes
and functions in the WAuth library.

Main Interface
--------------

.. autoclass:: wauth.WAuth
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Functional API
--------------

.. autofunction:: wauth.set
.. autofunction:: wauth.set_file
.. autofunction:: wauth.get
.. autofunction:: wauth.valid
.. autofunction:: wauth.delete
.. autofunction:: wauth.list_keys

Verbose Control
---------------

.. autofunction:: wauth.set_verbose
.. autofunction:: wauth.get_verbose

CryptoEngine
------------

.. automodule:: wauth.core
   :members:
   :undoc-members:
   :show-inheritance:

Vault & SecretModel
-------------------

.. automodule:: wauth.vault
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions
----------

.. automodule:: wauth.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

Deprecation Utilities
---------------------

.. automodule:: wauth.deprecation
   :members:
   :undoc-members:
   :show-inheritance:

Utilities
---------

.. automodule:: wauth.utils
   :members:
   :undoc-members:
   :show-inheritance:

Drivers
-------

DriverFactory
~~~~~~~~~~~~~

.. autoclass:: wauth.drivers.DriverFactory
   :members:
   :undoc-members:
   :show-inheritance:

LocalDriver
~~~~~~~~~~~

.. autoclass:: wauth.drivers.local.LocalDriver
   :members:
   :undoc-members:
   :show-inheritance:

DockerDriver
~~~~~~~~~~~~

.. autoclass:: wauth.drivers.docker.DockerDriver
   :members:
   :undoc-members:
   :show-inheritance:
