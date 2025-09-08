# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for config.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/config.py
   :lines: 17-
"""
from typing import Any, Dict

import spack.schema
import spack.schema.projections

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "config": {
        "type": "object",
        "default": {},
        "properties": {
            "flags": {
                "type": "object",
                "properties": {
                    "keep_werror": {"type": "string", "enum": ["all", "specific", "none"]}
                },
            },
            "shared_linking": {
                "anyOf": [
                    {"type": "string", "enum": ["rpath", "runpath"]},
                    {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "enum": ["rpath", "runpath"]},
                            "bind": {"type": "boolean"},
                            "missing_library_policy": {"enum": ["error", "warn", "ignore"]},
                        },
                    },
                ]
            },
            "install_tree": {
                "type": "object",
                "properties": {
                    "root": {"type": "string"},
                    "padded_length": {
                        "oneOf": [{"type": "integer", "minimum": 0}, {"type": "boolean"}]
                    },
                    **spack.schema.projections.properties,
                },
            },
            "concretization_cache": {
                "type": "object",
                "properties": {
                    "enable": {"type": "boolean"},
                    "url": {"type": "string"},
                    "entry_limit": {"type": "integer", "minimum": 0},
                    "size_limit": {"type": "integer", "minimum": 0},
                },
            },
            "install_hash_length": {"type": "integer", "minimum": 1},
            "build_stage": {
                "oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]
            },
            "stage_name": {"type": "string"},
            "develop_stage_link": {"type": "string"},
            "test_stage": {"type": "string"},
            "extensions": {"type": "array", "items": {"type": "string"}},
            "template_dirs": {"type": "array", "items": {"type": "string"}},
            "license_dir": {"type": "string"},
            "source_cache": {"type": "string"},
            "misc_cache": {"type": "string"},
            "environments_root": {"type": "string"},
            "connect_timeout": {"type": "integer", "minimum": 0},
            "verify_ssl": {"type": "boolean"},
            "ssl_certs": {"type": "string"},
            "suppress_gpg_warnings": {"type": "boolean"},
            "debug": {"type": "boolean"},
            "checksum": {"type": "boolean"},
            "deprecated": {"type": "boolean"},
            "locks": {"type": "boolean"},
            "dirty": {"type": "boolean"},
            "build_language": {"type": "string"},
            "build_jobs": {"type": "integer", "minimum": 1},
            "concurrent_packages": {"type": "integer", "minimum:": 1},
            "ccache": {"type": "boolean"},
            "db_lock_timeout": {"type": "integer", "minimum": 1},
            "package_lock_timeout": {
                "anyOf": [{"type": "integer", "minimum": 1}, {"type": "null"}]
            },
            "allow_sgid": {"type": "boolean"},
            "install_status": {"type": "boolean"},
            "binary_index_root": {"type": "string"},
            "url_fetch_method": {"type": "string", "pattern": r"^urllib$|^curl( .*)*"},
            "additional_external_search_paths": {"type": "array", "items": {"type": "string"}},
            "binary_index_ttl": {"type": "integer", "minimum": 0},
            "aliases": {"type": "object", "patternProperties": {r"\w[\w-]*": {"type": "string"}}},
        },
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack core configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}


def update(data: dict) -> bool:
    """Update the data in place to remove deprecated properties.

    Args:
        data: dictionary to be updated

    Returns: True if data was changed, False otherwise
    """
    changed = False
    data = data["config"]
    shared_linking = data.get("shared_linking", None)
    if isinstance(shared_linking, str):
        # deprecated short-form shared_linking: rpath/runpath
        # add value as `type` in updated shared_linking
        data["shared_linking"] = {"type": shared_linking, "bind": False}
        changed = True
    return changed
