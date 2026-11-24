# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for projections.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/projections.py
   :lines: 14-
"""

from typing import Any, Dict

#: Properties for inclusion in other schemas
projections: Dict[str, Any] = {
    "type": "object",
    "description": "Customize directory structure and naming schemes by mapping specs to "
    "format strings.",
    "properties": {
        "all": {
            "type": "string",
            "description": "Default projection format string used as fallback for all specs "
            "that do not match other entries. Uses spec format syntax like "
            '"{name}/{version}/{hash:16}".',
        }
    },
    "additionalKeysAreSpecs": True,
    "additionalProperties": {
        "type": "string",
        "description": "Projection format string for specs matching this key. Uses spec "
        "format syntax supporting tokens like {name}, {version}, {compiler.name}, "
        "{^dependency.name}, etc.",
    },
}


#: $ref pointer for use in merged schema
ref_properties: Dict[str, Any] = {"projections": {"$ref": "#/definitions/projections"}}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack view projection configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": ref_properties,
    "definitions": {"projections": projections},
}
