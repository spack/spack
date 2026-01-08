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
        "description": "Spack's basic configuration options",
        "properties": {
            "flags": {
                "type": "object",
                "description": "Build flag configuration options",
                "properties": {
                    "keep_werror": {
                        "type": "string",
                        "enum": ["all", "specific", "none"],
                        "description": "Whether to keep -Werror flags active in package builds",
                    }
                },
            },
            "shared_linking": {
                "description": "Control how shared libraries are located at runtime on Linux",
                "anyOf": [
                    {"type": "string", "enum": ["rpath", "runpath"]},
                    {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["rpath", "runpath"],
                                "description": "Whether to use RPATH or RUNPATH for runtime "
                                "library search paths",
                            },
                            "bind": {
                                "type": "boolean",
                                "description": "Embed absolute paths of dependent libraries "
                                "directly in ELF binaries (experimental)",
                            },
                            "missing_library_policy": {
                                "enum": ["error", "warn", "ignore"],
                                "description": "How to handle missing dynamic libraries after "
                                "installation",
                            },
                        },
                    },
                ],
            },
            "install_tree": {
                "type": "object",
                "description": "Installation tree configuration",
                "properties": {
                    "root": {
                        "type": "string",
                        "description": "The location where Spack will install packages and "
                        "their dependencies",
                    },
                    "padded_length": {
                        "oneOf": [{"type": "integer", "minimum": 0}, {"type": "boolean"}],
                        "description": "Length to pad installation paths to allow better "
                        "relocation of binaries (true for max length, integer for specific "
                        "length)",
                    },
                    **spack.schema.projections.properties,
                },
            },
            "install_hash_length": {
                "type": "integer",
                "minimum": 1,
                "description": "Length of hash used in installation directory names",
            },
            "build_stage": {
                "oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}],
                "description": "Temporary locations Spack can try to use for builds",
            },
            "stage_name": {
                "type": "string",
                "description": "Name format for build stage directories",
            },
            "develop_stage_link": {
                "type": "string",
                "description": "Name for development spec build stage directories",
            },
            "test_stage": {
                "type": "string",
                "description": "Directory in which to run tests and store test results",
            },
            "extensions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of Spack extensions to load",
            },
            "template_dirs": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Locations where templates should be found",
            },
            "license_dir": {
                "type": "string",
                "description": "Directory where licenses should be located",
            },
            "source_cache": {
                "type": "string",
                "description": "Location to cache downloaded tarballs and repositories",
            },
            "misc_cache": {
                "type": "string",
                "description": "Temporary directory to store long-lived cache files, such as "
                "indices of packages",
            },
            "environments_root": {
                "type": "string",
                "description": "Directory where Spack managed environments are created and stored",
            },
            "connect_timeout": {
                "type": "integer",
                "minimum": 0,
                "description": "Abort downloads after this many seconds if no data is received "
                "(0 disables timeout)",
            },
            "verify_ssl": {
                "type": "boolean",
                "description": "When true, Spack will verify certificates of remote hosts when "
                "making SSL connections",
            },
            "ssl_certs": {
                "type": "string",
                "description": "Path to custom certificates for SSL verification",
            },
            "suppress_gpg_warnings": {
                "type": "boolean",
                "description": "Suppress GPG warnings from binary package verification",
            },
            "debug": {
                "type": "boolean",
                "description": "Enable debug mode for additional logging",
            },
            "checksum": {
                "type": "boolean",
                "description": "When true, Spack verifies downloaded source code using checksums",
            },
            "deprecated": {
                "type": "boolean",
                "description": "If true, Spack will fetch deprecated versions without warning",
            },
            "locks": {
                "type": "boolean",
                "description": "When true, concurrent instances of Spack will use locks to avoid "
                "conflicts (strongly recommended)",
            },
            "dirty": {
                "type": "boolean",
                "description": "When true, builds will NOT clean potentially harmful variables "
                "from the environment",
            },
            "build_language": {
                "type": "string",
                "description": "The language the build environment will use (C for English, "
                "empty string for user's environment)",
            },
            "build_jobs": {
                "type": "integer",
                "minimum": 1,
                "description": "The maximum number of jobs to use for the build system (e.g. "
                "make -j), defaults to 16",
            },
            "concurrent_packages": {
                "type": "integer",
                "minimum": 1,
                "description": "The maximum number of concurrent package builds a single Spack "
                "instance will run",
            },
            "ccache": {
                "type": "boolean",
                "description": "When true, Spack's compiler wrapper will use ccache when "
                "compiling C and C++",
            },
            "db_lock_timeout": {
                "type": "integer",
                "minimum": 1,
                "description": "How long to wait to lock the Spack installation database",
            },
            "package_lock_timeout": {
                "anyOf": [{"type": "integer", "minimum": 1}, {"type": "null"}],
                "description": "How long to wait when attempting to modify a package (null for "
                "never timeout)",
            },
            "allow_sgid": {
                "type": "boolean",
                "description": "Allow installation on filesystems that don't allow setgid bit "
                "manipulation",
            },
            "install_status": {
                "type": "boolean",
                "description": "Whether to show status information in the terminal title during "
                "the build",
            },
            "url_fetch_method": {
                "anyOf": [{"enum": ["urllib", "curl"]}, {"type": "string", "pattern": r"^curl "}],
                "description": "The default URL fetch method to use (urllib or curl)",
            },
            "additional_external_search_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Additional paths to search for external packages",
            },
            "binary_index_ttl": {
                "type": "integer",
                "minimum": 0,
                "description": "Number of seconds a buildcache's index.json is cached locally "
                "before probing for updates",
            },
            "aliases": {
                "type": "object",
                "additionalProperties": {"type": "string"},
                "description": "A mapping of aliases that can be used to define new "
                "Spack commands",
            },
            "installer": {
                "type": "string",
                "enum": ["old", "new"],
                "description": "Which installer to use. The new installer is experimental.",
            },
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
