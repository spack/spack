# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for packages.yaml configuration files.

.. literalinclude:: _spack_root/lib/spack/spack/schema/packages.py
   :lines: 13-
"""


#: Properties for inclusion in other schemas
properties = {
    "packages": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "patternProperties": {
            r"\w[\w-]*": {  # package name
                "type": "object",
                "default": {},
                "additionalProperties": False,
                "properties": {
                    "require": {
                        "oneOf": [
                            # 'require' can be a list of requirement_groups.
                            # each requirement group is a list of one or more
                            # specs. Either at least one or exactly one spec
                            # in the group must be satisfied (depending on
                            # whether you use "any_of" or "one_of",
                            # repectively)
                            {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "one_of": {"type": "array"},
                                        "any_of": {"type": "array"},
                                    },
                                },
                            },
                            # Shorthand for a single requirement group with
                            # one member
                            {"type": "string"},
                        ]
                    },
                    "version": {
                        "type": "array",
                        "default": [],
                        # version strings
                        "items": {"anyOf": [{"type": "string"}, {"type": "number"}]},
                    },
                    "target": {
                        "type": "array",
                        "default": [],
                        # target names
                        "items": {"type": "string"},
                    },
                    "compiler": {
                        "type": "array",
                        "default": [],
                        "items": {"type": "string"},
                    },  # compiler specs
                    "buildable": {"type": "boolean", "default": True},
                    "permissions": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "read": {"type": "string", "enum": ["user", "group", "world"]},
                            "write": {"type": "string", "enum": ["user", "group", "world"]},
                            "group": {"type": "string"},
                        },
                    },
                    # If 'get_full_repo' is promoted to a Package-level
                    # attribute, it could be useful to set it here
                    "package_attributes": {
                        "type": "object",
                        "additionalProperties": False,
                        "patternProperties": {r"\w+": {}},
                    },
                    "providers": {
                        "type": "object",
                        "default": {},
                        "additionalProperties": False,
                        "patternProperties": {
                            r"\w[\w-]*": {
                                "type": "array",
                                "default": [],
                                "items": {"type": "string"},
                            }
                        },
                    },
                    "variants": {
                        "oneOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                        ]
                    },
                    "externals": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "spec": {"type": "string"},
                                "prefix": {"type": "string"},
                                "modules": {"type": "array", "items": {"type": "string"}},
                                "extra_attributes": {"type": "object"},
                            },
                            "additionalProperties": True,
                            "required": ["spec"],
                        },
                    },
                },
            }
        },
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack package configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
