"""Example: migrating from environment variables to WAuth.

Shows how to transition from os.getenv() patterns to encrypted
secret storage with a migration helper.
"""

import os

from wauth import WAuth


def migrate_from_env(auth: WAuth, variables: list[str]) -> int:
    """Migrate environment variables to encrypted secrets.

    Args:
        auth: WAuth instance to store secrets in.
        variables: List of environment variable names to migrate.

    Returns:
        Number of variables successfully migrated.
    """
    migrated = 0
    for var in variables:
        value = os.environ.get(var)
        if value:
            auth.set(var, value)
            print(f"  ✅ Migrated {var}")
            migrated += 1
        else:
            print(f"  ⚠️  Skipped {var} (not set)")
    return migrated


def main() -> None:
    """Run the migration example."""
    db_path = "example_migration.db"
    auth = WAuth(db_path=db_path)

    print("── Migration from Environment Variables ──\n")

    # Set some env vars for demonstration
    os.environ["DEMO_API_KEY"] = "demo-key-123"
    os.environ["DEMO_DB_URL"] = "postgresql://localhost/demo"

    # Variables to migrate
    variables_to_migrate = [
        "DEMO_API_KEY",
        "DEMO_DB_URL",
        "DEMO_MISSING_VAR",  # This one doesn't exist
    ]

    print("Migrating environment variables to WAuth:")
    count = migrate_from_env(auth, variables_to_migrate)
    print(f"\n📊 Migrated {count}/{len(variables_to_migrate)} variables")

    # Verify migration
    print("\nVerifying migrated secrets:")
    for var in ["DEMO_API_KEY", "DEMO_DB_URL"]:
        value = auth.get(var)
        print(f"  {var}: {value}")

    # Now your code can use auth.get() instead of os.getenv()
    print("\n── Before/After ──")
    print("Before: api_key = os.getenv('DEMO_API_KEY')")
    print("After:  api_key = auth.get('DEMO_API_KEY')")
    print(f"Result: {auth.get('DEMO_API_KEY')}")

    # Clean up
    for key in auth.list_keys():
        auth.delete(key)
    if os.path.exists(db_path):
        os.remove(db_path)
    os.environ.pop("DEMO_API_KEY", None)
    os.environ.pop("DEMO_DB_URL", None)


if __name__ == "__main__":
    main()
