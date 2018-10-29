# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for repos.yaml configuration file.

.. literalinclude:: ../spack/schema/repos.py
   :lines: 13-
"""


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack repository configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        r'repos': {
            'type': 'array',
            'default': [],
            'items': {
                'type': 'string'},
        },
    },
}
