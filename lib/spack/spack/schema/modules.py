# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for modules.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/modules.py
   :lines: 13-
"""
import spack.schema.environment


#: Matches a spec or a multi-valued variant but not another
#: valid keyword.
#:
#: THIS NEEDS TO BE UPDATED FOR EVERY NEW KEYWORD THAT
#: IS ADDED IMMEDIATELY BELOW THE MODULE TYPE ATTRIBUTE
spec_regex = r'(?!hierarchy|verbose|hash_length|whitelist|' \
             r'blacklist|naming_scheme|core_compilers|all)(^\w[\w-]*)'

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
            'naming_scheme': {
                'type': 'string'  # Can we be more specific here?
            },
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


# Properties for inclusion into other schemas (requires definitions)
properties = {
    'modules': {
        'type': 'object',
        'default': {},
        'additionalProperties': False,
        'properties': {
            'prefix_inspections': {
                'type': 'object',
                'patternProperties': {
                    # prefix-relative path to be inspected for existence
                    r'\w[\w-]*': array_of_strings
                }
            },
            'enable': {
                'type': 'array',
                'default': [],
                'items': {
                    'type': 'string',
                    'enum': ['tcl', 'dotkit', 'lmod']
                },
                'deprecatedProperties': {
                    'properties': ['dotkit'],
                    'message': 'cannot enable "{property}" in modules.yaml '
                               '[support for {property} module files has been'
                               ' dropped]',
                    'error': False
                },
            },
            'lmod': {
                'allOf': [
                    # Base configuration
                    module_type_configuration,
                    {
                        'type': 'object',
                        'properties': {
                            'core_compilers': array_of_strings,
                            'hierarchy': array_of_strings
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
            'dotkit': {
                'allOf': [
                    # Base configuration
                    module_type_configuration,
                    {}  # Specific dotkit extensions
                ]
            },
        },
        'deprecatedProperties': {
            'properties': ['dotkit'],
            'message': 'the section "{property}" in modules.yaml has no effect'
                       ' [support for {property} module files has been '
                       'dropped]',
            'error': False
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack module file configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
