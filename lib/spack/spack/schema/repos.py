# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for repos.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/repos.py
   :lines: 18-
"""
from typing import Any, Dict

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "repos": {
        "oneOf": [
            {
                # old format: array of paths
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "Path to a Spack package repository directory",
                },
            },
            {
                # new format: dict of namespace => path
                "type": "object",
                "additionalProperties": {
                    "type": "string",
                    "description": "Path to a Spack package repository directory",
                },
            },
        ],
        "default": {},
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


def update(data: Dict[str, Any]) -> bool:
    """Update the repos.yaml configuration data to the new format."""
    if not isinstance(data["repos"], list):
        return False

    from llnl.util import tty

    from spack.repo import from_path

    # Convert old format [paths...] to new format {namespace: path, ...}
    repos = {}
    for path in data["repos"]:
        try:
            repo = from_path(path)
        except Exception as e:
            tty.warn(f"package repository {path} is disabled due to: {e}")
            continue
        if repo.namespace is not None:
            repos[repo.namespace] = path

    data["repos"] = repos
    return True
