# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for modules.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/modules.py
   :lines: 16-
"""
from typing import Any, Dict

import spack.schema.environment
import spack.schema.projections

#: Definitions for parts of module schema
array_of_strings = {"type": "array", "default": [], "items": {"type": "string"}}

dependency_selection = {"type": "string", "enum": ["none", "run", "direct", "all"]}

module_file_configuration = {
    "type": "object",
    "default": {},
    "description": "Configuration for individual module file behavior and content customization",
    "additionalProperties": False,
    "properties": {
        "filter": {
            "type": "object",
            "default": {},
            "description": "Filter out specific environment variable modifications from "
            "module files",
            "additionalProperties": False,
            "properties": {
                "exclude_env_vars": {
                    "type": "array",
                    "default": [],
                    "items": {"type": "string"},
                    "description": "List of environment variable names to exclude from module "
                    "file modifications",
                }
            },
        },
        "template": {
            "type": "string",
            "description": "Path to custom template file for generating module files",
        },
        "autoload": {
            **dependency_selection,
            "description": "Automatically load dependency modules when this module is loaded",
        },
        "prerequisites": {
            **dependency_selection,
            "description": "Mark dependency modules as prerequisites instead of autoloading them",
        },
        "conflict": {
            **array_of_strings,
            "description": "List of modules that conflict with this one and should not be loaded "
            "simultaneously",
        },
        "load": {
            **array_of_strings,
            "description": "List of additional modules to load when this module is loaded",
        },
        "suffixes": {
            "type": "object",
            "description": "Add custom suffixes to module names based on spec matching for better "
            "readability",
            "additionalKeysAreSpecs": True,
            "additionalProperties": {"type": "string"},  # key
        },
        "environment": {
            **spack.schema.environment.definition,
            "description": "Custom environment variable modifications to apply in this module "
            "file",
        },
    },
}

projections_scheme = spack.schema.projections.properties["projections"]

common_props = {
    "verbose": {
        "type": "boolean",
        "default": False,
        "description": "Enable verbose output during module file generation",
    },
    "hash_length": {
        "type": "integer",
        "minimum": 0,
        "default": 7,
        "description": "Length of package hash to include in module file names (0-32, shorter "
        "hashes may cause naming conflicts)",
    },
    "include": {
        **array_of_strings,
        "description": "List of specs to explicitly include for module file generation, even if "
        "they would normally be excluded",
    },
    "exclude": {
        **array_of_strings,
        "description": "List of specs to exclude from module file generation",
    },
    "exclude_implicits": {
        "type": "boolean",
        "default": False,
        "description": "Exclude implicit dependencies from module file generation while still "
        "allowing autoloading",
    },
    "defaults": {
        **array_of_strings,
        "description": "List of specs for which to create default module symlinks when multiple "
        "versions exist",
    },
    "hide_implicits": {
        "type": "boolean",
        "default": False,
        "description": "Hide implicit dependency modules from 'module avail' but still allow "
        "autoloading (requires module system support)",
    },
    "naming_scheme": {
        "type": "string",
        "description": "Custom naming scheme for module files using format strings",
    },
    "projections": {
        **projections_scheme,
        "description": "Custom directory structure and naming convention for module files using "
        "projection format",
    },
    "all": {
        **module_file_configuration,
        "description": "Default configuration applied to all module files in this module set",
    },
}

tcl_configuration = {
    "type": "object",
    "default": {},
    "description": "Configuration for TCL module files compatible with Environment Modules and "
    "Lmod",
    "additionalKeysAreSpecs": True,
    "properties": {**common_props},
    "additionalProperties": module_file_configuration,
}

lmod_configuration = {
    "type": "object",
    "default": {},
    "description": "Configuration for Lua module files compatible with Lmod hierarchical module "
    "system",
    "additionalKeysAreSpecs": True,
    "properties": {
        **common_props,
        "core_compilers": {
            **array_of_strings,
            "description": "List of core compilers that are always available at the top level of "
            "the Lmod hierarchy",
        },
        "hierarchy": {
            **array_of_strings,
            "description": "List of packages to use for building the Lmod module hierarchy "
            "(typically compilers and MPI implementations)",
        },
        "core_specs": {
            **array_of_strings,
            "description": "List of specs that should be placed in the core level of the Lmod "
            "hierarchy regardless of dependencies",
        },
        "filter_hierarchy_specs": {
            "type": "object",
            "description": "Filter which specs are included at different levels of the Lmod "
            "hierarchy based on spec matching",
            "additionalKeysAreSpecs": True,
            "additionalProperties": array_of_strings,
        },
    },
    "additionalProperties": module_file_configuration,
}

module_config_properties = {
    "use_view": {
        "anyOf": [{"type": "string"}, {"type": "boolean"}],
        "description": "Generate modules relative to an environment view instead of install "
        "tree (True for default view, string for named view, False to disable)",
    },
    "arch_folder": {
        "type": "boolean",
        "description": "Whether to include architecture-specific subdirectories in module file "
        "paths",
    },
    "roots": {
        "type": "object",
        "description": "Custom root directories for different module file types",
        "properties": {
            "tcl": {"type": "string", "description": "Root directory for TCL module files"},
            "lmod": {"type": "string", "description": "Root directory for Lmod module files"},
        },
    },
    "enable": {
        "type": "array",
        "default": [],
        "description": "List of module types to automatically generate during package "
        "installation",
        "items": {"type": "string", "enum": ["tcl", "lmod"]},
    },
    "lmod": {
        **lmod_configuration,
        "description": "Configuration for Lmod hierarchical module system",
    },
    "tcl": {
        **tcl_configuration,
        "description": "Configuration for TCL module files compatible with Environment Modules",
    },
    "prefix_inspections": {
        "type": "object",
        "description": "Control which package subdirectories are added to environment variables "
        "(e.g., bin to PATH, lib to LIBRARY_PATH)",
        "additionalProperties": {
            # prefix-relative path to be inspected for existence
            **array_of_strings,
            "description": "List of environment variables to update with this prefix-relative "
            "path if it exists",
        },
    },
}


# Properties for inclusion into other schemas (requires definitions)
properties: Dict[str, Any] = {
    "modules": {
        "type": "object",
        "description": "Configure automatic generation of module files for Environment Modules "
        "and Lmod to manage user environments at HPC centers",
        "properties": {
            "prefix_inspections": {
                "type": "object",
                "description": "Global prefix inspection settings that apply to all module sets, "
                "controlling which subdirectories are added to environment variables",
                "additionalProperties": {
                    # prefix-relative path to be inspected for existence
                    **array_of_strings,
                    "description": "List of environment variables to update with this "
                    "prefix-relative path if it exists",
                },
            }
        },
        "additionalProperties": {
            "type": "object",
            "default": {},
            "description": "Named module set configuration (e.g., 'default') defining how module "
            "files are generated for a specific set of packages",
            "additionalProperties": False,
            "properties": module_config_properties,
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
