# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for gitlab-ci.yaml configuration file.

.. literalinclude:: ../spack/schema/ci.py
   :lines: 13-
"""

from llnl.util.lang import union_dicts

import spack.schema.cdash

remove_attributes_schema = {
    "type": "object",
    "additionalProperties": False,
    "required": ["tags"],
    "properties": {
        "tags": {"type": "array", "items": {"type": "string"}},
    },
}


attributes_schema = {
    "type": "object",
}

jobconfig_schema = {
    "anyOf": [
        # Global generated job attributes, apply to all jobs
        {
            "type": "object",
            "additionalProperties": False,
            "required": ["any-job"],
            "properties": {
                "any-job": attributes_schema,
            },
        },
        attributes_schema,
        # Attributes applied to jobs based on type
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "build-job": attributes_schema,
                "reindex-job": attributes_schema,
                "noop-job": attributes_schema,
                "cleanup-job": attributes_schema,
                "signing-job": attributes_schema,
            },
        },
        # Attributes applied to spec-specific jobs based on spec matching
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "match_behavior": {
                    "type": "string",
                    "enum": ["first", "merge"],
                    "default": "first",
                },
                "submapping": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["match"],
                        "additionalProperties": False,
                        "properties": {
                            "match": {
                                "anyOf": [
                                    {"type": "string"},
                                    {"type": "array", "items": {"type": "string"}},
                                ]
                            },
                            "build-job-remove": remove_attributes_schema,
                            "build-job": attributes_schema,
                        },
                    },
                },
            },
        },
    ]
}

core_shared_properties = union_dicts(
    {
        "bootstrap": {
            "type": "array",
            "items": {
                "anyOf": [
                    {
                        "type": "string",
                    },
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["name"],
                        "properties": {
                            "name": {
                                "type": "string",
                            },
                            "compiler-agnostic": {
                                "type": "boolean",
                                "default": False,
                            },
                        },
                    },
                ],
            },
        },
        "pipeline-attributes": {"type": "object"},
        "build-if-matches": {
            "anyOf": [{"type": "null"}, {"type": "array", "items": {"type": "string"}}]
        },
        "job-configuration": {"type": "array", "items": jobconfig_schema},
        "rebuild-index": {"type": "boolean"},
        "broken-specs-url": {"type": "string"},
        "broken-tests-packages": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
        "cdash": spack.schema.cdash.properties,
    },
)

ci_properties = {
    "anyOf": [
        {
            "type": "object",
            "additionalProperties": False,
            "properties": union_dicts(
                core_shared_properties,
                {
                    "enable-artifacts-buildcache": {
                        "type": "boolean",
                    },
                },
            ),
        },
        {
            "type": "object",
            "additionalProperties": False,
            "properties": union_dicts(
                core_shared_properties,
                {
                    "temporary-storage-url-prefix": {
                        "type": "string",
                    },
                },
            ),
        },
    ]
}

#: Properties for inclusion in other schemas
properties = {
    "ci": ci_properties,
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack CI configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
