# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for a spec found in spec descriptor or database index.json files

.. literalinclude:: _spack_root/lib/spack/spack/schema/spec.py
   :lines: 15-
"""
from typing import Any, Dict

target = {
    "description": "Target architecture (string for abstract specs, object for concrete specs)",
    "oneOf": [
        {
            "type": "string",
            "description": 'Target as a string (e.g. "zen2" or "haswell:broadwell") used in '
            "abstract specs",
        },
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
            "description": "Target as an object with detailed fields, used in concrete specs",
        },
    ],
}

arch = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "platform": {
            "type": ["string", "null"],
            "description": 'Target platform (e.g. "linux" or "darwin"). May be null for abstract '
            "specs",
        },
        "platform_os": {
            "type": ["string", "null"],
            "description": 'Target operating system (e.g. "ubuntu24.04"). May be '
            "null for abstract specs",
        },
        "target": target,
    },
}

#: Corresponds to specfile format v1
dependencies_v1 = {
    "type": "object",
    "description": "Specfile v1 style dependencies specification (package name to dependency "
    "info)",
    "additionalProperties": {
        "type": "object",
        "properties": {
            "hash": {"type": "string", "description": "Unique identifier of the dependency"},
            "type": {
                "type": "array",
                "items": {"enum": ["build", "link", "run", "test"]},
                "description": "Dependency types",
            },
        },
    },
}

#: Corresponds to specfile format v2-v3
dependencies_v2_v3 = {
    "type": "array",
    "description": "Specfile v2-v3 style dependencies specification (array of dependencies)",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": ["name", "hash", "type"],
        "properties": {
            "name": {"type": "string", "description": "Name of the dependency package"},
            "hash": {"type": "string", "description": "Unique identifier of the dependency"},
            "type": {
                "type": "array",
                "items": {"enum": ["build", "link", "run", "test"]},
                "description": "Dependency types",
            },
        },
    },
}

#: Corresponds to specfile format v4+
dependencies_v4_plus = {
    "type": "array",
    "description": "Specfile v4+ style dependencies specification (array of dependencies)",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": ["name", "hash", "parameters"],
        "properties": {
            "name": {"type": "string", "description": "Name of the dependency package"},
            "hash": {"type": "string", "description": "Unique identifier of the dependency"},
            "parameters": {
                "type": "object",
                "additionalProperties": False,
                "required": ["deptypes", "virtuals"],
                "properties": {
                    "deptypes": {
                        "type": "array",
                        "items": {"enum": ["build", "link", "run", "test"]},
                        "description": "Dependency types",
                    },
                    "virtuals": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Virtual dependencies used by the parent",
                    },
                    "direct": {
                        "type": "boolean",
                        "description": "Whether the dependency is direct (only on abstract specs)",
                    },
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
    "description": "Records the origin spec as it was built (used in splicing)",
}

#: Schema for a single spec node (used in both spec files and database entries)
spec_node = {
    "type": "object",
    "additionalProperties": False,
    "required": ["name"],
    "properties": {
        "name": {
            "type": ["string", "null"],
            "description": "Name is a string for concrete specs, but may be null for abstract "
            "specs",
        },
        "hash": {"type": "string", "description": "The DAG hash, which identifies the spec"},
        "package_hash": {"type": "string", "description": "The package hash (concrete specs)"},
        "full_hash": {
            "type": "string",
            "description": "This hash was used on some specs prior to 0.18",
        },
        "build_hash": {
            "type": "string",
            "description": "This hash was used on some specs prior to 0.18",
        },
        "version": {"type": "string", "description": "A single, concrete version (e.g. @=1.2)"},
        "versions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Abstract version (e.g. @1.2)",
        },
        "propagate": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of variants to propagate (for abstract specs)",
        },
        "abstract": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of multi-valued variants that are abstract, i.e. foo=bar,baz "
            "instead of foo:=bar,baz (for abstract specs)",
        },
        "concrete": {
            "type": "boolean",
            "description": "Whether the spec is concrete or not, when omitted defaults to true",
        },
        "arch": arch,
        "compiler": {
            "type": "object",
            "additionalProperties": False,
            "properties": {"name": {"type": "string"}, "version": {"type": "string"}},
            "description": "Compiler name and version (in spec file v5 listed as normal "
            "dependencies)",
        },
        "namespace": {"type": "string", "description": "Package repository namespace"},
        "parameters": {
            "type": "object",
            "additionalProperties": True,
            "description": "Variants and other parameters",
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
        "patches": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of patches, similar to the patches variant under parameters",
        },
        "dependencies": dependencies,
        "build_spec": build_spec,
        "external": {
            "type": "object",
            "additionalProperties": False,
            "description": "If path or module (or both) are set, the spec is an external "
            "system-installed package",
            "properties": {
                "path": {
                    "type": ["string", "null"],
                    "description": "Install prefix on the system, e.g. /usr",
                },
                "module": {
                    "anyOf": [{"type": "array", "items": {"type": "string"}}, {"type": "null"}],
                    "description": 'List of module names, e.g. ["pkg/1.2"]',
                },
                "extra_attributes": {
                    "type": "object",
                    "description": "Package.py specific attributes to use the external package, "
                    "such as paths to compiler executables",
                },
            },
        },
        "annotations": {
            "type": "object",
            "properties": {
                "original_specfile_version": {"type": "number"},
                "compiler": {"type": "string"},
            },
            "required": ["original_specfile_version"],
            "additionalProperties": False,
            "description": "Currently used to preserve compiler information of old specs when "
            "upgrading to a newer spec format",
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
            "_meta": {
                "type": "object",
                "properties": {"version": {"type": "number"}},
                "description": "Spec schema version metadata, used for parsing spec files",
            },
            "nodes": {
                "type": "array",
                "items": spec_node,
                "description": "List of spec nodes which, combined with dependencies, induce a "
                "DAG",
            },
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
