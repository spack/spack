# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for a spec found in spec descriptor or database index.json files

.. literalinclude:: _spack_root/lib/spack/spack/schema/spec.py
   :lines: 15-
"""
from typing import Any, Dict

target = {
    "oneOf": [
        {"type": "string"},
        {
            "type": "object",
            "additionalProperties": False,
            "required": ["name", "vendor", "features", "generation", "parents"],
            "properties": {
                "name": {"type": "string"},
                "vendor": {"type": "string"},
                "features": {"type": "array", "items": {"type": "string"}},
                "generation": {"type": "integer"},
                "parents": {"type": "array", "items": {"type": "string"}},
                "cpupart": {"type": "string"},
            },
        },
    ]
}

arch = {
    "type": "object",
    "additionalProperties": False,
    "properties": {"platform": {}, "platform_os": {}, "target": target},
}

#: Corresponds to specfile format v1
dependencies_v1 = {
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "properties": {
            "hash": {"type": "string"},
            "type": {"type": "array", "items": {"type": "string"}},
        },
    },
}

#: Corresponds to specfile format v2-v3
dependencies_v2_v3 = {
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": ["name", "hash", "type"],
        "properties": {
            "name": {"type": "string"},
            "hash": {"type": "string"},
            "type": {"type": "array", "items": {"type": "string"}},
        },
    },
}

#: Corresponds to specfile format v4+
dependencies_v4_plus = {
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": ["name", "hash", "parameters"],
        "properties": {
            "name": {"type": "string"},
            "hash": {"type": "string"},
            "parameters": {
                "type": "object",
                "additionalProperties": False,
                "required": ["deptypes", "virtuals"],
                "properties": {
                    "deptypes": {"type": "array", "items": {"type": "string"}},
                    "virtuals": {"type": "array", "items": {"type": "string"}},
                    "direct": {"type": "boolean"},
                },
            },
        },
    },
}

dependencies = {"oneOf": [dependencies_v1, dependencies_v2_v3, dependencies_v4_plus]}

build_spec = {
    "type": "object",
    "additionalProperties": False,
    "required": ["name", "hash"],
    "properties": {"name": {"type": "string"}, "hash": {"type": "string"}},
}

#: Schema for a single spec node (used in both spec files and database entries)
spec_node = {
    "type": "object",
    "additionalProperties": False,
    "required": ["name"],
    "properties": {
        # name is a string for concrete specs, but may be null for abstract specs
        "name": {"type": ["string", "null"]},
        "hash": {"type": "string"},
        "package_hash": {"type": "string"},
        # these hashes were used on some specs prior to 0.18
        "full_hash": {"type": "string"},
        "build_hash": {"type": "string"},
        # concrete specs have a single version
        "version": {"type": "string"},
        # abstract specs have a version list
        "versions": {"type": "array", "items": {"type": "string"}},
        # list of variants to propagate (for abstract specs)
        "propagate": {"type": "array", "items": {"type": "string"}},
        # list of multi-valued variants that are abstract, i.e. foo=bar,baz instead of foo:=bar,baz (for abstract specs)
        "abstract": {"type": "array", "items": {"type": "string"}},
        # Whether the spec is concrete or not, when omitted defaults to true
        "concrete": {"type": "boolean"},
        "arch": arch,
        "compiler": {
            "type": "object",
            "additionalProperties": False,
            "properties": {"name": {"type": "string"}, "version": {"type": "string"}},
        },
        "develop": {"anyOf": [{"type": "boolean"}, {"type": "string"}]},
        "namespace": {"type": "string"},
        "parameters": {
            "type": "object",
            "additionalProperties": True,
            "properties": {
                "patches": {"type": "array", "items": {"type": "string"}},
                "cflags": {"type": "array", "items": {"type": "string"}},
                "cppflags": {"type": "array", "items": {"type": "string"}},
                "cxxflags": {"type": "array", "items": {"type": "string"}},
                "fflags": {"type": "array", "items": {"type": "string"}},
                "ldflags": {"type": "array", "items": {"type": "string"}},
                "ldlibs": {"type": "array", "items": {"type": "string"}},
            },
        },
        "patches": {"type": "array", "items": {"type": "string"}},
        "dependencies": dependencies,
        "build_spec": build_spec,
        "external": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "path": {"type": ["string", "null"]},
                "module": {
                    "anyOf": [{"type": "array", "items": {"type": "string"}}, {"type": "null"}]
                },
                "extra_attributes": {"type": "object"},
            },
        },
        "annotations": {
            "type": "object",
            "properties": {
                "original_specfile_version": {"type": "number"},
                "compiler": {"type": "string"},
            },
            "required": ["original_specfile_version"],
        },
    },
}

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "spec": {
        "type": "object",
        "additionalProperties": False,
        "required": ["_meta", "nodes"],
        "properties": {
            "_meta": {"type": "object", "properties": {"version": {"type": "number"}}},
            "nodes": {"type": "array", "items": spec_node},
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack spec schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["spec"],
    "properties": properties,
}
