##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Schema for config.yaml configuration file.

.. literalinclude:: ../spack/schema/config.py
   :lines: 32-
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
            }
        },
    },
}
