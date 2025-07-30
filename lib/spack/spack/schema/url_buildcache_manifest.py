# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for buildcache entry manifest file

.. literalinclude:: _spack_root/lib/spack/spack/schema/url_buildcache_manifest.py
   :lines: 11-
"""
from typing import Any, Dict

properties: Dict[str, Any] = {
    "version": {"type": "integer"},
    "data": {
        "type": "array",
        "items": {
            "type": "object",
            "required": [
                "contentLength",
                "mediaType",
                "compression",
                "checksumAlgorithm",
                "checksum",
            ],
            "properties": {
                "contentLength": {"type": "integer"},
                "mediaType": {"type": "string"},
                "compression": {"type": "string"},
                "checksumAlgorithm": {"type": "string"},
                "checksum": {"type": "string"},
            },
            "additionalProperties": True,
        },
    },
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Buildcache manifest schema",
    "type": "object",
    "required": ["version", "data"],
    "additionalProperties": True,
    "properties": properties,
}
