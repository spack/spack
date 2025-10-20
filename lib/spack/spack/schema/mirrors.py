# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for mirrors.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/mirrors.py
   :lines: 13-
"""
from typing import Any, Dict

#: Common properties for connection specification
connection = {
    "url": {"type": "string"},
    "access_pair": {
        "type": "object",
        "required": ["secret_variable"],
        # Only allow id or id_variable to be set, not both
        "oneOf": [{"required": ["id"]}, {"required": ["id_variable"]}],
        "properties": {
            "id": {"type": "string"},
            "id_variable": {"type": "string"},
            "secret_variable": {"type": "string"},
        },
    },
    "profile": {"type": ["string", "null"]},
    "endpoint_url": {"type": ["string", "null"]},
    "access_token_variable": {"type": ["string", "null"]},
}


#: Mirror connection inside pull/push keys
fetch_and_push = {
    "anyOf": [
        {"type": "string"},
        {"type": "object", "additionalProperties": False, "properties": {**connection}},
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
        "signed": {"type": "boolean"},
        "fetch": fetch_and_push,
        "push": fetch_and_push,
        "autopush": {"type": "boolean"},
        **connection,
    },
}

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "mirrors": {
        "type": "object",
        "default": {},
        "additionalProperties": {"anyOf": [{"type": "string"}, mirror_entry]},
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
