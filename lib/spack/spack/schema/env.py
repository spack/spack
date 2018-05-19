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
    'title': 'Spack Environments user configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'env': {
            'type': 'object',
            'default': {},
            'properties': {
                'configs': {
                    'type': 'array',
                    'default': [],
                    'items': {'type': 'string'}
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
