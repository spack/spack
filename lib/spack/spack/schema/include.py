# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for include.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/include.py
   :lines: 13-
"""


#: Properties for inclusion in other schemas
properties = {
    'include': {
        'type': 'array',
        'default': [],
        'items': {'type': 'string'},
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack include other configuration scopes',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
