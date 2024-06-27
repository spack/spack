# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for splice.yaml configuration file.
"""


#: Properties for inclusion in other schemas
properties = {
    "splice": {
        "type": "array",
        "default": [],
        "items": {
            "type": "object",
            "required": ["target", "replacement"],
            "additionalProperties": False,
            "properties": {
                "target": {"type": "string"},
                "replacement": {"type": "string"},
                "transitive": {"type": "boolean", "default": False},
            },
        },
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack concretization splice configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
