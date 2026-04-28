"""Example demonstrating WAuth + WPipe integration for access control.

This example shows how to:
1. Use WAuth to store and retrieve encrypted secrets.
2. Use WPipe to create a conditional pipeline for authentication.
3. Combine both libraries for secure, stateful access control.

Prerequisites:
    Run create_secret.py first to populate the secret vault.

Usage:
    python example.py
"""

import os
from pathlib import Path

from pydantic import BaseModel
from wpipe import Condition, Pipeline, step, to_obj

from wauth import WAuth


class SecretInfo(BaseModel):
    """Model representing user credentials."""

    user: str
    secret: str


class AccessResult(BaseModel):
    """Model representing access control result."""

    permitid_access: int


class UserProfile(BaseModel):
    """Model representing user profile data."""

    rol: str
    salario: int
    company: str


class ReportData(BaseModel):
    """Model representing final report data."""

    user: str
    secret: str


CUSTOM_KEY = "my-very-secure-key"
DB_PATH = "wauth2.db"
PIPELINE_DB = "./wpipe_wauth.db"
CONFIG_DIR = "./config"


@step(name="login", version="v1.0")
@to_obj
def login(my_data: SecretInfo) -> AccessResult:
    """Authenticate user by comparing credentials against stored secrets."""
    auth = WAuth(db_path=DB_PATH, custom_key=CUSTOM_KEY)
    real_password = auth.get("USER_1")

    permitid_access = 1 if my_data.secret == real_password else 0
    return AccessResult(permitid_access=permitid_access)


@step(name="search_db", version="v1.0")
@to_obj
def search_db(my_data: SecretInfo) -> UserProfile:
    """Fetch user profile from database."""
    return UserProfile(
        rol="example_role",
        salario=50000,
        company="example_company",
    )


@step(name="report", version="v1.0")
@to_obj
def report(my_data: SecretInfo) -> ReportData:
    """Generate final report with user data."""
    return ReportData(
        user=my_data.user,
        secret=my_data.secret,
    )


@to_obj
def print_access_granted(my_data: SecretInfo) -> dict:
    """Print access granted message."""
    print("Access granted for user:", my_data.user)
    return {}


@to_obj
def print_access_denied(my_data: AccessResult) -> dict:
    """Print access denied message."""
    print("Access denied")
    return {}


def main() -> None:
    """Run the WAuth + WPipe access control pipeline."""
    if not os.path.exists(DB_PATH):
        print("Run create_secret.py first to populate the vault")
        return

    wauth_wpipe = Pipeline(
        tracking_db=PIPELINE_DB,
        config_dir=CONFIG_DIR,
        pipeline_name="access_control",
        verbose=False,
    )

    wauth_wpipe.set_steps(
        [
            login,
            Condition(
                expression="permitid_access == 1",
                branch_true=[
                    (print_access_granted, "report", "v1.0"),
                    search_db,
                    report,
                ],
                branch_false=[(print_access_denied, "report", "v1.0")],
            ),
        ]
    )

    def run_pipeline(car_dict):
        return wauth_wpipe.run(car_dict)

    user = SecretInfo(user="USER_1", secret="mysecretpassword123")
    result = run_pipeline(user.dict())
    print(result)


if __name__ == "__main__":
    main()
