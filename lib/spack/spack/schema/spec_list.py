# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
matrix_schema = {
    "type": "array",
    "description": "List of spec constraint lists whose cross product generates multiple specs",
    "items": {
        "type": "array",
        "description": "List of spec constraints for this matrix dimension",
        "items": {"type": "string"},
    },
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


spec_list_properties = {
    "matrix": matrix_schema,
    "exclude": {
        "type": "array",
        "description": "List of specific spec combinations to exclude from the matrix",
        "items": {"type": "string"},
    },
}

spec_list_schema = {
    "type": "array",
    "description": "List of specs to include in the environment, supporting both simple specs and "
    "matrix configurations",
    "default": [],
    "items": {
        "anyOf": [
            {
                "type": "object",
                "description": "Matrix configuration for generating multiple specs from "
                "combinations of constraints",
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
}
