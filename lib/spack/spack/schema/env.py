# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for env.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/env.py
   :lines: 36-
"""
import warnings

from llnl.util.lang import union_dicts

import spack.schema.merged
import spack.schema.packages
import spack.schema.projections

warned_about_concretization = False


def deprecate_concretization(instance, props):
    global warned_about_concretization
    if warned_about_concretization:
        return None
    # Deprecate `spack:concretization` in favor of `spack:concretizer:unify`.
    concretization_to_unify = {"together": "true", "separately": "false"}
    concretization = instance["concretization"]
    unify = concretization_to_unify[concretization]

    return (
        "concretization:{} is deprecated and will be removed in Spack 0.19 in favor of "
        "the new concretizer:unify:{} config option.".format(concretization, unify)
    )


#: legal first keys in the schema
keys = ("spack", "env")

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
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "string",
                            },
                        },
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
    "patternProperties": {
        "^env|spack$": {
            "type": "object",
            "default": {},
            "additionalProperties": False,
            "deprecatedProperties": {
                "properties": ["concretization"],
                "message": deprecate_concretization,
                "error": False,
            },
            "properties": union_dicts(
                # merged configuration scope schemas
                spack.schema.merged.properties,
                # extra environment schema properties
                {
                    "include": {
                        "type": "array",
                        "default": [],
                        "items": {"type": "string"},
                    },
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
                            },
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
                    "concretization": {
                        "type": "string",
                        "enum": ["together", "separately"],
                        "default": "separately",
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
    updated = False
    if "include" in data:
        msg = "included configuration files should be updated manually" " [files={0}]"
        warnings.warn(msg.format(", ".join(data["include"])))

    # Spack 0.19 drops support for `spack:concretization` in favor of
    # `spack:concretizer:unify`. Here we provide an upgrade path that changes the former
    # into the latter, or warns when there's an ambiguity. Note that Spack 0.17 is not
    # forward compatible with `spack:concretizer:unify`.
    if "concretization" in data:
        has_unify = "unify" in data.get("concretizer", {})
        to_unify = {"together": True, "separately": False}
        unify = to_unify[data["concretization"]]

        if has_unify and data["concretizer"]["unify"] != unify:
            warnings.warn(
                "The following configuration conflicts: "
                "`spack:concretization:{}` and `spack:concretizer:unify:{}`"
                ". Please update manually.".format(
                    data["concretization"], data["concretizer"]["unify"]
                )
            )
        else:
            data.update({"concretizer": {"unify": unify}})
            data.pop("concretization")
            updated = True

    return updated
