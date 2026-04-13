Tutorials
=========

Step-by-step guides for common WAuth use cases.

Tutorial 1: Local Development Secrets
--------------------------------------

**Scenario**: You're developing a local application and need to store
API keys, database credentials, and service tokens securely.

.. code-block:: python

   from wauth import WAuth

   # Step 1: Initialize
   auth = WAuth()

   # Step 2: Store multiple secrets
   auth.set("DATABASE_URL", "postgresql://localhost:5432/myapp")
   auth.set("REDIS_URL", "redis://localhost:6379")
   auth.set("JWT_SECRET", "super-secret-jwt-key")

   # Step 3: Retrieve when needed
   db_url = auth.get("DATABASE_URL")
   redis_url = auth.get("REDIS_URL")

   # Step 4: Use in your application
   # import psycopg2
   # conn = psycopg2.connect(db_url)

**Why this works well**: Each developer on the team has their own encrypted
vault on their machine. No shared secrets files, no environment variables
to configure.

Tutorial 2: Storing TLS Certificates
-------------------------------------

**Scenario**: You need to store TLS certificates and private keys securely
for a web server.

.. code-block:: python

   from wauth import WAuth

   auth = WAuth()

   # Store certificate files
   auth.set_file("TLS_CERT", "/etc/letsencrypt/live/example.com/cert.pem")
   auth.set_file("TLS_KEY", "/etc/letsencrypt/live/example.com/privkey.pem")

   # Later, when starting the server
   cert_data = auth.get("TLS_CERT")
   key_data = auth.get("TLS_KEY")

   # Write to temporary files for the server
   import tempfile
   with tempfile.NamedTemporaryFile(suffix=".pem", delete=False) as f:
       f.write(cert_data)
       cert_path = f.name

   # Use cert_path with your server configuration

**Security benefit**: Certificates are encrypted at rest and only decrypted
when needed by the running process.

Tutorial 3: Docker Container Secrets
--------------------------------------

**Scenario**: Your application runs in Docker and needs to read secrets
injected by Docker Swarm or Docker Compose.

Docker Compose Setup
~~~~~~~~~~~~~~~~~~~~

Create a ``docker-compose.yml``:

.. code-block:: yaml

   version: "3.8"
   services:
     app:
       image: myapp:latest
       secrets:
         - db_password
         - api_key

   secrets:
     db_password:
       file: ./secrets/db_password.txt
     api_key:
       file: ./secrets/api_key.txt

Application Code
~~~~~~~~~~~~~~~~

.. code-block:: python

   from wauth.drivers import DriverFactory

   # DriverFactory automatically tries Docker secrets first
   factory = DriverFactory()

   # This reads from /run/secrets/db_password in the container
   db_pass = factory.get_value("db_password")

   # Falls back to local vault if not in Docker
   api_key = factory.get_value("api_key")

**How it works**: Inside a Docker container, ``DriverFactory`` detects the
Docker environment (via ``/.dockerenv``) and reads from ``/run/secrets/``.
Outside Docker, it falls back to the local encrypted vault.

Tutorial 4: Hybrid Local + Production Setup
---------------------------------------------

**Scenario**: During development you use local encrypted secrets, but in
production you use Docker secrets.

.. code-block:: python

   import os
   from wauth import WAuth
   from wauth.drivers import DriverFactory

   def get_secret(key: str) -> str | None:
       """Get a secret from the appropriate source."""
       if os.getenv("DOCKER_CONTAINER"):
           # In production Docker container
           factory = DriverFactory()
           return factory.get_value(key)
       else:
           # Local development
           auth = WAuth()
           return auth.get(key)

   # Usage — same API in both environments
   db_password = get_secret("DB_PASSWORD")
   api_key = get_secret("API_KEY")

**Benefit**: Same code works in both environments. No environment-specific
branching in your business logic.

Tutorial 5: Database Migration
-------------------------------

**Scenario**: You want to move your secrets database to a different location.

.. code-block:: python

   from wauth import WAuth
   import shutil

   # Old database location
   old_auth = WAuth(db_path="~/.wisrovi/wauth.db")

   # New database location
   new_auth = WAuth(db_path="/new/path/secrets.db")

   # Note: Because encryption is machine-locked, you cannot simply copy
   # the database. You need to re-encrypt on the target machine:

   # On the OLD machine:
   # key_value = old_auth.get("MY_KEY")
   # Save key_value to a secure temporary location

   # On the NEW machine:
   # new_auth.set("MY_KEY", key_value_from_old_machine)

**Important reminder**: Machine-locked encryption means databases are
not portable across machines by design.
