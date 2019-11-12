# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for dependencies.yaml package dependency files.

"""


#: Properties for inclusion in other schemas
properties = {
    'dependencies': {
        'type': 'object',
        'default': {},
        'additionalProperties': False,
        'patternProperties': {
            r'\w[\w-]*': {  # dependency spec
                'type': 'object',
                'default': {},
                'additionalProperties': False,
                'properties': {
                    'when': {
                        'type': 'string',
                    },
                    'patches': {
                        'oneOf': [
                            {'type': 'string'},
                            {'type': 'array',
                             'items': {'type': 'string'}}],
                    },
                    'type': {
                        'oneOf': [
                            {'type': 'string'},
                            {'type': 'array',
                             'items': {'type': 'string'}}],
                    },
                },
            },
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack package dependency file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
