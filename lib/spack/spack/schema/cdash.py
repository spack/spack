# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for cdash.yaml configuration file.

.. literalinclude:: ../spack/schema/cdash.py
   :lines: 13-
"""


#: Properties for inclusion in other schemas
properties = {
    'cdash': {
        'type': 'object',
        'additionalProperties': False,
        'required': ['build-group', 'url', 'project', 'site'],
        'patternProperties': {
            r'build-group': {'type': 'string'},
            r'url': {'type': 'string'},
            r'project': {'type': 'string'},
            r'site': {'type': 'string'},
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Spack cdash configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
