# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for projections.yaml configuration file.

.. literalinclude:: ../spack/schema/projections.py
   :lines: 13-
"""


#: Properties for inclusion in other schemas
properties = {
    'projections': {
        'type': 'object',
        'default': {},
        'patternProperties': {
            r'all|\w[\w-]*': {
                'type': 'string'
            },
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack view projection configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
