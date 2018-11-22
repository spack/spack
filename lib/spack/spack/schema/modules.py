# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for modules.yaml configuration file.

.. literalinclude:: ../spack/schema/modules.py
   :lines: 13-
"""

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
definitions = {
    'array_of_strings': {
        'type': 'array',
        'default': [],
        'items': {
            'type': 'string'
        }
    },
    'dictionary_of_strings': {
        'type': 'object',
        'patternProperties': {
            r'\w[\w-]*': {  # key
                'type': 'string'
            }
        }
    },
    'dependency_selection': {
        'type': 'string',
        'enum': ['none', 'direct', 'all']
    },
    'module_file_configuration': {
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
            'autoload': {
                '$ref': '#/definitions/dependency_selection'},
            'prerequisites': {
                '$ref': '#/definitions/dependency_selection'},
            'conflict': {
                '$ref': '#/definitions/array_of_strings'},
            'load': {
                '$ref': '#/definitions/array_of_strings'},
            'suffixes': {
                'type': 'object',
                'validate_spec': True,
                'patternProperties': {
                    r'\w[\w-]*': {  # key
                        'type': 'string'
                    }
                }
            },
            'environment': {
                'type': 'object',
                'default': {},
                'additionalProperties': False,
                'properties': {
                    'set': {
                        '$ref': '#/definitions/dictionary_of_strings'},
                    'unset': {
                        '$ref': '#/definitions/array_of_strings'},
                    'prepend_path': {
                        '$ref': '#/definitions/dictionary_of_strings'},
                    'append_path': {
                        '$ref': '#/definitions/dictionary_of_strings'}
                }
            }
        }
    },
    'module_type_configuration': {
        'type': 'object',
        'default': {},
        'allOf': [
            {
                'properties': {
                    'verbose': {
                        'type': 'boolean',
                        'default': False
                    },
                    'hash_length': {
                        'type': 'integer',
                        'minimum': 0,
                        'default': 7
                    },
                    'whitelist': {
                        '$ref': '#/definitions/array_of_strings'},
                    'blacklist': {
                        '$ref': '#/definitions/array_of_strings'},
                    'blacklist_implicits': {
                        'type': 'boolean',
                        'default': False
                    },
                    'naming_scheme': {
                        'type': 'string'  # Can we be more specific here?
                    },
                    'all': {
                        '$ref': '#/definitions/module_file_configuration'
                    },
                }
            },
            {
                'validate_spec': True,
                'patternProperties': {
                    spec_regex: {
                        '$ref': '#/definitions/module_file_configuration'
                    },
                    anonymous_spec_regex: {
                        '$ref': '#/definitions/module_file_configuration'
                    },
                }
            }
        ]
    }
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
                    r'\w[\w-]*': {
                        '$ref': '#/definitions/array_of_strings'}}},
            'enable': {
                'type': 'array',
                'default': [],
                'items': {
                    'type': 'string',
                    'enum': ['tcl', 'dotkit', 'lmod']}},
            'lmod': {
                'allOf': [
                    # Base configuration
                    {'$ref': '#/definitions/module_type_configuration'},
                    {
                        'type': 'object',
                        'properties': {
                            'core_compilers': {
                                '$ref': '#/definitions/array_of_strings'
                            },
                            'hierarchy': {
                                '$ref': '#/definitions/array_of_strings'
                            }
                        },
                    }  # Specific lmod extensions
                ]
            },
            'tcl': {
                'allOf': [
                    # Base configuration
                    {'$ref': '#/definitions/module_type_configuration'},
                    {}  # Specific tcl extensions
                ]
            },
            'dotkit': {
                'allOf': [
                    # Base configuration
                    {'$ref': '#/definitions/module_type_configuration'},
                    {}  # Specific dotkit extensions
                ]
            },
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack module file configuration file schema',
    'definitions': definitions,
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
