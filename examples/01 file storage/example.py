"""Example: storing and retrieving file secrets.

Demonstrates how to encrypt and store entire files (certificates,
private keys, configuration files) and retrieve their contents.
"""

import os
import tempfile

from wauth import WAuth


def main() -> None:
    """Run the file storage example."""
    db_path = "example_files.db"
    auth = WAuth(db_path=db_path)

    # Create temporary files to act as our "secrets"
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".pem", delete=False
    ) as cert:
        cert.write("-----BEGIN CERTIFICATE-----\nMIID...")
        cert_path = cert.name

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".key", delete=False
    ) as key_file:
        key_file.write("-----BEGIN RSA PRIVATE KEY-----\nMIIEow...")
        key_path = key_file.name

    # Store files (they get encrypted and saved as binary blobs)
    auth.set_file("SERVER_CERT", cert_path)
    auth.set_file("SERVER_KEY", key_path)

    # Retrieve — returns raw bytes
    cert_data = auth.get("SERVER_CERT")
    key_data = auth.get("SERVER_KEY")

    assert isinstance(cert_data, bytes)
    assert b"BEGIN CERTIFICATE" in cert_data
    assert isinstance(key_data, bytes)
    assert b"BEGIN RSA PRIVATE KEY" in key_data

    print(f"✅ Retrieved certificate: {cert_data[:30]}...")
    print(f"✅ Retrieved key: {key_data[:30]}...")

    # Clean up
    auth.delete("SERVER_CERT")
    auth.delete("SERVER_KEY")
    os.remove(cert_path)
    os.remove(key_path)
    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    main()
