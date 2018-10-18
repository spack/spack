# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for config.yaml configuration file.

.. literalinclude:: ../spack/schema/config.py
   :lines: 13-
"""


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack core configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        'config': {
            'type': 'object',
            'default': {},
            'properties': {
                'install_tree': {'type': 'string'},
                'install_hash_length': {'type': 'integer', 'minimum': 1},
                'install_path_scheme': {'type': 'string'},
                'build_stage': {
                    'oneOf': [
                        {'type': 'string'},
                        {'type': 'array',
                         'items': {'type': 'string'}}],
                },
                'template_dirs': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
                'module_roots': {
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        'tcl': {'type': 'string'},
                        'lmod': {'type': 'string'},
                        'dotkit': {'type': 'string'},
                    },
                },
                'source_cache': {'type': 'string'},
                'misc_cache': {'type': 'string'},
                'verify_ssl': {'type': 'boolean'},
                'debug': {'type': 'boolean'},
                'checksum': {'type': 'boolean'},
                'locks': {'type': 'boolean'},
                'dirty': {'type': 'boolean'},
                'build_jobs': {'type': 'integer', 'minimum': 1},
                'ccache': {'type': 'boolean'},
                'db_lock_timeout': {'type': 'integer', 'minimum': 1},
                'package_lock_timeout': {
                    'anyOf': [
                        {'type': 'integer', 'minimum': 1},
                        {'type': 'null'}
                    ],
                },
            }
        },
    },
}
