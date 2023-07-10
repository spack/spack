# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for mirrors.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/mirrors.py
   :lines: 12-78
"""

#: Common properties for connection specification
connection = {
    "url": {"type": "string"},
    # todo: replace this with named keys "username" / "password" or "id" / "secret"
    "access_pair": {
        "type": "array",
        "items": {"type": ["string", "null"], "minItems": 2, "maxItems": 2},
    },
    "access_token": {"type": ["string", "null"]},
    "profile": {"type": ["string", "null"]},
    "endpoint_url": {"type": ["string", "null"]},
}

#: Mirror connection inside pull/push keys
fetch_and_push = {
    "anyOf": [
        {"type": "string"},
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {**connection},  # type: ignore
        },
    ]
}

#: Mirror connection when no pull/push keys are set
mirror_entry = {
    "type": "object",
    "additionalProperties": False,
    "anyOf": [{"required": ["url"]}, {"required": ["fetch"]}, {"required": ["pull"]}],
    "properties": {
        "source": {"type": "boolean"},
        "binary": {"type": "boolean"},
        "fetch": fetch_and_push,
        "push": fetch_and_push,
        **connection,  # type: ignore
    },
}

#: Properties for inclusion in other schemas
properties = {
    "mirrors": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "patternProperties": {r"\w[\w-]*": {"anyOf": [{"type": "string"}, mirror_entry]}},
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack mirror configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}


def update(data: dict):
    """Update the mirror config section

    Args:
        data (dict): dictionary to be updated

    Returns:
        True if data was changed, False otherwise
    """
    # get rid of keys that just have `null` values, which we
    # added in the past by accident.

    def drop_null_values(details):
        if not isinstance(details, dict):
            return False
        updated = False
        if details.get("access_pair", False) == [None, None]:
            del details["access_pair"]
            updated = True
        if details.get("access_token", False) is None:
            del details["access_token"]
            updated = True
        if details.get("profile", False) is None:
            del details["profile"]
            updated = True
        if details.get("endpoint_url", False) is None:
            del details["endpoint_url"]
            updated = True
        return updated

    updated = False

    for name in list(data.keys()):
        mirror = data[name]

        # Just a URL
        if isinstance(mirror, str):
            continue

        # First we drop nulls in (access_pair, access_token, profile, endpoint_url)
        updated |= drop_null_values(mirror)
        updated |= drop_null_values(mirror.get("fetch", None))
        updated |= drop_null_values(mirror.get("push", None))

    return updated
