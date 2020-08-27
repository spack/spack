# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for gitlab-ci.yaml configuration file.

.. literalinclude:: ../spack/schema/gitlab_ci.py
   :lines: 13-
"""

image_schema = {
    'oneOf': [
        {
            'type': 'string'
        }, {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'entrypoint': {
                    'type': 'array',
                    'items': {
                        'type': 'string',
                    },
                },
            },
        },
    ],
}

#: Properties for inclusion in other schemas
properties = {
    'gitlab-ci': {
        'type': 'object',
        'additionalProperties': False,
        'required': ['mappings'],
        'patternProperties': {
            'bootstrap': {
                'type': 'array',
                'items': {
                    'anyOf': [
                        {
                            'type': 'string',
                        }, {
                            'type': 'object',
                            'additionalProperties': False,
                            'required': ['name'],
                            'properties': {
                                'name': {
                                    'type': 'string',
                                },
                                'compiler-agnostic': {
                                    'type': 'boolean',
                                    'default': False,
                                },
                            },
                        },
                    ],
                },
            },
            'mappings': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'additionalProperties': False,
                    'required': ['match', 'runner-attributes'],
                    'properties': {
                        'match': {
                            'type': 'array',
                            'items': {
                                'type': 'string',
                            },
                        },
                        'runner-attributes': {
                            'type': 'object',
                            'additionalProperties': True,
                            'required': ['tags'],
                            'properties': {
                                'image': image_schema,
                                'tags': {
                                    'type': 'array',
                                    'default': [],
                                    'items': {'type': 'string'}
                                },
                                'variables': {
                                    'type': 'object',
                                    'default': {},
                                    'patternProperties': {
                                        r'[\w\d\-_\.]+': {
                                            'type': 'string',
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            'enable-artifacts-buildcache': {
                'type': 'boolean',
                'default': False,
            },
            'enable-debug-messages': {
                'type': 'boolean',
                'default': False,
            },
            'final-stage-rebuild-index': {
                'type': 'object',
                'additionalProperties': False,
                'required': ['tags'],
                'properties': {
                    'image': image_schema,
                    'tags': {
                        'type': 'array',
                        'default': [],
                        'items': {'type': 'string'}
                    },
                },
            },
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack gitlab-ci configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
