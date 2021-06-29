# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for bootstrap.yaml configuration file."""

properties = {
    'bootstrap': {
        'type': 'object',
        'properties': {
            'enable': {'type': 'boolean'},
            'root': {
                'type': 'string'
            },
        }
    }
}

#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack bootstrap configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
