# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for mirrors.yaml configuration file.

.. literalinclude:: ../spack/schema/mirrors.py
   :lines: 13-
"""


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack mirror configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        r'mirrors': {
            'type': 'object',
            'default': {},
            'additionalProperties': False,
            'patternProperties': {
                r'\w[\w-]*': {
                    'type': 'string'},
            },
        },
    },
}
