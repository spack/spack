# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for env.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/env.py
   :lines: 19-
"""

import os
from typing import Any, Dict

import spack.schema.merged

from .spec_list import spec_list_properties, spec_list_schema

#: Top level key in a manifest file
TOP_LEVEL_KEY = "spack"

# (DEPRECATED) include concrete entries to be merged under the include key
include_concrete = {
    "type": "array",
    "default": [],
    "description": "List of paths to other environments. Includes concrete specs "
    "from their spack.lock files without modifying the source environments. Useful "
    "for phased deployments where you want to build on existing concrete specs.",
    "items": {"type": "string"},
}

group_name_and_deps = {
    "group": {"type": "string", "description": "Name for this group of specs"},
    "explicit": {
        "type": "boolean",
        "default": True,
        "description": "When false, specs in this group are installed as implicit "
        "dependencies and are eligible for garbage collection.",
    },
    "needs": {
        "type": "array",
        "description": "Groups of specs that are needed by this group",
        "items": {"type": "string"},
    },
    "override": {
        "type": "object",
        "description": "Top-most configuration scope for this group of specs",
        "additionalProperties": False,
        "properties": {**spack.schema.merged.ref_sections},
    },
}


properties: Dict[str, Any] = {
    "spack": {
        "type": "object",
        "default": {},
        "description": "Spack environment configuration, including specs, view, and any other "
        "config section (config, packages, concretizer, mirrors, etc.)",
        "additionalProperties": False,
        "properties": {
            # merged configuration scope schemas
            **spack.schema.merged.ref_sections,
            # extra environment schema properties
            "specs": {
                "type": "array",
                "description": "List of specs to include in the environment, "
                "supporting both simple specs and matrix configurations",
                "default": [],
                "items": {
                    "anyOf": [
                        {
                            "type": "object",
                            "description": "Matrix configuration for generating multiple specs"
                            " from combinations of constraints",
                            "additionalProperties": False,
                            "properties": {**spec_list_properties},
                        },
                        {"type": "string", "description": "Simple spec string"},
                        {"type": "null"},
                        {
                            "type": "object",
                            "description": "User spec group with a single matrix",
                            "additionalProperties": False,
                            "properties": {**spec_list_properties, **group_name_and_deps},
                        },
                        {
                            "type": "object",
                            "description": "User spec group with multiple matrices",
                            "additionalProperties": False,
                            "properties": {**group_name_and_deps, "specs": spec_list_schema},
                        },
                    ]
                },
            },
            # (DEPRECATED) include concrete to be merged under the include key
            "include_concrete": include_concrete,
        },
    }
}

schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack environment file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
    "definitions": spack.schema.merged.defs,
}


def update(data: Dict[str, Any]) -> bool:
    """Update the spack.yaml data to the new format.

    Args:
        data: dictionary to be updated

    Returns:
        ``True`` if data was changed, ``False`` otherwise
    """
    if not isinstance(data, dict):
        return False

    if "include_concrete" not in data:
        return False

    # Move the old 'include_concrete' paths to reside under the 'include',
    # ensuring that the lock file name is appended.
    includes = []
    for path in data["include_concrete"]:
        if os.path.basename(path) != "spack.lock":
            path = os.path.join(path, "spack.lock")
        includes.append(path)

    # Now add back the includes the environment file already has.
    if "include" in data:
        for path in data["include"]:
            includes.append(path)

    data["include"] = includes
    del data["include_concrete"]

    return True
