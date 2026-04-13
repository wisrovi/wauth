"""Example: CI/CD pipeline integration.

Demonstrates how WAuth manages secrets in automated pipelines,
including build tokens, deployment credentials, and notifications.
"""

import os

from wauth import WAuth


def main() -> None:
    """Run the CI/CD pipeline example."""
    db_path = "example_cicd.db"
    auth = WAuth(db_path=db_path, custom_key="pipeline-key-2024")

    print("── CI/CD Pipeline Secrets ──\n")

    # ── Build stage ──
    print("🔨 Build Stage:")
    auth.set("NPM_TOKEN", "npm_12345abcde")
    auth.set("DOCKER_REGISTRY", "registry.example.com")
    print("   ✅ NPM_TOKEN stored")
    print("   ✅ DOCKER_REGISTRY stored\n")

    # ── Test stage ──
    print("🧪 Test Stage:")
    auth.set("TEST_DB_URL", "postgresql://test:test@localhost/test_db")
    auth.set("TEST_API_KEY", "test-key-expire-soon", ttl=7200)  # 2 hours
    print("   ✅ TEST_DB_URL stored")
    print("   ✅ TEST_API_KEY stored (2h TTL)\n")

    # ── Deploy stage ──
    print("🚀 Deploy Stage:")
    auth.set("AWS_ACCESS_KEY", "AKIAIOSFODNN7EXAMPLE")
    auth.set("AWS_SECRET_KEY", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")
    auth.set_file("DEPLOY_KEY", __file__)
    print("   ✅ AWS credentials stored")
    print("   ✅ Deploy key file stored\n")

    # ── Notify stage ──
    print("📢 Notification Stage:")
    auth.set("SLACK_WEBHOOK", "https://hooks.slack.com/services/T00/B00/xxx")
    auth.set("EMAIL_API_KEY", "sendgrid-api-key-123")
    print("   ✅ Slack webhook stored")
    print("   ✅ Email API key stored\n")

    # ── Pipeline summary ──
    keys = auth.list_keys()
    print(f"📊 Pipeline vault summary:")
    print(f"   Total secrets: {len(keys)}")
    for key in sorted(keys):
        print(f"   - {key}")

    # ── Cleanup after pipeline ──
    print("\n🧹 Pipeline cleanup:")
    # Delete temporary test credentials
    auth.delete("TEST_DB_URL")
    auth.delete("TEST_API_KEY")
    print("   ✅ Test credentials deleted")

    remaining = auth.list_keys()
    print(f"   {len(remaining)} secrets retained for next runs")

    # Clean up
    for key in auth.list_keys():
        auth.delete(key)
    if os.path.exists(db_path):
        os.remove(db_path)


if __name__ == "__main__":
    main()
