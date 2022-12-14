# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for mirrors.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/mirrors.py
"""

#: Common properties for connection specification
connection = {
    "url": {"type": "string"},
    "access_pair": {"type": "array", "items": {"type": "string", "minItems": 2, "maxItems": 2}},
    "access_token": {"type", "string"},
    "profile": {"type": "string"},
    "endpoint_url": {"type": "string"},
}

#: Mirror connection inside pull/push keys
mirror_conection = {
    "type": "object",
    "additionalProperties": False,
    "required": ["url"],
    "properties": {**connection},
}

#: Mirror connection when no pull/push keys are set
top_level_mirror_connection = {
    "type": "object",
    "additionalProperties": False,
    "required": ["url"],
    "properties": {"source": {"type": "boolean"}, "binary": {"type": "boolean"}, **connection},
}

#: Properties for inclusion in other schemas
properties = {
    "mirrors": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "patternProperties": {
            r"\w[\w-]*": {
                "anyOf": [
                    {"type": "string"},
                    top_level_mirror_connection,
                    {
                        "type": "object",
                        "required": ["fetch", "push"],
                        "additionalProperties": False,
                        "properties": {
                            "fetch": {"anyOf": [{"type": "string"}, mirror_conection]},
                            "push": {"anyOf": [{"type": "string"}, mirror_conection]},
                        },
                    },
                ]
            }
        },
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
