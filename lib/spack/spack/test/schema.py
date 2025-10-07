# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import importlib
import os

import pytest

from spack.vendor import jsonschema

import spack.schema
import spack.util.spack_yaml as syaml
from spack.llnl.util.lang import list_modules

_draft_07_with_spack_extensions = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://json-schema.org/draft-07/schema#",
    "title": "Core schema meta-schema",
    "definitions": {
        "schemaArray": {"type": "array", "minItems": 1, "items": {"$ref": "#"}},
        "nonNegativeInteger": {"type": "integer", "minimum": 0},
        "nonNegativeIntegerDefault0": {
            "allOf": [{"$ref": "#/definitions/nonNegativeInteger"}, {"default": 0}]
        },
        "simpleTypes": {
            "enum": ["array", "boolean", "integer", "null", "number", "object", "string"]
        },
        "stringArray": {
            "type": "array",
            "items": {"type": "string"},
            "uniqueItems": True,
            "default": [],
        },
    },
    "type": ["object", "boolean"],
    "properties": {
        "$id": {"type": "string", "format": "uri-reference"},
        "$schema": {"type": "string", "format": "uri"},
        "$ref": {"type": "string", "format": "uri-reference"},
        "$comment": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "default": True,
        "readOnly": {"type": "boolean", "default": False},
        "writeOnly": {"type": "boolean", "default": False},
        "examples": {"type": "array", "items": True},
        "multipleOf": {"type": "number", "exclusiveMinimum": 0},
        "maximum": {"type": "number"},
        "exclusiveMaximum": {"type": "number"},
        "minimum": {"type": "number"},
        "exclusiveMinimum": {"type": "number"},
        "maxLength": {"$ref": "#/definitions/nonNegativeInteger"},
        "minLength": {"$ref": "#/definitions/nonNegativeIntegerDefault0"},
        "pattern": {"type": "string", "format": "regex"},
        "additionalItems": {"$ref": "#"},
        "items": {
            "anyOf": [{"$ref": "#"}, {"$ref": "#/definitions/schemaArray"}],
            "default": True,
        },
        "maxItems": {"$ref": "#/definitions/nonNegativeInteger"},
        "minItems": {"$ref": "#/definitions/nonNegativeIntegerDefault0"},
        "uniqueItems": {"type": "boolean", "default": False},
        "contains": {"$ref": "#"},
        "maxProperties": {"$ref": "#/definitions/nonNegativeInteger"},
        "minProperties": {"$ref": "#/definitions/nonNegativeIntegerDefault0"},
        "required": {"$ref": "#/definitions/stringArray"},
        "additionalProperties": {"$ref": "#"},
        "definitions": {"type": "object", "additionalProperties": {"$ref": "#"}, "default": {}},
        "properties": {"type": "object", "additionalProperties": {"$ref": "#"}, "default": {}},
        "patternProperties": {
            "type": "object",
            "additionalProperties": {"$ref": "#"},
            "propertyNames": {"format": "regex"},
            "default": {},
        },
        "dependencies": {
            "type": "object",
            "additionalProperties": {
                "anyOf": [{"$ref": "#"}, {"$ref": "#/definitions/stringArray"}]
            },
        },
        "propertyNames": {"$ref": "#"},
        "const": True,
        "enum": {"type": "array", "items": True, "minItems": 1, "uniqueItems": True},
        "type": {
            "anyOf": [
                {"$ref": "#/definitions/simpleTypes"},
                {
                    "type": "array",
                    "items": {"$ref": "#/definitions/simpleTypes"},
                    "minItems": 1,
                    "uniqueItems": True,
                },
            ]
        },
        "format": {"type": "string"},
        "contentMediaType": {"type": "string"},
        "contentEncoding": {"type": "string"},
        "if": {"$ref": "#"},
        "then": {"$ref": "#"},
        "else": {"$ref": "#"},
        "allOf": {"$ref": "#/definitions/schemaArray"},
        "anyOf": {"$ref": "#/definitions/schemaArray"},
        "oneOf": {"$ref": "#/definitions/schemaArray"},
        "not": {"$ref": "#"},
        # What follows is two Spack extensions to JSON Schema Draft 7:
        # deprecatedProperties and additionalKeysAreSpecs
        "deprecatedProperties": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                        "uniqueItems": True,
                    },
                    "message": {"type": "string"},
                    "error": {"type": "boolean"},
                },
                "required": ["names", "message"],
                "additionalProperties": False,
            },
        },
        "additionalKeysAreSpecs": {"type": "boolean"},
    },
    "default": True,
    # note: not in draft-07, this is for catching typos
    "additionalProperties": False,
}


