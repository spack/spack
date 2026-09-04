# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for filter.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/filter.py
   :lines: 18-
"""

from typing import Any, Dict

import spack.schema.projections

projection_scheme = spack.schema.projections.projections

allow_block = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "allow": {"type": "array", "default": [], "items": {"type": "string"}},
        "block": {"type": "array", "default": [], "items": {"type": "string"}},
    },
}

packages_filter = {
    "default": "all",
    "oneOf": [{"type": "string", "enum": ["all", "externals_only"]}, allow_block],
}

properties: Dict[str, Any] = {
    "filter": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "properties": {
            "projections": projection_scheme,
            "concrete": {"type": "boolean", "default": True},
            "specs": allow_block,
            "packages": packages_filter,
            "config": allow_block,
        },
    }
}

schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack filter configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
