# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for include.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/include.py
   :lines: 12-
"""
from typing import Any, Dict

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "include": {
        "type": "array",
        "default": [],
        "additionalProperties": False,
        "description": "Include external configuration files to pull in configuration from "
        "other files/URLs for modular and reusable configurations",
        "items": {
            "anyOf": [
                # local, required path
                {
                    "type": "string",
                    "description": "Simple include entry specifying path to required "
                    "configuration file/directory",
                },
                # local or remote paths that may be optional or conditional
                {
                    "type": "object",
                    "description": "Advanced include entry with optional conditions and "
                    "remote file support",
                    "properties": {
                        "when": {
                            "type": "string",
                            "description": "Include this config only when the condition (as "
                            "Python code) evaluates to true",
                        },
                        "name": {"type": "string"},
                        "path_override_env_var": {"type": "string"},
                        "path": {
                            "type": "string",
                            "description": "Path to configuration file/directory (absolute, "
                            "relative, or URL). URLs must be raw file content (GitHub/GitLab "
                            "raw form). Supports file, ftp, http, https schemes and "
                            "Spack/environment variables",
                        },
                        "sha256": {
                            "type": "string",
                            "description": "Required SHA256 hash for remote URLs to verify "
                            "file integrity",
                        },
                        "optional": {
                            "type": "boolean",
                            "description": "If true, include only if path exists; if false "
                            "(default), path is required and missing files cause errors",
                        },
                        "prefer_modify": {"type": "boolean"},
                    },
                    "required": ["path"],
                    "additionalProperties": False,
                },
                # remote git paths that may be optional or conditional
                {
                    "type": "object",
                    "description": "Include configuration files from a git repository with "
                    "conditional and optional support",
                    "properties": {
                        "git": {
                            "type": "string",
                            "description": "URL of the git repository to clone (e.g., "
                            "https://github.com/spack/spack-configs)",
                        },
                        "branch": {
                            "type": "string",
                            "description": "Branch to check out from the repository",
                        },
                        "commit": {
                            "type": "string",
                            "description": "Specific commit SHA to check out from the repository",
                        },
                        "tag": {
                            "type": "string",
                            "description": "Tag to check out from the repository",
                        },
                        "paths": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "Relative path within the repository to a "
                                "configuration file to include",
                            },
                            "description": "List of relative paths within the repository where "
                            "configuration files are located",
                        },
                        "when": {
                            "type": "string",
                            "description": "Include this config only when the condition (as "
                            "Python code) evaluates to true",
                        },
                        "optional": {
                            "type": "boolean",
                            "description": "If true, include only if repository is accessible; "
                            "if false (default), inaccessible repository causes errors",
                        },
                    },
                    "required": ["git", "paths"],
                    "additionalProperties": False,
                },
            ]
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack include configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
