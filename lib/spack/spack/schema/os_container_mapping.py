# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for os-container-mapping.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/os_container_mapping.py
   :lines: 32-
"""


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack release builds os/container mapping config file schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        r'containers': {
            'type': 'object',
            'default': {},
            'patternProperties': {
                r'[\w\d\-_\.]+': {
                    'type': 'object',
                    'default': {},
                    'additionalProperties': False,
                    'required': ['image'],
                    'properties': {
                        'image': {'type': 'string'},
                        'setup_script': {'type': 'string'},
                        'compilers': {
                            'type': 'array',
                            'default': [],
                            'items': {
                                'type': 'object',
                                'default': {},
                                'additionalProperties': False,
                                'required': ['name'],
                                'properties': {
                                    'name': {'type': 'string'},
                                    'path': {'type': 'string'},
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}
