# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for concretizer.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/concretizer.py
   :lines: 12-
"""
from typing import Any, Dict

properties: Dict[str, Any] = {
    "concretizer": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "reuse": {
                "oneOf": [{"type": "boolean"}, {"type": "string", "enum": ["dependencies"]}]
            },
            "enable_node_namespace": {"type": "boolean"},
            "targets": {
                "type": "object",
                "properties": {
                    "host_compatible": {"type": "boolean"},
                    "granularity": {"type": "string", "enum": ["generic", "microarchitectures"]},
                },
            },
            "unify": {
                "oneOf": [{"type": "boolean"}, {"type": "string", "enum": ["when_possible"]}]
            },
            "duplicates": {
                "type": "object",
                "properties": {
                    "strategy": {"type": "string", "enum": ["none", "minimal", "full"]}
                },
            },
        },
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack concretizer configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
