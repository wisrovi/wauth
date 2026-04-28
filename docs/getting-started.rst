Getting Started
===============

This guide will walk you through installing WAuth and storing your first
encrypted secret in under 5 minutes.

Installation
------------

From PyPI
~~~~~~~~~

The recommended way to install WAuth is from PyPI:

.. code-block:: bash

   pip install wpipe

From Source
~~~~~~~~~~~

To install the latest development version:

.. code-block:: bash

   git clone https://github.com/wisrovi/wpipe.git
   cd wpipe
   python -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev,docs]"

Verifying Installation
----------------------

Test that the installation works correctly:

.. code-block:: python

   >>> from wauth import WAuth
   >>> print("WAuth installed successfully!")
   WAuth installed successfully!

Your First Encrypted Secret
---------------------------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from wauth import WAuth

   # 1. Initialize WAuth (creates database at ~/.wisrovi/wauth.db)
   auth = WAuth()

   # 2. Store a secret — it's automatically encrypted with Fernet (AES-128-CBC)
   auth.set("DATABASE_URL", "postgresql://user:pass@localhost/mydb")

   # 3. Retrieve the secret — it's automatically decrypted
   db_url = auth.get("DATABASE_URL")
   print(db_url)  # postgresql://user:pass@localhost/mydb

Using a Custom Database Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from wauth import WAuth

   # Use a custom path for the secrets database
   auth = WAuth(db_path="/path/to/my_secrets.db")
   auth.set("API_KEY", "my-api-key")
   print(auth.get("API_KEY"))

Storing Files
~~~~~~~~~~~~~

WAuth can also encrypt and store entire files:

.. code-block:: python

   from wauth import WAuth

   auth = WAuth()

   # Store a TLS certificate
   auth.set_file("MY_CERT", "/etc/ssl/certs/my-cert.pem")

   # Retrieve the file contents as bytes
   cert_data = auth.get("MY_CERT")
   # cert_data is now the decrypted bytes of the original file

Functional API
~~~~~~~~~~~~~~

For simple scripts, you can use the module-level functions without
instantiating a class:

.. code-block:: python

   from wauth import set, get, set_file, delete, list_keys

   # Store and retrieve
   set("MY_TOKEN", "abc123")
   token = get("MY_TOKEN")

   # Delete when done
   delete("MY_TOKEN")

Understanding Machine-Locked Encryption
----------------------------------------

WAuth uses a **machine-locked** encryption approach:

1. **Machine Identification**: A unique identifier is derived from your machine
   (using ``/etc/machine-id`` on Linux, UUID on Windows, IOPlatformUUID on macOS)

2. **Key Derivation**: The machine ID is hashed with SHA-256 and a salt to produce
   a 32-byte encryption key

3. **Encryption**: The key is used with Fernet (AES-128-CBC) to encrypt secrets

**Important**: Secrets encrypted on one machine **cannot** be decrypted on a
different machine. This is intentional — it prevents accidental secret leakage
across environments.

LTS Features Quick Reference
----------------------------

Time-To-Live (TTL)
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   auth.set("SESSION_TOKEN", "temp-value", ttl=3600)  # Expires in 1 hour

Key Rotation
~~~~~~~~~~~~

.. code-block:: python

   results = auth.rotate_key("new-encryption-key")
   # {"KEY1": True, "KEY2": True}

Backup & Restore
~~~~~~~~~~~~~~~~

.. code-block:: python

   auth.backup("vault_backup.wauth")   # Export
   auth.restore("vault_backup.wauth")  # Import

Async Support
~~~~~~~~~~~~~

.. code-block:: python

   import asyncio

   async def main():
       auth = WAuth()
       await auth.async_set("KEY", "value")
       value = await auth.async_get("KEY")

    asyncio.run(main())

Secure Secret Verification
~~~~~~~~~~~~~~~~~~~~~~~~~

When you only need to check if a value matches a stored secret, use ``valid()`` instead of ``get()``:

.. code-block:: python

    from wauth import WAuth

    auth = WAuth()
    auth.set("API_KEY", "secret123")

    # LESS SECURE: Using get() exposes the secret
    # api_key = auth.get("API_KEY")  # DON'T DO THIS
    # if api_key == user_input:  # Secret is now in memory

    # MORE SECURE: Using valid() never exposes the secret
    user_input = input("Enter API key: ")
    if auth.valid("API_KEY", user_input):
        print("Access granted")
    else:
        print("Access denied")
    # The secret never leaves the wauth library

The ``valid()`` method:
- Uses constant-time comparison to prevent timing attacks
- Never returns or exposes the actual secret
- Only returns ``True`` or ``False``

Async Secret Verification
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from wauth import WAuth

    async def main():
        auth = WAuth()
        auth.set("API_KEY", "secret123")
        
        user_input = input("Enter API key: ")
        if await auth.async_valid("API_KEY", user_input):
            print("Access granted")

    asyncio.run(main())

Verbose Logging
~~~~~~~~~~~~~~~

.. code-block:: python

   from wauth import WAuth, set_verbose

   # Enable diagnostic logging
   set_verbose(True)

   # Or per-instance
   auth = WAuth(verbose=True)

Custom Exceptions
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from wauth.exceptions import DecryptionError, KeyNotFoundError

   try:
       value = auth.get("MISSING")
   except KeyNotFoundError:
       print("Key does not exist")

Configuration File
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   auth = WAuth(config_path="~/.wauth.toml")

Next Steps
----------

- Read the :doc:`api` for complete API documentation
- Follow the :doc:`tutorials` for advanced use cases
- Check the :doc:`faq` for common questions
