"""LaunchDarkly SDK initialization and helpers."""

import os

from dotenv import load_dotenv
import ldclient
from ldclient import Context
from ldclient.config import Config

load_dotenv()

_sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY")
if _sdk_key:
    ldclient.set_config(Config(_sdk_key))


def get_client():
    """Return the LaunchDarkly client. May not be initialized if SDK key is missing."""
    return ldclient.get()


def get_context(user_id: str, tier: str, name: str | None = None) -> Context:
    """Build an LD context for the given user."""
    builder = Context.builder(user_id)
    builder.set("tier", tier)
    if name:
        builder.name(name)
    return builder.build()


def track(event_key: str, context: Context, data: dict | None = None) -> None:
    """Track a custom event."""
    get_client().track(event_key, context, data)
