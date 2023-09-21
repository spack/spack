# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for modules.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/modules.py
   :lines: 13-
"""
import spack.schema.environment
import spack.schema.projections

#: Matches a spec or a multi-valued variant but not another
#: valid keyword.
#:
#: THIS NEEDS TO BE UPDATED FOR EVERY NEW KEYWORD THAT
#: IS ADDED IMMEDIATELY BELOW THE MODULE TYPE ATTRIBUTE
SPEC_REGEX = (
    r"(?!hierarchy|core_specs|verbose|hash_length|defaults|filter_hierarchy_specs|"
    r"whitelist|blacklist|"  # DEPRECATED: remove in 0.20.
    r"include|exclude|"  # use these more inclusive/consistent options
    r"projections|naming_scheme|core_compilers|all)(^\w[\w-]*)"
)

#: Matches a valid name for a module set
VALID_MODULE_SET_NAME = r"^(?!prefix_inspections$)\w[\w-]*$"

#: Matches an anonymous spec, i.e. a spec without a root name
ANONYMOUS_SPEC_REGEX = r"^[\^@%+~]"

#: Definitions for parts of module schema
array_of_strings = {"type": "array", "default": [], "items": {"type": "string"}}

dictionary_of_strings = {"type": "object", "patternProperties": {r"\w[\w-]*": {"type": "string"}}}

dependency_selection = {"type": "string", "enum": ["none", "direct", "all"]}

module_file_configuration = {
    "type": "object",
    "default": {},
    "additionalProperties": False,
    "properties": {
        "filter": {
            "type": "object",
            "default": {},
            "additionalProperties": False,
            "properties": {
                # DEPRECATED: remove in 0.20.
                "environment_blacklist": {
                    "type": "array",
                    "default": [],
                    "items": {"type": "string"},
                },
                # use exclude_env_vars instead
                "exclude_env_vars": {"type": "array", "default": [], "items": {"type": "string"}},
            },
        },
        "template": {"type": "string"},
        "autoload": dependency_selection,
        "prerequisites": dependency_selection,
        "conflict": array_of_strings,
        "load": array_of_strings,
        "suffixes": {
            "type": "object",
            "validate_spec": True,
            "patternProperties": {r"\w[\w-]*": {"type": "string"}},  # key
        },
        "environment": spack.schema.environment.definition,
    },
}

projections_scheme = spack.schema.projections.properties["projections"]

module_type_configuration = {
    "type": "object",
    "default": {},
    "allOf": [
        {
            "properties": {
                "verbose": {"type": "boolean", "default": False},
                "hash_length": {"type": "integer", "minimum": 0, "default": 7},
                # DEPRECATED: remove in 0.20.
                "whitelist": array_of_strings,
                "blacklist": array_of_strings,
                "blacklist_implicits": {"type": "boolean", "default": False},
                # whitelist/blacklist have been replaced with include/exclude
                "include": array_of_strings,
                "exclude": array_of_strings,
                "exclude_implicits": {"type": "boolean", "default": False},
                "defaults": array_of_strings,
                "naming_scheme": {"type": "string"},  # Can we be more specific here?
                "projections": projections_scheme,
                "all": module_file_configuration,
            }
        },
        {
            "validate_spec": True,
            "patternProperties": {
                SPEC_REGEX: module_file_configuration,
                ANONYMOUS_SPEC_REGEX: module_file_configuration,
            },
        },
    ],
}


module_config_properties = {
    "use_view": {"anyOf": [{"type": "string"}, {"type": "boolean"}]},
    "arch_folder": {"type": "boolean"},
    "roots": {
        "type": "object",
        "properties": {"tcl": {"type": "string"}, "lmod": {"type": "string"}},
    },
    "enable": {
        "type": "array",
        "default": [],
        "items": {"type": "string", "enum": ["tcl", "lmod"]},
    },
    "lmod": {
        "allOf": [
            # Base configuration
            module_type_configuration,
            {
                "type": "object",
                "properties": {
                    "core_compilers": array_of_strings,
                    "hierarchy": array_of_strings,
                    "core_specs": array_of_strings,
                    "filter_hierarchy_specs": {
                        "type": "object",
                        "patternProperties": {SPEC_REGEX: array_of_strings},
                    },
                },
            },  # Specific lmod extensions
        ]
    },
    "tcl": {
        "allOf": [
            # Base configuration
            module_type_configuration,
            {},  # Specific tcl extensions
        ]
    },
    "prefix_inspections": {
        "type": "object",
        "additionalProperties": False,
        "patternProperties": {
            # prefix-relative path to be inspected for existence
            r"^[\w-]*": array_of_strings
        },
    },
}


# Properties for inclusion into other schemas (requires definitions)
properties = {
    "modules": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "prefix_inspections": {
                "type": "object",
                "additionalProperties": False,
                "patternProperties": {
                    # prefix-relative path to be inspected for existence
                    r"^[\w-]*": array_of_strings
                },
            }
        },
        "patternProperties": {
            VALID_MODULE_SET_NAME: {
                "type": "object",
                "default": {},
                "additionalProperties": False,
                "properties": module_config_properties,
            }
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack module file configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}
