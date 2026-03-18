# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for packages.yaml configuration files.

.. literalinclude:: _spack_root/lib/spack/spack/schema/packages.py
   :lines: 14-
"""
from typing import Any, Dict

import spack.schema.environment

from .compilers import extra_rpaths, flags, implicit_rpaths

permissions = {
    "type": "object",
    "description": "File permissions settings for package installations",
    "additionalProperties": False,
    "properties": {
        "read": {
            "type": "string",
            "enum": ["user", "group", "world"],
            "description": "Who can read the files installed by a package",
        },
        "write": {
            "type": "string",
            "enum": ["user", "group", "world"],
            "description": "Who can write to the files installed by a package",
        },
        "group": {
            "type": "string",
            "description": "The group that owns the files installed by a package",
        },
    },
}

variants = {
    "oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}],
    "description": "Soft variant preferences as a single spec string or list of variant "
    "specifications (ignored if the concretizer can reuse existing installations)",
}

requirements = {
    "description": "Package requirements that must be satisfied during concretization",
    "oneOf": [
        # 'require' can be a list of requirement_groups. each requirement group is a list of one or
        # more specs. Either at least one or exactly one spec in the group must be satisfied
        # (depending on whether you use "any_of" or "one_of", respectively)
        {
            "type": "array",
            "items": {
                "oneOf": [
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "one_of": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of specs where exactly one must be satisfied",
                            },
                            "any_of": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of specs where at least one must be "
                                "satisfied",
                            },
                            "spec": {
                                "type": "string",
                                "description": "Single spec requirement that must be satisfied",
                            },
                            "message": {
                                "type": "string",
                                "description": "Custom error message when requirement is not "
                                "satisfiable",
                            },
                            "when": {
                                "type": "string",
                                "description": "Conditional spec that triggers this requirement",
                            },
                        },
                    },
                    {"type": "string"},
                ]
            },
        },
        # Shorthand for a single requirement group with one member
        {"type": "string"},
    ],
}

prefer_and_conflict = {
    "type": "array",
    "items": {
        "oneOf": [
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "spec": {"type": "string", "description": "Spec constraint to apply"},
                    "message": {
                        "type": "string",
                        "description": "Custom message explaining the constraint",
                    },
                    "when": {
                        "type": "string",
                        "description": "Conditional spec that triggers this constraint",
                    },
                },
            },
            {"type": "string"},
        ]
    },
}

package_attributes = {
    "type": "object",
    "description": "Class-level attributes to assign to package instances "
    "(accessible in package.py methods)",
    "additionalProperties": False,
    "patternProperties": {r"^[a-zA-Z_]\w*$": {}},
}

REQUIREMENT_URL = "https://spack.readthedocs.io/en/latest/packages_yaml.html#package-requirements"

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "packages": {
        "type": "object",
        "description": "Package-specific build settings and external package configurations",
        "default": {},
        "properties": {
            "all": {
                "type": "object",
                "description": "Default settings that apply to all packages (can be overridden "
                "by package-specific settings)",
                "default": {},
                "additionalProperties": False,
                "properties": {
                    "require": requirements,
                    "prefer": {
                        "description": "Strong package preferences that influence concretization "
                        "without imposing hard constraints",
                        **prefer_and_conflict,
                    },
                    "conflict": {
                        "description": "Package conflicts that prevent certain spec combinations",
                        **prefer_and_conflict,
                    },
                    # target names
                    "target": {
                        "type": "array",
                        "description": "Ordered list of soft preferences for target "
                        "architectures for all packages (ignored if the concretizer can reuse "
                        "existing installations)",
                        "default": [],
                        "items": {"type": "string"},
                    },
                    # compiler specs
                    "compiler": {
                        "type": "array",
                        "description": "Soft preferences for compiler specs for all packages "
                        "(deprecated)",
                        "default": [],
                        "items": {"type": "string"},
                    },
                    "buildable": {
                        "type": "boolean",
                        "description": "Whether packages should be built from source (false "
                        "prevents building)",
                        "default": True,
                    },
                    "permissions": permissions,
                    # If 'get_full_repo' is promoted to a Package-level
                    # attribute, it could be useful to set it here
                    "package_attributes": package_attributes,
                    "providers": {
                        "type": "object",
                        "description": "Soft preferences for providers of virtual packages "
                        "(ignored if the concretizer can reuse existing installations)",
                        "default": {},
                        "additionalProperties": {
                            "type": "array",
                            "description": "Ordered list of preferred providers for this virtual "
                            "package",
                            "default": [],
                            "items": {"type": "string"},
                        },
                    },
                    "variants": variants,
                },
                "deprecatedProperties": [
                    {
                        "names": ["compiler"],
                        "message": "The packages:all:compiler preference has been deprecated in "
                        "Spack v1.0, and is currently ignored. It will be removed from config in "
                        "Spack v1.2.",
                        "error": False,
                    }
                ],
            }
        },
        # package names
        "additionalProperties": {
            "type": "object",
            "description": "Package-specific settings that override defaults from 'all'",
            "default": {},
            "additionalProperties": False,
            "properties": {
                "require": requirements,
                "prefer": {
                    "description": "Strong package preferences that influence concretization "
                    "without imposing hard constraints",
                    **prefer_and_conflict,
                },
                "conflict": {
                    "description": "Package conflicts that prevent certain spec combinations",
                    **prefer_and_conflict,
                },
                "version": {
                    "type": "array",
                    "description": "Ordered list of soft preferences for versions for this "
                    "package (ignored if the concretizer can reuse existing installations)",
                    "default": [],
                    # version strings
                    "items": {"anyOf": [{"type": "string"}, {"type": "number"}]},
                },
                "buildable": {
                    "type": "boolean",
                    "description": "Whether this package should be built from source (false "
                    "prevents building)",
                    "default": True,
                },
                "permissions": permissions,
                # If 'get_full_repo' is promoted to a Package-level
                # attribute, it could be useful to set it here
                "package_attributes": package_attributes,
                "variants": variants,
                "externals": {
                    "type": "array",
                    "description": "List of external, system-installed instances of this package",
                    "items": {
                        "type": "object",
                        "properties": {
                            "spec": {
                                "type": "string",
                                "description": "Spec string describing this external package "
                                "instance. Typically name@version and relevant variants",
                            },
                            "prefix": {
                                "type": "string",
                                "description": "Installation prefix path for this external "
                                "package (typically /usr, *excluding* bin/, lib/, etc.)",
                            },
                            "modules": {
                                "type": "array",
                                "description": "Environment modules to load for this external "
                                "package",
                                "items": {"type": "string"},
                            },
                            "id": {"type": "string"},
                            "extra_attributes": {
                                "type": "object",
                                "description": "Additional information needed by the package "
                                "to use this external",
                                "additionalProperties": {"type": "string"},
                                "properties": {
                                    "compilers": {
                                        "type": "object",
                                        "description": "Compiler executable paths for external "
                                        "compiler packages",
                                        "properties": {
                                            "c": {
                                                "type": "string",
                                                "description": "Path to the C compiler "
                                                "executable (e.g. /usr/bin/gcc)",
                                            },
                                            "cxx": {
                                                "type": "string",
                                                "description": "Path to the C++ compiler "
                                                "executable (e.g. /usr/bin/g++)",
                                            },
                                            "fortran": {
                                                "type": "string",
                                                "description": "Path to the Fortran compiler "
                                                "executable (e.g. /usr/bin/gfortran)",
                                            },
                                        },
                                        "patternProperties": {r"^\w": {"type": "string"}},
                                        "additionalProperties": False,
                                    },
                                    "environment": spack.schema.environment.definition,
                                    "extra_rpaths": extra_rpaths,
                                    "implicit_rpaths": implicit_rpaths,
                                    "flags": flags,
                                },
                            },
                            "dependencies": {
                                "type": "array",
                                "description": "List of dependencies for this external package, "
                                "specifying dependency relationships explicitly",
                                "items": {
                                    "type": "object",
                                    "description": "Dependency specification for an external "
                                    "package",
                                    "properties": {
                                        "id": {
                                            "type": "string",
                                            "description": "Explicit reference ID to another "
                                            "external package (provides unambiguous reference)",
                                        },
                                        "spec": {
                                            "type": "string",
                                            "description": "Spec string that matches an "
                                            "available external package",
                                        },
                                        "deptypes": {
                                            "oneOf": [
                                                {
                                                    "type": "string",
                                                    "description": "Single dependency type "
                                                    "(e.g., 'build', 'link', 'run', 'test')",
                                                },
                                                {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "string",
                                                        "description": "Dependency type (e.g., "
                                                        "'build', 'link', 'run', 'test')",
                                                    },
                                                    "description": "List of dependency types "
                                                    "(e.g., ['build', 'link'])",
                                                },
                                            ],
                                            "description": "Dependency types; if not specified, "
                                            "inferred from package recipe",
                                        },
                                        "virtuals": {
                                            "type": "string",
                                            "description": "Virtual package name this dependency "
                                            "provides (e.g., 'mpi')",
                                        },
                                    },
                                },
                            },
                        },
                        "additionalProperties": False,
                        "required": ["spec"],
                    },
                },
            },
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


def update(data):
    data = data["packages"]
    changed = False
    for key in data:
        version = data[key].get("version")
        if not version or all(isinstance(v, str) for v in version):
            continue

        data[key]["version"] = [str(v) for v in version]
        changed = True

    return changed
