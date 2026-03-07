"""LaunchDarkly SDK setup: init, flag evaluation, and track for connectivity validation."""

import os

from dotenv import load_dotenv

load_dotenv()
import ldclient
from ldclient import Context
from ldclient.config import Config


def main() -> None:
    sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY")
    if not sdk_key:
        raise ValueError(
            "LAUNCHDARKLY_SDK_KEY environment variable is required. "
            "Set it in .env or export it before running."
        )

    ldclient.set_config(Config(sdk_key))
    client = ldclient.get()

    try:
        if not client.is_initialized():
            print("Waiting for SDK to initialize...")
            client.wait_for_initialization(timeout=10)

        context = Context.builder("sdk-validation-context").name("SDK Validation").build()

        # Flag evaluation to confirm connectivity
        flag_value = client.variation("example-flag-key", context, False)
        print(f"Flag 'example-flag-key' value: {flag_value}")

        # Track custom event to validate connectivity
        client.track("sdk-connectivity-check", context, {"source": "cursor"})
        print("Track event 'sdk-connectivity-check' sent with data: {source: 'cursor'}")

    finally:
        ldclient.close()


if __name__ == "__main__":
    main()
