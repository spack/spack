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
        "description": "Configuration for package repositories that Spack searches for packages",
        "oneOf": [
            {
                # old format: array of strings
                "type": "array",
                "items": {
                    "type": "string",
                    "description": "Path to a Spack package repository directory",
                },
                "description": "Legacy format: list of local paths to package repository "
                "directories",
            },
            {
                # new format: object with named repositories
                "type": "object",
                "description": "Named repositories mapping configuration names to repository "
                "definitions",
                "additionalProperties": {
                    "oneOf": [
                        {
                            # local path
                            "type": "string",
                            "description": "Path to a local Spack package repository directory "
                            "containing repo.yaml and packages/",
                        },
                        {
                            # remote git repository
                            "type": "object",
                            "properties": {
                                "git": {
                                    "type": "string",
                                    "description": "Git repository URL for remote package "
                                    "repository",
                                },
                                "branch": {
                                    "type": "string",
                                    "description": "Git branch name to checkout (default branch "
                                    "if not specified)",
                                },
                                "commit": {
                                    "type": "string",
                                    "description": "Specific git commit hash to pin the "
                                    "repository to",
                                },
                                "tag": {
                                    "type": "string",
                                    "description": "Git tag name to pin the repository to",
                                },
                                "destination": {
                                    "type": "string",
                                    "description": "Custom local directory path where the Git "
                                    "repository should be cloned",
                                },
                                "paths": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of relative paths (from the Git "
                                    "repository root) that contain Spack package repositories "
                                    "(overrides spack-repo-index.yaml)",
                                },
                            },
                            "additionalProperties": False,
                        },
                    ]
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

    from spack.llnl.util import tty
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
