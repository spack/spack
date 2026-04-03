# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for env.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/env.py
   :lines: 19-
"""

import os
from typing import Any, Dict

import spack.schema.merged

#: Top level key in a manifest file
TOP_LEVEL_KEY = "spack"

# (DEPRECATED) include concrete entries to be merged under the include key
include_concrete = {
    "type": "array",
    "default": [],
    "description": "List of paths to other environments. Includes concrete specs "
    "from their spack.lock files without modifying the source environments. Useful "
    "for phased deployments where you want to build on existing concrete specs.",
    "items": {"type": "string"},
}


properties: Dict[str, Any] = {
    "spack": {
        "type": "object",
        "default": {},
        "description": "Spack environment configuration, including specs, view, and any other "
        "config section (config, packages, concretizer, mirrors, etc.)",
        "additionalProperties": False,
        "properties": {
            # merged configuration scope schemas
            **spack.schema.merged.ref_sections,
            # extra environment schema properties
            # (DEPRECATED) include concrete to be merged under the include key
            "include_concrete": include_concrete,
            # nested environments
            "spack": {"$ref": "#/spack/properties"},
        },
    }
}

schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack environment file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
    "definitions": spack.schema.merged.defs,
}


def update(data: Dict[str, Any]) -> bool:
    """Update the spack.yaml data to the new format.

    Args:
        data: dictionary to be updated

    Returns:
        ``True`` if data was changed, ``False`` otherwise
    """
    if not isinstance(data, dict):
        return False

    if "include_concrete" not in data:
        return False

    # Move the old 'include_concrete' paths to reside under the 'include',
    # ensuring that the lock file name is appended.
    includes = []
    for path in data["include_concrete"]:
        if os.path.basename(path) != "spack.lock":
            path = os.path.join(path, "spack.lock")
        includes.append(path)

    # Now add back the includes the environment file already has.
    if "include" in data:
        for path in data["include"]:
            includes.append(path)

    data["include"] = includes
    del data["include_concrete"]

    return True
