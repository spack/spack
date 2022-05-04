# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for concretizer.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/concretizer.py
   :lines: 13-
"""

properties = {
    'concretizer': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'reuse': {
                'anyOf': [{'type': 'boolean'},
                          {'type': 'string'}]
            }
        }
    }
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Spack concretizer configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
