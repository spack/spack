# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for env.yaml configuration file.

.. literalinclude:: ../spack/schema/env.py
   :lines: 36-
"""
from llnl.util.lang import union_dicts

import spack.schema.merged


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack environment file schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        '^env|spack$': {
            'type': 'object',
            'default': {},
            'additionalProperties': False,
            'properties': union_dicts(
                # merged configuration scope schemas
                spack.schema.merged.properties,
                # extra environment schema properties
                {
                    'include': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        },
                    },
                    'specs': {
                        # Specs is a list of specs, which can have
                        # optional additional properties in a sub-dict
                        'type': 'array',
                        'default': [],
                        'additionalProperties': False,
                        'items': {
                            'anyOf': [
                                {'type': 'string'},
                                {'type': 'null'},
                                {'type': 'object'},
                            ]
                        }
                    },
                    'view': {
                        'type': ['boolean', 'string']
                    }
                }
            )
        }
    }
}
