# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for cdash.yaml configuration file.

.. literalinclude:: ../spack/schema/cdash.py
   :lines: 13-
"""
from typing import Any, Dict

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "cdash": {
        "type": "object",
        "additionalProperties": False,
        "required": ["build-group"],
        "description": "Configuration for uploading build results to CDash",
        "properties": {
            "build-group": {
                "type": "string",
                "description": "Unique build group name for this stack",
            },
            "url": {"type": "string", "description": "CDash server URL"},
            "project": {"type": "string", "description": "CDash project name"},
            "site": {"type": "string", "description": "Site identifier for CDash reporting"},
        },
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack cdash configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
