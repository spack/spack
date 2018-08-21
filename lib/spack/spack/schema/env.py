# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for env.yaml configuration file.

.. literalinclude:: ../spack/schema/env.py
   :lines: 32-
"""


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack environment file schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        '^env|spack$': {
            'type': 'object',
            'default': {},
            'properties': {
                'include': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    },
                },


                'specs': {
                    'type': 'object',
                    'default': {},
                    'additionalProperties': False,
                    'patternProperties': {
                        r'\w[\w-]*': {  # user spec
                            'type': 'object',
                            'default': {},
                            'additionalProperties': False,
                        }
                    }
                }
            }
        }
    }
}
