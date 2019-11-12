# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for versions.yaml package version files.

"""


#: Properties for inclusion in other schemas
properties = {
    'versions': {
        'type': 'object',
        'default': {},
        'additionalProperties': False,
        'patternProperties': {
            r'\w[\w-]*': {  # version spec
                'type': 'object',
                'default': {},
                'additionalProperties': True,
                'properties': {
                    'checksum': {
                        'type': 'string',
                    },
                },
            },
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack package versions file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
