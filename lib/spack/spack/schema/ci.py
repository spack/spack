# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for gitlab-ci.yaml configuration file.

.. literalinclude:: ../spack/schema/ci.py
   :lines: 13-
"""

from llnl.util.lang import union_dicts

# Schema for script fields
# List of lists and/or strings
# This is similar to what is allowed in
# the gitlab schema
script_schema = {
    "type": "array",
    "items": {"anyOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
}

# Additional attributes are allow
# and will be forwarded directly to the
# CI target YAML for each job.
attributes_schema = {
    "type": "object",
    "properties": {
        "image": {
            "oneOf": [
                {"type": "string"},
                {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "entrypoint": {"type": "array", "items": {"type": "string"}},
                    },
                },
            ]
        },
        "tags": {"type": "array", "items": {"type": "string"}},
        "variables": {
            "type": "object",
            "patternProperties": {r"[\w\d\-_\.]+": {"type": "string"}},
        },
        "before_script": script_schema,
        "script": script_schema,
        "after_script": script_schema,
    },
}

submapping_schema = {
    "type": "object",
    "additinoalProperties": False,
    "required": ["submapping"],
    "properties": {
        "match_behavior": {"type": "string", "enum": ["first", "merge"], "default": "first"},
        "submapping": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["match"],
                "properties": {
                    "match": {"type": "array", "items": {"type": "string"}},
                    "build-job": attributes_schema,
                    "build-job-remove": attributes_schema,
                },
            },
        },
    },
}

named_attributes_schema = {
    "oneOf": [
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {"noop-job": attributes_schema, "noop-job-remove": attributes_schema},
        },
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {"build-job": attributes_schema, "build-job-remove": attributes_schema},
        },
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "reindex-job": attributes_schema,
                "reindex-job-remove": attributes_schema,
            },
        },
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "signing-job": attributes_schema,
                "signing-job-remove": attributes_schema,
            },
        },
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "cleanup-job": attributes_schema,
                "cleanup-job-remove": attributes_schema,
            },
        },
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {"any-job": attributes_schema, "any-job-remove": attributes_schema},
        },
    ]
}

pipeline_gen_schema = {
    "type": "array",
    "items": {"oneOf": [submapping_schema, named_attributes_schema]},
}

core_shared_properties = union_dicts(
    {
        "pipeline-gen": pipeline_gen_schema,
        "bootstrap": {
            "type": "array",
            "items": {
                "anyOf": [
                    {"type": "string"},
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["name"],
                        "properties": {
                            "name": {"type": "string"},
                            "compiler-agnostic": {"type": "boolean", "default": False},
                        },
                    },
                ]
            },
        },
        "rebuild-index": {"type": "boolean"},
        "broken-specs-url": {"type": "string"},
        "broken-tests-packages": {"type": "array", "items": {"type": "string"}},
        "target": {"type": "string", "enum": ["gitlab"], "default": "gitlab"},
    }
)

ci_properties = {
    "anyOf": [
        {
            "type": "object",
            "additionalProperties": False,
            # "required": ["mappings"],
            "properties": union_dicts(
                core_shared_properties, {"enable-artifacts-buildcache": {"type": "boolean"}}
            ),
        },
        {
            "type": "object",
            "additionalProperties": False,
            # "required": ["mappings"],
            "properties": union_dicts(
                core_shared_properties, {"temporary-storage-url-prefix": {"type": "string"}}
            ),
        },
    ]
}

#: Properties for inclusion in other schemas
properties = {"ci": ci_properties}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack CI configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
