Bibliography & Source Resources
================================

This page provides references to external resources, standards, and
technologies used by WAuth.

Encryption Standards
--------------------

Fernet Specification
~~~~~~~~~~~~~~~~~~~~

WAuth uses Fernet as its encryption standard. Fernet is a symmetric
encryption format built on AES-128-CBC with HMAC-SHA256 authentication.

- **Specification**: https://github.com/fernet/spec/blob/master/Spec-v1.md
- **Python Implementation**: https://cryptography.io/en/latest/fernet/
- **Security Properties**: Authenticated encryption, random IV per message

AES-128-CBC
~~~~~~~~~~~

The Advanced Encryption Standard (AES) with 128-bit keys in Cipher Block
Chaining (CBC) mode.

- **NIST Standard**: FIPS 197
- **RFC Reference**: RFC 3602

SHA-256 Key Derivation
~~~~~~~~~~~~~~~~~~~~~~

Encryption keys are derived by hashing a salted machine identifier with
SHA-256.

- **NIST Standard**: FIPS 180-4
- **Python Implementation**: ``hashlib.sha256()``

Technologies
------------

SQLite
~~~~~~

Lightweight, serverless, self-contained SQL database engine used for
persistent secret storage.

- **Website**: https://www.sqlite.org/
- **Python Module**: ``sqlite3`` (standard library)

Pydantic v2
~~~~~~~~~~~

Data validation and settings management using Python type annotations.

- **Documentation**: https://docs.pydantic.dev/latest/
- **GitHub**: https://github.com/pydantic/pydantic

cryptography
~~~~~~~~~~~~

Package designed to expose cryptographic primitives and recipes to
Python developers.

- **Documentation**: https://cryptography.io/
- **GitHub**: https://github.com/pyca/cryptography

wsqlite
~~~~~~~

SQLite ORM with Pydantic integration, used by WAuth for database
operations.

- **PyPI**: https://pypi.org/project/wsqlite/

Code Quality Tools
------------------

Pylint
~~~~~~

Source-code, bug and quality checker for Python.

- **Documentation**: https://pylint.readthedocs.io/
- **Configuration**: See ``pyproject.toml`` in the project root

pytest
~~~~~~

Full-featured Python testing framework.

- **Documentation**: https://docs.pytest.org/
- **Plugin**: pytest-cov for coverage reporting

Black
~~~~~

The uncompromising Python code formatter.

- **Documentation**: https://black.readthedocs.io/
- **Configuration**: ``pyproject.toml`` section ``[tool.black]``

Ruff
~~~~

Extremely fast Python linter, written in Rust.

- **Documentation**: https://docs.astral.sh/ruff/
- **Configuration**: ``pyproject.toml`` section ``[tool.ruff]``

Bandit
~~~~~~

Security linter for Python code.

- **Documentation**: https://bandit.readthedocs.io/
- **Scan Command**: ``bandit -r wauth/``

Documentation Tools
-------------------

Sphinx
~~~~~~

Python documentation generator.

- **Documentation**: https://www.sphinx-doc.org/
- **Theme Used**: Furo (https://github.com/pradyunsg/furo)

reStructuredText
~~~~~~~~~~~~~~~~

Markup syntax used for Python documentation.

- **Quick Reference**: https://docutils.sourceforge.io/docs/user/rst/quickref.html

Best Practices
--------------

Secret Management
~~~~~~~~~~~~~~~~~

- **Never commit secrets to version control**
- **Use environment-specific secret stores** (Docker secrets, HashiCorp Vault)
- **Rotate secrets regularly** and update the encrypted vault
- **Back up the database file** if you need to preserve secrets

Machine-Locked Design
~~~~~~~~~~~~~~~~~~~~~

The machine-locked approach is intentionally restrictive:

1. **Prevents accidental leakage** across environments
2. **Encourages proper secret management** in production (Docker, Vault)
3. **Simplifies local development** without complex setup

For production multi-node deployments, consider:

- `HashiCorp Vault <https://www.vaultproject.io/>`_
- `AWS Secrets Manager <https://aws.amazon.com/secrets-manager/>`_
- `Docker Secrets <https://docs.docker.com/engine/swarm/secrets/>`_

Author
------

**William Rodríguez — wisrovi**  
*Technology Evangelist & Open Source Advocate*

🔗 `LinkedIn <https://es.linkedin.com/in/wisrovi-rodriguez>`_  
🐙 `GitHub <https://github.com/wisrovi>`_
