# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for resource.yaml configuration file."""

from typing import Any, Dict

#: Schema for bootstrap resources
resource_provider = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string"},
        "endpoint": {"type": "string"},
        "sha256": {"type": "string"},
    },
}

resource_entry = {
    "type": "object",
    "default": {},
    "additionalProperties": False,
    "patternProperties": {
        r"\w[\w]*": {
            "type": "object",
            "additionalProperties": False,
            "anyOf": [{"required": ["providers"]}],
            "properties": {"providers": {"type": "array", "items": resource_provider}},
        }
    },
}

properties: Dict[str, Any] = {
    "resource": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "properties": {"enable": {"type": "boolean"}, "resources": resource_entry},
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack resource configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
