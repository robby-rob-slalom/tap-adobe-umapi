"""Stream type classes for tap-adobe-umapi."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
from singer_sdk import typing as th  # JSON Schema typing helpers
from tap_adobe_umapi.client import AdobeUmapiStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class OrganizationBasedStream(AdobeUmapiStream):
    """Base class for streams that are keys based on project ID."""

    @property
    def partitions(self) -> list:
        """Return a list of partition key dicts (if applicable), otherwise None."""
        if "{orgId}" in self.path:
            return [
                {"orgId": self.config.get("organization_id")}
            ]
        raise ValueError(
            "Could not detect partition type for stream "
            f"'{self.name}' ({self.path}). "
            "Expected a URL path containing '{organization_id}'. "
        )

class UsersStream(OrganizationBasedStream):
    """Define custom stream."""
    name = "users"
    path = "/users/{orgId}/0"
    records_jsonpath = "$.users[*]"
    primary_keys = []
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "users.json"
    

