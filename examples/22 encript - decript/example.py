"""Example 22: Direct Encryption and Decryption (Strings & Dicts).

This example demonstrates how to use WAuth's underlying encryption logic
directly to encrypt and decrypt data on-the-fly, including automatic
JSON serialization for dictionaries.
"""

import os
from wauth import WAuth

# Constants for the example
DB_PATH: str = "example_encryption.db"
CUSTOM_KEY: str = "temporary-secret-key-123"


def main() -> None:
    """Run the encryption/decryption proof of concept."""
    auth = WAuth(db_path=DB_PATH, custom_key=CUSTOM_KEY)

    print("── Part 1: String Encryption ──")
    text_data: str = "Sensitive plain text"
    encrypted_text: str = auth.encrypt(text_data)
    decrypted_text: str = auth.decrypt(encrypted_text)
    
    print(f"📄 Original: {text_data}")
    print(f"🔒 Encrypted: {encrypted_text[:40]}...")
    print(f"🔓 Decrypted: {decrypted_text}")
    print(f"✅ Match: {text_data == decrypted_text}\n")

    print("── Part 2: Dictionary (JSON) Encryption ──")
    dict_data = {
        "user_id": 12345,
        "role": "administrator",
        "permissions": ["read", "write", "execute"],
        "active": True
    }
    
    # Dictionaries are automatically serialized to JSON before encryption
    encrypted_dict: str = auth.encrypt(dict_data)
    
    # Dictionaries are automatically deserialized back to dict during decryption
    decrypted_dict = auth.decrypt(encrypted_dict)
    
    print(f"📦 Original Dict: {dict_data}")
    print(f"🔒 Encrypted Token: {encrypted_dict[:40]}...")
    print(f"🔓 Decrypted Result Type: {type(decrypted_dict)}")
    print(f"🔓 Decrypted Result: {decrypted_dict}")
    print(f"✅ Match: {dict_data == decrypted_dict}\n")

    # Cleanup
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    print("🧹 Cleanup complete")


if __name__ == "__main__":
    main()
