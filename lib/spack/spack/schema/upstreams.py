# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Configuration for upstream DBs."""

#: Properties for inclusion in other schemas
properties = {
    "upstreams": {
        "type": "object",
        "default": {},
        "patternProperties": {
            # pylint: disable=duplicate-code
            r"\w[\w-]*": {
                "type": "object",
                "default": {},
                "additionalProperties": False,
                "properties": {
                    "install_tree": {"type": "string"},
                    "modules": {
                        "type": "object",
                        "properties": {"tcl": {"type": "string"}, "lmod": {"type": "string"}},
                    },
                },
            }
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack upstream configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
