# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for env.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/env.py
   :lines: 19-
"""

from typing import Any, Dict

import spack.schema.merged

from .spec_list import spec_list_properties, spec_list_schema

#: Top level key in a manifest file
TOP_LEVEL_KEY = "spack"

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
    "needs": {
        "type": "array",
        "description": "Groups of specs that are needed by this group",
        "items": {"type": "string"},
    },
    "override": {
        "type": "object",
        "description": "Top-most configuration scope for this group of specs",
        "additionalProperties": False,
        "properties": {**spack.schema.merged.properties},
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
            **spack.schema.merged.properties,
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
}


def update(data: Dict[str, Any]) -> bool:
    """Update the spack.yaml data in place to remove deprecated properties.

    Args:
        data: dictionary to be updated

    Returns:
        ``True`` if data was changed, ``False`` otherwise
    """
    # There are not currently any deprecated attributes in this section
    # that have not been removed
    return False
