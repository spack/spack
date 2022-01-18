# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for mirrors.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/mirrors.py
   :lines: 13-
"""


#: Properties for inclusion in other schemas
properties = {
    'mirrors': {
        'type': 'object',
        'default': {},
        'additionalProperties': False,
        'patternProperties': {
            r'\w[\w-]*': {
                'anyOf': [
                    {'type': 'string'},
                    {
                        'type': 'object',
                        'required': ['fetch', 'push'],
                        'properties': {
                            'fetch': {'type': ['string', 'object']},
                            'push': {'type': ['string', 'object']}
                        }
                    }
                ]
            },
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Spack mirror configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
