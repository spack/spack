# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for expressing dependencies of a set of specs in a JSON file

.. literalinclude:: _spack_root/lib/spack/spack/schema/specs_deps.py
   :lines: 32-
"""


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack schema for the dependencies of a set of specs',
    'type': 'object',
    'additionalProperties': False,
    'required': ['specs'],
    'properties': {
        r'dependencies': {
            'type': 'array',
            'default': [],
            'items': {
                'type': 'object',
                'additionalProperties': False,
                'required': ['depends', 'spec'],
                'properties': {
                    r'depends': {'type': 'string'},
                    r'spec': {'type': 'string'},
                },
            },
        },
        r'specs': {
            'type': 'array',
            'default': [],
            'items': {
                'type': 'object',
                'additionalProperties': False,
                'required': ['root_spec', 'spec', 'label'],
                'properties': {
                    r'root_spec': {'type': 'string'},
                    r'spec': {'type': 'string'},
                    r'label': {'type': 'string'},
                }
            },
        },
    },
}
