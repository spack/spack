# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for concretizer.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/concretizer.py
   :lines: 12-
"""
from typing import Any, Dict

LIST_OF_SPECS = {"type": "array", "items": {"type": "string"}}

properties: Dict[str, Any] = {
    "concretizer": {
        "type": "object",
        "additionalProperties": False,
        "description": "Concretizer configuration that controls dependency selection, package "
        "reuse, and solver behavior",
        "properties": {
            "force": {
                "type": "boolean",
                "default": False,
                "description": "Force re-concretization when concretizing environments",
            },
            "reuse": {
                "description": "Controls how aggressively Spack reuses installed packages and "
                "build caches during concretization",
                "oneOf": [
                    {
                        "type": "boolean",
                        "description": "If true, reuse installed packages and build caches for "
                        "all specs; if false, always perform fresh concretization",
                    },
                    {
                        "type": "string",
                        "enum": ["dependencies"],
                        "description": "Reuse installed packages and build caches only for "
                        "dependencies, not root specs",
                    },
                    {
                        "type": "object",
                        "description": "Advanced reuse configuration with fine-grained control "
                        "over which specs are reused",
                        "properties": {
                            "roots": {
                                "type": "boolean",
                                "description": "If true, root specs are reused; if false, only "
                                "dependencies of root specs are reused",
                            },
                            "include": {
                                **LIST_OF_SPECS,
                                "description": "List of spec constraints. Reusable specs must "
                                "match at least one constraint",
                            },
                            "exclude": {
                                **LIST_OF_SPECS,
                                "description": "List of spec constraints. Reusable specs must "
                                "not match any constraint",
                            },
                            "from": {
                                "type": "array",
                                "description": "List of sources from which reused specs are taken",
                                "items": {
                                    "type": "object",
                                    "description": "Source configuration for reusable specs",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": [
                                                "local",
                                                "buildcache",
                                                "external",
                                                "environment",
                                            ],
                                            "description": "Type of source: 'local' (installed "
                                            "packages), 'buildcache' (remote binaries), "
                                            "'external' (system packages), or 'environment' "
                                            "(from specific environment)",
                                        },
                                        "path": {
                                            "type": "string",
                                            "description": "Path to the source (for environment "
                                            "type sources)",
                                        },
                                        "include": {
                                            **LIST_OF_SPECS,
                                            "description": "Spec constraints that must be "
                                            "matched for this source (overrides global include)",
                                        },
                                        "exclude": {
                                            **LIST_OF_SPECS,
                                            "description": "Spec constraints that must not be "
                                            "matched for this source (overrides global exclude)",
                                        },
                                    },
                                },
                            },
                        },
                    },
                ],
            },
            "targets": {
                "type": "object",
                "description": "Controls which target microarchitectures are considered "
                "during concretization",
                "properties": {
                    "host_compatible": {
                        "type": "boolean",
                        "description": "If true, only allow targets compatible with the "
                        "current host; if false, allow any target (e.g., concretize for icelake "
                        "while running on haswell)",
                    },
                    "granularity": {
                        "type": "string",
                        "enum": ["generic", "microarchitectures"],
                        "description": "Target selection granularity: 'microarchitectures' "
                        "(e.g., haswell, skylake) or 'generic' (e.g., x86_64_v3, aarch64)",
                    },
                },
            },
            "unify": {
                "description": "Controls whether environment specs are concretized together "
                "or separately",
                "oneOf": [
                    {
                        "type": "boolean",
                        "description": "If true, concretize environment root specs together "
                        "for unified dependencies; if false, concretize each spec independently",
                    },
                    {
                        "type": "string",
                        "enum": ["when_possible"],
                        "description": "Maximizes reuse, while allowing multiple instances of the "
                        "same package",
                    },
                ],
            },
            "compiler_mixing": {
                "oneOf": [{"type": "boolean"}, {"type": "array"}],
                "description": "Whether to allow compiler mixing between link/run dependencies",
            },
            "splice": {
                "type": "object",
                "additionalProperties": False,
                "description": "Configuration for spec splicing: replacing dependencies "
                "with ABI-compatible alternatives to improve package reuse",
                "properties": {
                    "explicit": {
                        "type": "array",
                        "default": [],
                        "description": "List of explicit splice configurations to replace "
                        "specific dependencies",
                        "items": {
                            "type": "object",
                            "required": ["target", "replacement"],
                            "additionalProperties": False,
                            "description": "Explicit splice configuration",
                            "properties": {
                                "target": {
                                    "type": "string",
                                    "description": "Abstract spec to be replaced (e.g., 'mpi' "
                                    "or specific package)",
                                },
                                "replacement": {
                                    "type": "string",
                                    "description": "Concrete spec with hash to use as "
                                    "replacement (e.g., 'mpich/abcdef')",
                                },
                                "transitive": {
                                    "type": "boolean",
                                    "default": False,
                                    "description": "If true, use transitive splice (conflicts "
                                    "resolved using replacement dependencies); if false, use "
                                    "intransitive splice (conflicts resolved using original "
                                    "dependencies)",
                                },
                            },
                        },
                    },
                    "automatic": {
                        "type": "boolean",
                        "description": "Enable automatic splicing for ABI-compatible packages "
                        "(experimental feature)",
                    },
                },
            },
            "duplicates": {
                "type": "object",
                "description": "Controls whether the dependency graph can contain multiple "
                "configurations of the same package",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": ["none", "minimal", "full"],
                        "description": "Duplication strategy: 'none' (single config per "
                        "package), 'minimal' (allow build-tools duplicates), 'full' "
                        "(experimental: allow full build-tool stack separation)",
                    },
                    "max_dupes": {
                        "type": "object",
                        "description": "Maximum number of duplicates allowed per package when "
                        "using strategies that permit duplicates",
                        "additionalProperties": {
                            "type": "integer",
                            "minimum": 1,
                            "description": "Maximum number of duplicate instances for this "
                            "package",
                        },
                    },
                },
            },
            "static_analysis": {
                "type": "boolean",
                "description": "Enable static analysis to reduce concretization time by "
                "generating smaller ASP problems",
            },
            "timeout": {
                "type": "integer",
                "minimum": 0,
                "description": "Maximum time in seconds for the solve phase (0 means no "
                "time limit)",
            },
            "error_on_timeout": {
                "type": "boolean",
                "description": "If true, timeout always results in error; if false, use best "
                "suboptimal solution found before timeout (yields unreproducible results)",
            },
            "os_compatible": {
                "type": "object",
                "additionalProperties": {"type": "array"},
                "description": "Compatibility mapping between operating systems for reuse of "
                "compilers and packages (key: target OS, value: list of compatible source OSes)",
            },
            "concretization_cache": {
                "type": "object",
                "description": "Configuration for caching solver outputs from successful "
                "concretization runs",
                "properties": {
                    "enable": {
                        "type": "boolean",
                        "description": "Whether to utilize a cache of solver outputs from "
                        "successful concretization runs",
                    },
                    "url": {
                        "type": "string",
                        "description": "Path to the location where Spack will root the "
                        "concretization cache",
                    },
                    "entry_limit": {
                        "type": "integer",
                        "minimum": 0,
                        "description": "Limit on the number of concretization results that "
                        "Spack will cache (0 disables pruning)",
                    },
                },
            },
            "externals": {
                "type": "object",
                "description": "Configuration for how Spack handles external packages during "
                "concretization",
                "properties": {
                    "completion": {
                        "type": "string",
                        "enum": ["architecture_only", "default_variants"],
                        "description": "Controls how missing information (variants, etc.) is "
                        "completed for external packages: 'architecture_only' completes only "
                        "mandatory architectural information; 'default_variants' also completes "
                        "missing variants using their default values",
                    }
                },
            },
        },
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack concretizer configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
