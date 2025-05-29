# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for toolchains.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/toolchains.py
   :lines: 13-
"""
from typing import Any, Dict

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "toolchains": {
        "type": "object",
        "default": {},
        "additionalProperties": {
            "oneOf": [
                {"type": "string"},
                {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"spec": {"type": "string"}, "when": {"type": "string"}},
                    },
                },
            ]
        },
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack toolchain configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
