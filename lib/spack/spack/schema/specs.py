# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for specs.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/specs.py
   :lines: 14-
"""

from typing import Any, Dict

from .spec_list import group_name_and_deps, spec_list_properties, spec_list_schema

properties: Dict[str, Any] = {
    "specs": {
        "type": "array",
        "description": "List of specs, supporting both simple specs and matrix configurations",
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
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack specs configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
