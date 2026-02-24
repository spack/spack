# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for view

.. literalinclude:: _spack_root/lib/spack/spack/schema/view.py
   :lines: 15-
"""
from typing import Any, Dict

import spack.schema
import spack.schema.projections

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "view": {
        "description": "Environment filesystem view configuration for creating a directory with "
        "traditional structure where all files of installed packages are linked",
        "anyOf": [
            {
                "type": "boolean",
                "description": "Enable or disable default views. If 'true', the view is "
                "generated under .spack-env/view",
            },
            {"type": "string", "description": "Path where the default view should be created"},
            {
                "type": "object",
                "description": "Advanced view configuration with one or more named view "
                "descriptors",
                "additionalProperties": {
                    "description": "Named view descriptor (use 'default' for the view activated "
                    "with environment)",
                    "required": ["root"],
                    "additionalProperties": False,
                    "properties": {
                        "root": {
                            "type": "string",
                            "description": "Root directory path where the view will be " "created",
                        },
                        "link": {
                            "enum": ["roots", "all", "run"],
                            "description": "Which specs to include: 'all' (environment roots "
                            "with transitive run+link deps), 'run' (environment roots with "
                            "transitive run deps), 'roots' (environment roots only)",
                        },
                        "link_type": {
                            "type": "string",
                            "enum": ["symlink", "hardlink", "copy"],
                            "description": "How files are linked in the view: 'symlink' "
                            "(default), 'hardlink', or 'copy'",
                        },
                        "select": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of specs to include in the view "
                            "(default: select everything)",
                        },
                        "exclude": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of specs to exclude from the view "
                            "(default: exclude nothing)",
                        },
                        **spack.schema.projections.properties,
                    },
                },
            },
        ],
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack view configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