@pytest.fixture()
def validate_spec_schema():
    return {
        "type": "object",
        "additionalKeysAreSpecs": True,
        "patternProperties": {r"\w[\w-]*": {"type": "string"}},
    }


@pytest.fixture()
def module_suffixes_schema():
    return {
        "type": "object",
        "properties": {
            "tcl": {
                "type": "object",
                "patternProperties": {
                    r"\w[\w-]*": {
                        "type": "object",
                        "properties": {
                            "suffixes": {
                                "additionalKeysAreSpecs": True,
                                "patternProperties": {r"\w[\w-]*": {"type": "string"}},
                            }
                        },
                    }
                },
            }
        },
    }


@pytest.mark.regression("9857")
def test_validate_spec(validate_spec_schema):
    v = spack.schema.Validator(validate_spec_schema)
    data = {"foo@3.7": "bar"}

    # Validate good data (the key is a spec)
    v.validate(data)

    # Check that invalid data throws
    data["^python@3.7@"] = "baz"
    with pytest.raises(jsonschema.ValidationError, match="is not a valid spec"):
        v.validate(data)


@pytest.mark.regression("9857")
def test_module_suffixes(module_suffixes_schema):
    v = spack.schema.Validator(module_suffixes_schema)
    data = {"tcl": {"all": {"suffixes": {"^python@2.7@": "py2.7"}}}}

    with pytest.raises(jsonschema.ValidationError, match="is not a valid spec"):
        v.validate(data)


def test_deprecated_properties(module_suffixes_schema):
    # Test that an error is reported when 'error: True'
    msg_fmt = r"{name} is deprecated"
    module_suffixes_schema["deprecatedProperties"] = [
        {"names": ["tcl"], "message": msg_fmt, "error": True}
    ]
    v = spack.schema.Validator(module_suffixes_schema)
    data = {"tcl": {"all": {"suffixes": {"^python": "py"}}}}

    expected_match = "tcl is deprecated"
    with pytest.raises(jsonschema.ValidationError, match=expected_match):
        v.validate(data)

    # Test that just a warning is reported when 'error: False'
    module_suffixes_schema["deprecatedProperties"] = [
        {"names": ["tcl"], "message": msg_fmt, "error": False}
    ]
    v = spack.schema.Validator(module_suffixes_schema)
    data = {"tcl": {"all": {"suffixes": {"^python": "py"}}}}
    # The next validation doesn't raise anymore
    v.validate(data)


def test_ordereddict_merge_order():
    """ "Test that source keys come before dest keys in merge_yaml results."""
    source = syaml.syaml_dict([("k1", "v1"), ("k2", "v2"), ("k3", "v3")])

    dest = syaml.syaml_dict([("k4", "v4"), ("k3", "WRONG"), ("k5", "v5")])

    result = spack.schema.merge_yaml(dest, source)
    assert "WRONG" not in result.values()

    expected_keys = ["k1", "k2", "k3", "k4", "k5"]
    expected_items = [("k1", "v1"), ("k2", "v2"), ("k3", "v3"), ("k4", "v4"), ("k5", "v5")]
    assert expected_keys == list(result.keys())
    assert expected_items == list(result.items())


def test_list_merge_order():
    """ "Test that source lists are prepended to dest."""
    source = ["a", "b", "c"]
    dest = ["d", "e", "f"]

    result = spack.schema.merge_yaml(dest, source)

    assert ["a", "b", "c", "d", "e", "f"] == result


def test_spack_schemas_are_valid():
    """Test that the Spack schemas in spack.schema.*.schema are valid under JSON Schema Draft 7
    with Spack extensions *only*."""
    # Collect schema submodules, and verify we have at least a few known ones
    schema_submodules = (
        importlib.import_module(f"spack.schema.{name}")
        for name in list_modules(os.path.dirname(spack.schema.__file__))
    )
    schemas = {m.__name__: m.schema for m in schema_submodules if hasattr(m, "schema")}
    assert set(schemas) >= {"spack.schema.config", "spack.schema.packages", "spack.schema.modules"}

    # Validate them using the meta-schema
    for module_name, module_schema in schemas.items():
        try:
            jsonschema.validate(module_schema, _draft_07_with_spack_extensions)
        except jsonschema.ValidationError as e:
            raise RuntimeError(f"Invalid JSON schema in {module_name}: {e.message}") from e
