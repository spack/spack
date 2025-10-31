# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for include.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/include.py
   :lines: 12-
"""
from typing import Any, Dict

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "include": {
        "type": "array",
        "default": [],
        "additionalProperties": False,
        "items": {
            "anyOf": [
                # local, required path
                {"type": "string"},
                # local or remote paths that may be optional or conditional
                {
                    "type": "object",
                    "properties": {
                        "when": {"type": "string"},
                        "name": {"type": "string"},
                        "path_override_env_var": {"type": "string"},
                        "path": {"type": "string"},
                        "sha256": {"type": "string"},
                        "optional": {"type": "boolean"},
                    },
                    "required": ["path"],
                    "additionalProperties": False,
                },
                # remote git paths that may be optional or conditional
                {
                    "type": "object",
                    "properties": {
                        "git": {"type": "string"},
                        "branch": {"type": "string"},
                        "commit": {"type": "string"},
                        "tag": {"type": "string"},
                        "paths": {"type": "array", "items": {"type": "string"}},
                        "when": {"type": "string"},
                        "optional": {"type": "boolean"},
                    },
                    "required": ["git", "paths"],
                    "additionalProperties": False,
                },
            ]
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack include configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
