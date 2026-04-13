Frequently Asked Questions (FAQ)
=================================

General Questions
-----------------

What is WAuth?
~~~~~~~~~~~~~~

WAuth is a Python library for storing and retrieving secrets (API keys,
passwords, certificates) encrypted with Fernet (AES-128-CBC), backed by
a local SQLite database. The encryption key is derived from the machine's
unique identifier, making secrets portable only on the machine where they
were created.

Why "machine-locked" encryption?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Machine-locked encryption is a security feature, not a limitation. It
ensures that:

- Secrets cannot be accidentally leaked to another machine
- Each developer has their own encrypted vault
- Production environments use Docker secrets instead

This is ideal for local development and single-node deployments.

What encryption does WAuth use?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WAuth uses **Fernet**, which is built on top of:

- **AES-128-CBC** for encryption
- **HMAC-SHA256** for authentication
- A random 128-bit IV for each encryption operation

The 32-byte Fernet key is derived using **SHA-256** hashing of a salted
machine identifier.

Installation & Setup
---------------------

How do I install WAuth?
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install wpipe

See :doc:`getting-started` for detailed instructions.

Can I use WAuth with Python 3.8?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No. WAuth requires **Python 3.9 or higher** due to its use of modern
type hints (``str | bytes | None`` union syntax) and Pydantic v2.

How do I verify my installation?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python -c "from wauth import WAuth; print('OK')"

Usage Questions
--------------

How do I store a secret?
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from wauth import WAuth
   auth = WAuth()
   auth.set("MY_KEY", "my-secret-value")

Can I store binary data?
~~~~~~~~~~~~~~~~~~~~~~~~

Yes. Use ``set_file()`` to store any binary content:

.. code-block:: python

   auth.set_file("MY_BINARY", "/path/to/file.bin")
   data = auth.get("MY_BINARY")  # Returns bytes

How do I delete a secret?
~~~~~~~~~~~~~~~~~~~~~~~~~

WAuth currently does not expose a delete operation. Secrets are stored
using ``INSERT OR REPLACE`` semantics, so you can overwrite a secret
with an empty value if needed:

.. code-block:: python

   auth.set("OLD_KEY", "")

Where is the database stored?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, at ``~/.wisrovi/wauth.db``. You can specify a custom path:

.. code-block:: python

   auth = WAuth(db_path="/custom/path/secrets.db")

Can I share secrets between machines?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Not directly, due to machine-locked encryption. However, you can:

1. Decrypt the secret on the source machine
2. Transfer it through a secure channel (e.g., ``scp``, password manager)
3. Re-encrypt it on the target machine using ``auth.set()``

For cross-machine secret sharing, use **Docker secrets** or
**environment variables** instead.

Docker Integration
------------------

How does Docker secret support work?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When running inside a Docker container, the ``DriverFactory`` automatically
detects the environment and reads secrets from ``/run/secrets/`` (the
standard Docker secrets path).

How do I set up Docker secrets?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create secret files and reference them in your ``docker-compose.yml``:

.. code-block:: yaml

   secrets:
     my_secret:
       file: ./secrets/my_secret.txt

Docker will mount these as files under ``/run/secrets/``.

Does WAuth write to Docker secrets?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No. Docker secrets are **read-only**. WAuth's ``DriverFactory`` writes
to the local encrypted vault and reads from Docker secrets when available.

Troubleshooting
--------------

Why can't I decrypt a secret on a different machine?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is by design. Secrets are encrypted with a key derived from the
source machine's identifier. They can only be decrypted on that same
machine.

**Solution**: Re-store the secret on the target machine.

What happens if I delete the database file?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All stored secrets are lost. The database will be recreated automatically
on the next ``set()`` call, but it will be empty.

**Recommendation**: Back up your database file if you need to preserve
secrets across reinstall or migration.

Why do I get an empty result from ``get()``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Possible causes:

1. The key does not exist in the database
2. The database path is incorrect
3. The decryption failed (corrupted data) — returns ``None`` for security

**Debugging**: Check that the key exists:

.. code-block:: python

   result = auth.get("MY_KEY")
   if result is None:
       print("Key not found or decryption failed")

How do I migrate from environment variables to WAuth?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Replace ``os.getenv()`` calls with ``auth.get()``:

.. code-block:: python

   # Before
   import os
   db_url = os.getenv("DATABASE_URL")

   # After
   from wauth import WAuth
   auth = WAuth()
   db_url = auth.get("DATABASE_URL")

**Migration script**:

.. code-block:: python

   from wauth import WAuth
   import os

   auth = WAuth()

   # Migrate all env vars to encrypted secrets
   env_vars = ["DATABASE_URL", "REDIS_URL", "API_KEY"]
   for var in env_vars:
       value = os.getenv(var)
       if value:
           auth.set(var, value)
           print(f"Migrated {var}")

Security & Quality
------------------

Is WAuth security audited?
~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes. A Bandit scan shows **0 medium/high severity** findings. All 8
findings are classified as "Low" (informational), related to standard
test patterns and intentional error handling design.

What is the code quality score?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Pylint (wauth/)**: 10.00/10
- **Pylint (test/)**: 9.98/10
- **Test Coverage**: 98%
- **Docstrings**: 100% Google Style
- **Type Hints**: Complete

Where can I report security issues?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please open an issue on the `GitHub repository
<https://github.com/wisrovi/wpipe/issues>`_ or contact the author
directly.
