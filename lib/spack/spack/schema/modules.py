# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for modules.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/modules.py
   :lines: 13-
"""
import warnings

import spack.schema.environment
import spack.schema.projections

#: Matches a spec or a multi-valued variant but not another
#: valid keyword.
#:
#: THIS NEEDS TO BE UPDATED FOR EVERY NEW KEYWORD THAT
#: IS ADDED IMMEDIATELY BELOW THE MODULE TYPE ATTRIBUTE
spec_regex = r'(?!hierarchy|core_specs|verbose|hash_length|whitelist|' \
             r'blacklist|projections|naming_scheme|core_compilers|all|' \
             r'defaults)(^\w[\w-]*)'

#: Matches a valid name for a module set
valid_module_set_name = r'^(?!arch_folder$|lmod$|roots$|enable$|prefix_inspections$|'\
                        r'tcl$|use_view$)\w[\w-]*$'

#: Matches an anonymous spec, i.e. a spec without a root name
anonymous_spec_regex = r'^[\^@%+~]'

#: Definitions for parts of module schema
array_of_strings = {
    'type': 'array', 'default': [], 'items': {'type': 'string'}
}

dictionary_of_strings = {
    'type': 'object', 'patternProperties': {r'\w[\w-]*': {'type': 'string'}}
}

dependency_selection = {'type': 'string', 'enum': ['none', 'direct', 'all']}

module_file_configuration = {
    'type': 'object',
    'default': {},
    'additionalProperties': False,
    'properties': {
        'filter': {
            'type': 'object',
            'default': {},
            'additionalProperties': False,
            'properties': {
                'environment_blacklist': {
                    'type': 'array',
                    'default': [],
                    'items': {
                        'type': 'string'
                    }
                }
            }
        },
        'template': {
            'type': 'string'
        },
        'autoload': dependency_selection,
        'prerequisites': dependency_selection,
        'conflict': array_of_strings,
        'load': array_of_strings,
        'suffixes': {
            'type': 'object',
            'validate_spec': True,
            'patternProperties': {
                r'\w[\w-]*': {  # key
                    'type': 'string'
                }
            }
        },
        'environment': spack.schema.environment.definition
    }
}

projections_scheme = spack.schema.projections.properties['projections']

module_type_configuration = {
    'type': 'object',
    'default': {},
    'allOf': [
        {'properties': {
            'verbose': {
                'type': 'boolean',
                'default': False
            },
            'hash_length': {
                'type': 'integer',
                'minimum': 0,
                'default': 7
            },
            'whitelist': array_of_strings,
            'blacklist': array_of_strings,
            'blacklist_implicits': {
                'type': 'boolean',
                'default': False
            },
            'defaults': array_of_strings,
            'naming_scheme': {
                'type': 'string'  # Can we be more specific here?
            },
            'projections': projections_scheme,
            'all': module_file_configuration,
        }
        },
        {'validate_spec': True,
         'patternProperties': {
             spec_regex: module_file_configuration,
             anonymous_spec_regex: module_file_configuration,
         }
         }
    ]
}


module_config_properties = {
    'use_view': {'anyOf': [
        {'type': 'string'},
        {'type': 'boolean'}
    ]},
    'arch_folder': {'type': 'boolean'},
    'roots': {
        'type': 'object',
        'properties': {
            'tcl': {'type': 'string'},
            'lmod': {'type': 'string'},
        },
    },
    'enable': {
        'type': 'array',
        'default': [],
        'items': {
            'type': 'string',
            'enum': ['tcl', 'lmod']
        }
    },
    'lmod': {
        'allOf': [
            # Base configuration
            module_type_configuration,
            {
                'type': 'object',
                'properties': {
                    'core_compilers': array_of_strings,
                    'hierarchy': array_of_strings,
                    'core_specs': array_of_strings,
                },
            }  # Specific lmod extensions
        ]
    },
    'tcl': {
        'allOf': [
            # Base configuration
            module_type_configuration,
            {}  # Specific tcl extensions
        ]
    },
    'prefix_inspections': {
        'type': 'object',
        'additionalProperties': False,
        'patternProperties': {
            # prefix-relative path to be inspected for existence
            r'^[\w-]*': array_of_strings
        }
    },
}


def deprecation_msg_default_module_set(instance, props):
    return (
        'Top-level properties "{0}" in module config are ignored as of Spack v0.18. '
        'They should be set on the "default" module set. Run\n\n'
        '\t$ spack config update modules\n\n'
        'to update the file to the new format'.format('", "'.join(instance))
    )


# Properties for inclusion into other schemas (requires definitions)
properties = {
    'modules': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'prefix_inspections': {
                'type': 'object',
                'additionalProperties': False,
                'patternProperties': {
                    # prefix-relative path to be inspected for existence
                    r'^[\w-]*': array_of_strings
                }
            },
        },
        'patternProperties': {
            valid_module_set_name: {
                'type': 'object',
                'default': {},
                'additionalProperties': False,
                'properties': module_config_properties
            },
            # Deprecated top-level keys (ignored in 0.18 with a warning)
            '^(arch_folder|lmod|roots|enable|tcl|use_view)$': {}
        },
        'deprecatedProperties': {
            'properties': ['arch_folder', 'lmod', 'roots', 'enable', 'tcl', 'use_view'],
            'message': deprecation_msg_default_module_set,
            'error': False
        }
    }
}

#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Spack module file configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}


def update(data):
    """Update the data in place to remove deprecated properties.

    Args:
        data (dict): dictionary to be updated

    Returns:
        True if data was changed, False otherwise
    """
    changed = False

    deprecated_top_level_keys = ('arch_folder', 'lmod', 'roots', 'enable',
                                 'tcl', 'use_view')

    # Don't update when we already have a default module set
    if 'default' in data:
        if any(key in data for key in deprecated_top_level_keys):
            warnings.warn('Did not move top-level module properties into "default" '
                          'module set, because the "default" module set is already '
                          'defined')
        return changed

    default = {}

    # Move deprecated top-level keys under "default" module set.
    for key in deprecated_top_level_keys:
        if key in data:
            default[key] = data.pop(key)

    if default:
        changed = True
        data['default'] = default

    return changed
