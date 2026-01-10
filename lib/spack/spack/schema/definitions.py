# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for definitions

.. literalinclude:: _spack_root/lib/spack/spack/schema/definitions.py
   :lines: 16-
"""
from typing import Any, Dict

from .spec_list import spec_list_schema

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
            "additionalProperties": spec_list_schema,
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
