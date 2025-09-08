# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for bootstrap.yaml configuration file."""
from typing import Any, Dict

#: Schema of a single source
_source_schema: Dict[str, Any] = {
    "type": "object",
    "description": "Bootstrap source configuration",
    "properties": {
        "name": {
            "type": "string",
            "description": "Name of the bootstrap source (e.g., 'github-actions-v0.6', "
            "'spack-install')",
        },
        "metadata": {
            "type": "string",
            "description": "Path to metadata directory containing bootstrap source configuration",
        },
    },
    "additionalProperties": False,
    "required": ["name", "metadata"],
}

properties: Dict[str, Any] = {
    "bootstrap": {
        "type": "object",
        "description": "Configure how Spack bootstraps its own dependencies when needed",
        "properties": {
            "enable": {
                "type": "boolean",
                "description": "Enable or disable bootstrapping entirely",
            },
            "root": {
                "type": "string",
                "description": "Where to install bootstrapped dependencies",
            },
            "sources": {
                "type": "array",
                "items": _source_schema,
                "description": "List of bootstrap sources tried in order. Each method may "
                "bootstrap different software depending on its type (e.g., pre-built binaries, "
                "source builds)",
            },
            "trusted": {
                "type": "object",
                "additionalProperties": {"type": "boolean"},
                "description": "Controls which sources are enabled for automatic bootstrapping",
            },
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack bootstrap configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
