# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for env.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/env.py
   :lines: 36-
"""
from llnl.util.lang import union_dicts

import spack.schema.gitlab_ci  # DEPRECATED
import spack.schema.merged
import spack.schema.packages
import spack.schema.projections

#: Top level key in a manifest file
TOP_LEVEL_KEY = "spack"

spec_list_schema = {
    "type": "array",
    "default": [],
    "items": {
        "anyOf": [
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "matrix": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "string"}},
                    },
                    "exclude": {"type": "array", "items": {"type": "string"}},
                },
            },
            {"type": "string"},
            {"type": "null"},
        ]
    },
}

projections_scheme = spack.schema.projections.properties["projections"]

schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack environment file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "spack": {
            "type": "object",
            "default": {},
            "additionalProperties": False,
            "properties": union_dicts(
                # Include deprecated "gitlab-ci" section
                spack.schema.gitlab_ci.properties,
                # merged configuration scope schemas
                spack.schema.merged.properties,
                # extra environment schema properties
                {
                    "include": {"type": "array", "default": [], "items": {"type": "string"}},
                    "develop": {
                        "type": "object",
                        "default": {},
                        "additionalProperties": False,
                        "patternProperties": {
                            r"\w[\w-]*": {
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "spec": {"type": "string"},
                                    "path": {"type": "string"},
                                },
                            }
                        },
                    },
                    "definitions": {
                        "type": "array",
                        "default": [],
                        "items": {
                            "type": "object",
                            "properties": {"when": {"type": "string"}},
                            "patternProperties": {r"^(?!when$)\w*": spec_list_schema},
                        },
                    },
                    "specs": spec_list_schema,
                    "view": {
                        "anyOf": [
                            {"type": "boolean"},
                            {"type": "string"},
                            {
                                "type": "object",
                                "patternProperties": {
                                    r"\w+": {
                                        "required": ["root"],
                                        "additionalProperties": False,
                                        "properties": {
                                            "root": {"type": "string"},
                                            "link": {
                                                "type": "string",
                                                "pattern": "(roots|all|run)",
                                            },
                                            "link_type": {"type": "string"},
                                            "select": {
                                                "type": "array",
                                                "items": {"type": "string"},
                                            },
                                            "exclude": {
                                                "type": "array",
                                                "items": {"type": "string"},
                                            },
                                            "projections": projections_scheme,
                                        },
                                    }
                                },
                            },
                        ]
                    },
                },
            ),
        }
    },
}


def update(data):
    """Update the data in place to remove deprecated properties.

    Args:
        data (dict): dictionary to be updated

    Returns:
        True if data was changed, False otherwise
    """

    import spack.ci

    if "gitlab-ci" in data:
        data["ci"] = data.pop("gitlab-ci")

    if "ci" in data:
        return spack.ci.translate_deprecated_config(data["ci"])

    # There are not currently any deprecated attributes in this section
    # that have not been removed
    return False
