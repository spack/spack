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
                "properties": {
                    "matrix": matrix_schema,
                    "exclude": {
                        "type": "array",
                        "description": "List of specific spec combinations to exclude from the "
                        "matrix",
                        "items": {"type": "string"},
                    },
                },
            },
            {"type": "string", "description": "Simple spec string"},
            {"type": "null"},
        ]
    },
}
