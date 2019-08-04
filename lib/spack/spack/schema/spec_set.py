# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for Spack spec-set configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/spec_set.py
   :lines: 32-
"""


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack test configuration file schema',
    'definitions': {
        # used for include/exclude
        'list_of_specs': {
            'type': 'array',
            'items': {'type': 'string'}
        },
        # used for compilers and for packages
        'objects_with_version_list': {
            'type': 'object',
            'additionalProperties': False,
            'patternProperties': {
                r'\w[\w-]*': {
                    'type': 'object',
                    'additionalProperties': False,
                    'required': ['versions'],
                    'properties': {
                        'versions': {
                            'type': 'array',
                            'items': {
                                'oneOf': [
                                    {'type': 'string'},
                                    {'type': 'number'},
                                ],
                            },
                        },
                    },
                },
            },
        },
        'packages': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'packages': {
                    '$ref': '#/definitions/objects_with_version_list'
                },
            }
        },
        'compilers': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'compilers': {
                    '$ref': '#/definitions/objects_with_version_list'
                },
            }
        },
        'specs': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'specs': {'$ref': '#/definitions/list_of_specs'},
            }
        },
    },
    # this is the actual top level object
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'spec-set': {
            'type': 'object',
            'additionalProperties': False,
            'required': ['matrix'],
            'properties': {
                # top-level settings are keys and need to be unique
                'include': {'$ref': '#/definitions/list_of_specs'},
                'exclude': {'$ref': '#/definitions/list_of_specs'},
                'cdash': {
                    'oneOf': [
                        {'type': 'string'},
                        {'type': 'array',
                         'items': {'type': 'string'}
                        },
                    ],
                },
                'project': {
                    'type': 'string',
                },
                # things under matrix (packages, compilers, etc.)  are a
                # list so that we can potentiall have multiple of them.
                'matrix': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'oneOf': [
                            {'$ref': '#/definitions/specs'},
                            {'$ref': '#/definitions/packages'},
                            {'$ref': '#/definitions/compilers'},
                        ],
                    },
                },
            },
        },
    },
}
