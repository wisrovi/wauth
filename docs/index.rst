WAuth Documentation
===================

**Machine-Locked Encrypted Secret Management for Python**

.. image:: https://img.shields.io/pypi/v/wpipe.svg
   :target: https://pypi.org/project/wpipe/
   :alt: PyPI version

.. image:: https://img.shields.io/badge/pylint-10.00%2F10-brightgreen.svg
   :alt: Pylint Score

.. image:: https://img.shields.io/badge/coverage-98%25-brightgreen.svg
   :alt: Test Coverage

Welcome to the official documentation for **WAuth**, a Python library that provides
simple, secure, machine-locked secret storage using Fernet encryption and SQLite.

.. grid:: 2

   .. grid-item-card:: 🚀 Getting Started
      :link: getting-started
      :link-type: doc

      New to WAuth? Start here with installation, setup, and your first encrypted secret.

   .. grid-item-card:: 📚 API Reference
      :link: api
      :link-type: doc

      Complete API documentation with classes, methods, and type signatures.

   .. grid-item-card:: 📖 Tutorials
      :link: tutorials
      :link-type: doc

      Step-by-step guides for common use cases including Docker integration.

   .. grid-item-card:: ❓ FAQ
      :link: faq
      :link-type: doc

      Frequently asked questions and troubleshooting guide.

Key Features
------------

- **Fernet Encryption**: AES-128-CBC encryption with machine-derived keys
- **SQLite Persistence**: Automatic secret storage in a local SQLite database
- **Docker Support**: Read Docker Swarm/Compose secrets from ``/run/secrets``
- **File Storage**: Store and retrieve encrypted files (certificates, keys)
- **Type Safe**: Full type hints and Pydantic validation
- **Zero Config**: Works out of the box with sensible defaults

Quick Example
-------------

.. code-block:: python

   from wauth import WAuth

   # Initialize
   auth = WAuth()

   # Store a secret (automatically encrypted with machine-locked key)
   auth.set("API_KEY", "sk-12345")

   # Retrieve the secret (automatically decrypted)
   key = auth.get("API_KEY")
   print(key)  # sk-12345

.. toctree::
   :maxdepth: 2
   :caption: Contents

   getting-started
   api
   tutorials
   faq
   resources

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
