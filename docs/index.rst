WAuth Documentation
===================

**Machine-Locked Encrypted Secret Management for Python**

.. image:: https://img.shields.io/pypi/v/wauth.svg
   :target: https://pypi.org/project/wauth/
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

External Links
--------------

- 📦 **PyPI**: https://pypi.org/project/wauth/
- 🐙 **GitHub**: https://github.com/wisrovi/wauth
- 🌐 **GitHub Pages**: https://wisrovi.github.io/wauth/

Integration: WPipe
------------------

Combine **WAuth** with **WPipe** for powerful stateful pipelines with secure secret management.

.. grid:: 2

   .. grid-item-card:: 🔐 WAuth + WPipe Pipeline
      :link: tutorials
      :link-type: doc

      Build secure access control pipelines using WAuth for secrets
      and WPipe for workflow orchestration.

   .. grid-item-card:: 🚀 WPipe (PyPI)
      :link: https://pypi.org/project/wpipe/
      :link-type: url

      WPipe is a Python library for building stateful pipelines with
      conditional logic, tracking, and persistence.

**Example**: Access control pipeline using both libraries:

.. code-block:: python

   from wauth import WAuth
   from wpipe import Pipeline, Condition, state

   # Store secrets with WAuth
   auth = WAuth(db_path="secrets.db", custom_key="my-key")
   auth.set("USER_PASSWORD", "secure-pass")

   # Use in WPipe pipeline
   @state(name="authenticate")
   def authenticate(credentials):
       auth = WAuth(db_path="secrets.db", custom_key="my-key")
       real_pass = auth.get("USER_PASSWORD")
       return {"access_granted": credentials.secret == real_pass}

   pipeline = Pipeline(pipeline_name="access_control")
   pipeline.set_steps([authenticate, Condition(...)])

See :doc:`tutorials` for the full example.

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
