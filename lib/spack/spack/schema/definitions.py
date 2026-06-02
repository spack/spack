# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for definitions

.. literalinclude:: _spack_root/lib/spack/spack/schema/definitions.py
   :lines: 16-
"""

from typing import Any, Dict

matrix_properties = {
    "matrix": {
        "type": "array",
        "description": "List of spec constraint lists whose cross product generate multiple specs",
        "items": {
            "type": "array",
            "description": "List of spec constraints for this matrix dimension",
            "items": {"type": "string"},
        },
    },
    "exclude": {
        "type": "array",
        "description": "List of specific spec combinations to exclude from the matrix",
        "items": {"type": "string"},
    },
}


definition_list_options = [
    {
        "type": "object",
        "description": "Matrix configuration for generating multiple specs from "
        "combinations of constraints",
        "additionalProperties": False,
        "properties": {**matrix_properties},
    },
    {"type": "string", "description": "Simple spec string"},
    {"type": "null"},
]


#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "definitions": {
        "type": "array",
        "default": [],
        "description": "Named spec lists to be referred to with $name in the specs section of "
        "environments",
        "items": {
            "type": "object",
            "description": "Named definition entry containing a named spec list and optional "
            "conditional 'when' clause",
            "properties": {
                "when": {
                    "type": "string",
                    "description": "Python code condition evaluated as boolean. Specs are "
                    "appended to the named list only if the condition is True. Available "
                    "variables: platform, os, target, arch, arch_str, re, env, hostname",
                }
            },
            "additionalProperties": {
                "type": "array",
                "description": "List of specs in a definition, supporting both simple specs and "
                "matrix configurations",
                "default": [],
                "items": {"anyOf": definition_list_options},
            },
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack definitions configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
