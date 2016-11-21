# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
"""Schema for rpms.yaml configuration file.

.. literalinclude:: ../spack/schema/mirrors.py
   :lines: 32-
"""


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack package configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        r'rpms': {
            'type': 'object',
            'default': {},
            'additionalProperties': False,
            'patternProperties': {
                r'\w[\w-]*': {  # package name
                    'type': 'object',
                    'default': {},
                    'additionalProperties': False,
                    'properties': {
                        'name': {'type': 'string'},
                        'prefix': {'type': 'string'},
                        'provides': {'type': 'string'},
                        'add-system-deps': {
                            'type': 'array',
                            'items': {'type': 'string'}
                        },
                        'add-system-build-deps': {
                            'type': 'array',
                            'items': {'type': 'string'}
                        },
                        'ignore-deps': {
                            'type': 'array',
                            'items': {'type': 'string'}
                        },
                        'dep-map': {
                            'type': 'object',
                            'patternProperties': {
                                r'\w[\w-]*': {'type': 'string'}
                            }
                        },
                        'build-dep-map': {
                            'type': 'object',
                            'patternProperties': {
                                r'\w[\w-]*': {'type': 'string'}
                            }
                        },
                        'subspaces': {
                            'type': 'object',
                            'patternProperties': {
                                r'\w[\w-]*': {
                                    'type': 'object',
                                    'properties': {
                                        'name': {'type': 'string'},
                                        'prefix': {'type': 'string'},
                                        'provides': {'type': 'string'},
                                        'add-system-deps': {
                                            'type': 'array',
                                            'items': {'type': 'string'}
                                        },
                                        'add-system-build-deps': {
                                            'type': 'array',
                                            'items': {'type': 'string'}
                                        },
                                        'ignore-deps': {
                                            'type': 'array',
                                            'items': {'type': 'string'}
                                        },
                                        'compiler': {
                                            'type': 'array',
                                            'default': [],
                                            'items': {'type': 'string'}},
                                        'version': {
                                            'type': 'array',
                                            'default': [],
                                            'items': {'anyOf': [
                                                {'type': 'string'},
                                                {'type': 'number'}]}},
                                    }}}
                        },
                    },
                },
            },
        },
    },
}
