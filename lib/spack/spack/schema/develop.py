# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Any, Dict

properties: Dict[str, Any] = {
    "develop": {
        "type": "object",
        "default": {},
        "description": "Configuration for local development of Spack packages",
        "additionalProperties": {
            "type": "object",
            "additionalProperties": False,
            "description": "Name of a package to develop, with its spec and optional "
            "source path",
            "required": ["spec"],
            "properties": {
                "spec": {
                    "type": "string",
                    "description": "Spec of the package to develop, e.g. hdf5@1.12.0",
                },
                "path": {
                    "type": "string",
                    "description": "Path to the source code for this package, can be "
                    "absolute or relative to the environment directory",
                },
            },
        },
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack repository configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
