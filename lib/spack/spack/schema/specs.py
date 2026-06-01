# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for specs.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/specs.py
   :lines: 14-
"""

from typing import Any, Dict

from .definitions import definition_list_options, matrix_properties
from .merged_no_specs import ref_sections


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
        "properties": {**ref_sections},
    },
}


spec_list_options = definition_list_options + [
    {
        "type": "object",
        "description": "User spec group with a single matrix",
        "additionalProperties": False,
        "properties": {**matrix_properties, **group_name_and_deps},
    },
    {
        "type": "object",
        "description": "User spec group with multiple matrices",
        "additionalProperties": False,
        "properties": {**group_name_and_deps, "specs": {"$ref": "#/definitions/spec_list_schema"}}
    },
]


spec_list_schema = {
    "type": "array",
    "description": "List of specs to include in the environment, supporting both simple specs and "
    "matrix configurations",
    "default": [],
    "items": {"anyOf": spec_list_options},
}


properties: Dict[str, Any] = {"specs": spec_list_schema}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack specs configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
    "definitions": {"spec_list_schema": spec_list_schema},
}
