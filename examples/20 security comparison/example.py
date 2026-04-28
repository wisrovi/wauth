"""Example 20: Comparing get() vs valid() for security.

Demonstrates why valid() is more secure when you only need to verify.
"""

from wauth import WAuth
import os

DB_PATH_DISK = "example_security.db"

def main() -> None:
    """Show security difference between get() and valid()."""
    auth = WAuth(db_path=DB_PATH_DISK)

    # Store a secret
    API_KEY = "sk-12345-secret-api-key"
    auth.set("API_KEY", API_KEY)
    print("Secret stored: API_KEY = 'sk-12345-secret-api-key'")
    print("-" * 60)

    # METHOD 1: Using get() - LESS SECURE
    print("\n1. Using get() to verify:")
    retrieved = auth.get("API_KEY")
    user_input = "sk-12345-secret-api-key"
    
    if retrieved == user_input:  # Secret is now in 'retrieved' variable
        print(f"   Access granted")
        print(f"   [!] Secret exposed in variable: {retrieved[:10]}...")
        print(f"   [!] Secret could be logged, printed, or leaked")
    
    # METHOD 2: Using valid() - MORE SECURE
    print("\n2. Using valid() to verify:")
    user_input = "sk-12345-secret-api-key"
    
    if auth.valid("API_KEY", user_input):  # Secret stays inside wauth
        print(f"   Access granted")
        print(f"   [✓] Secret NEVER left the wauth library")
        print(f"   [✓] Only True/False was returned")
    
    # Demonstrate with wrong value
    print("\n3. Using valid() with wrong value:")
    if not auth.valid("API_KEY", "wrong-value"):
        print("   Access denied (as expected)")
        print("   [✓] No information about the actual secret was exposed")

    print("\n" + "=" * 60)
    print("SECURITY RECOMMENDATION:")
    print("  - Use get() only when you NEED the actual secret value")
    print("  - Use valid() when you only need to CHECK/VERIFY a value")
    print("  - valid() uses constant-time comparison (timing attack safe)")
    print("=" * 60)

    # Cleanup
    if os.path.exists(DB_PATH_DISK):
        os.remove(DB_PATH_DISK)

if __name__ == "__main__":
    main()
