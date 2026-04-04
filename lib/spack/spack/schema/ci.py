# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for gitlab-ci.yaml configuration file.

.. literalinclude:: ../spack/schema/ci.py
   :lines: 16-
"""
from typing import Any, Dict

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

# Additional attributes are allowed and will be forwarded directly to the CI target YAML for each
# job.
ci_job_attributes = {
    "type": "object",
    "additionalProperties": True,
    "properties": {
        "image": image_schema,
        "tags": {"type": "array", "items": {"type": "string"}},
        "variables": {
            "type": "object",
            "patternProperties": {r"^[\w\-\.]+$": {"type": ["string", "number"]}},
        },
        "before_script": script_schema,
        "script": script_schema,
        "after_script": script_schema,
    },
}

ref_ci_job_attributes = {"$ref": "#/definitions/ci_job_attributes"}

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
                    "build-job": ref_ci_job_attributes,
                    "build-job-remove": ref_ci_job_attributes,
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
                # "endpoint" cannot have http patternProperties constraint since it is required
                # Constrain is applied in code
                "endpoint": {"type": "string"},
                "timeout": {"type": "integer", "minimum": 0},
                "verify_ssl": {"type": "boolean", "default": False},
                "header": {"type": "object", "additionalProperties": {"type": "string"}},
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
        "properties": {
            f"{name}-job": ref_ci_job_attributes,
            f"{name}-job-remove": ref_ci_job_attributes,
        },
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

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "ci": {
        "type": "object",
        "properties": {
            "pipeline-gen": pipeline_gen_schema,
            "rebuild-index": {"type": "boolean"},
            "broken-specs-url": {"type": "string"},
            "broken-tests-packages": {"type": "array", "items": {"type": "string"}},
            "target": {"type": "string", "default": "gitlab"},
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack CI configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "definitions": {"ci_job_attributes": ci_job_attributes},
    "properties": properties,
}
