# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for gitlab-ci.yaml configuration file.

.. literalinclude:: ../spack/schema/ci.py
   :lines: 16-
"""
from typing import Any, Dict

from llnl.util.lang import union_dicts

import spack.schema.gitlab_ci

# Schema for script fields
# List of lists and/or strings
# This is similar to what is allowed in
# the gitlab schema
script_schema = {
    "type": "array",
    "items": {"anyOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
}

# Schema for CI image
image_schema = {
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
}

# Additional attributes are allow
# and will be forwarded directly to the
# CI target YAML for each job.
attributes_schema = {
    "type": "object",
    "additionalProperties": True,
    "properties": {
        "image": image_schema,
        "tags": {"type": "array", "items": {"type": "string"}},
        "variables": {
            "type": "object",
            "patternProperties": {r"[\w\d\-_\.]+": {"type": ["string", "number"]}},
        },
        "before_script": script_schema,
        "script": script_schema,
        "after_script": script_schema,
    },
}

submapping_schema = {
    "type": "object",
    "additionalProperties": False,
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

dynamic_mapping_schema = {
    "type": "object",
    "additionalProperties": False,
    "required": ["dynamic-mapping"],
    "properties": {
        "dynamic-mapping": {
            "type": "object",
            "required": ["endpoint"],
            "properties": {
                "name": {"type": "string"},
                # "endpoint" cannot have http patternProperties constaint as it is a required field
                # Constrain is applied in code
                "endpoint": {"type": "string"},
                "timeout": {"type": "integer", "minimum": 0},
                "verify_ssl": {"type": "boolean", "default": False},
                "header": {"type": "object", "additionalProperties": False},
                "allow": {"type": "array", "items": {"type": "string"}},
                "require": {"type": "array", "items": {"type": "string"}},
                "ignore": {"type": "array", "items": {"type": "string"}},
            },
        }
    },
}


def job_schema(name: str):
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {f"{name}-job": attributes_schema, f"{name}-job-remove": attributes_schema},
    }


pipeline_gen_schema = {
    "type": "array",
    "items": {
        "oneOf": [
            submapping_schema,
            dynamic_mapping_schema,
            job_schema("any"),
            job_schema("build"),
            job_schema("cleanup"),
            job_schema("copy"),
            job_schema("noop"),
            job_schema("reindex"),
            job_schema("signing"),
        ]
    },
}

core_shared_properties = union_dicts(
    {
        "pipeline-gen": pipeline_gen_schema,
        "rebuild-index": {"type": "boolean"},
        "broken-specs-url": {"type": "string"},
        "broken-tests-packages": {"type": "array", "items": {"type": "string"}},
        "target": {"type": "string", "enum": ["gitlab"], "default": "gitlab"},
    }
)

# TODO: Remove in Spack 0.23
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
properties: Dict[str, Any] = {
    "ci": {
        "oneOf": [
            # TODO: Replace with core-shared-properties in Spack 0.23
            ci_properties,
            # Allow legacy format under `ci` for `config update ci`
            spack.schema.gitlab_ci.gitlab_ci_properties,
        ]
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack CI configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}


def update(data):
    import llnl.util.tty as tty

    import spack.ci
    import spack.environment as ev

    # Warn if deprecated section is still in the environment
    ci_env = ev.active_environment()
    if ci_env:
        env_config = ci_env.manifest[ev.TOP_LEVEL_KEY]
        if "gitlab-ci" in env_config:
            tty.die("Error: `gitlab-ci` section detected with `ci`, these are not compatible")

    # Detect if the ci section is using the new pipeline-gen
    # If it is, assume it has already been converted
    return spack.ci.translate_deprecated_config(data)
