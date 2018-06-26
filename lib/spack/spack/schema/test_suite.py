##############################################################################
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
"""Schema for Spack test-suite configuration file.

.. literalinclude:: ../spack/schema/test_suite.py
   :lines: 32-
"""


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack test configuration file schema',
    'definitions': {
        # used for include/exclude
        'list_of_specs': {
            'type': 'array',
            'items': {'type': 'string'}
        },
        # used for compilers and for packages
        'objects_with_version_list': {
            'type': 'object',
            'additionalProperties': False,
            'patternProperties': {
                r'\w[\w-]*': {
                    'type': 'object',
                    'additionalProperties': False,
                    'required': ['versions'],
                    'properties': {
                        'versions': {
                            'type': 'array',
                            'items': {
                                'oneOf': [
                                    {'type': 'string'},
                                    {'type': 'number'},
                                ],
                            },
                        },
                    },
                },
            },
        },
        'packages': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'packages': {
                    '$ref': '#/definitions/objects_with_version_list'
                },
            }
        },
        'compilers': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'compilers': {
                    '$ref': '#/definitions/objects_with_version_list'
                },
            }
        },
        'specs': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'specs': {'$ref': '#/definitions/list_of_specs'},
            }
        },
    },
    # this is the actual top level object
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'test-suite': {
            'type': 'object',
            'additionalProperties': False,
            'required': ['matrix'],
            'properties': {
                # top-level settings are keys and need to be unique
                'include': {'$ref': '#/definitions/list_of_specs'},
                'exclude': {'$ref': '#/definitions/list_of_specs'},
                'cdash': {
                    'oneOf': [
                        {'type': 'string'},
                        {'type': 'array',
                         'items': {'type': 'string'}
                        },
                    ],
                },
                'project': {
                    'type': 'string',
                },
                # things under matrix (packages, compilers, etc.)  are a
                # list so that we can potentiall have multiple of them.
                'matrix': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'oneOf': [
                            {'$ref': '#/definitions/specs'},
                            {'$ref': '#/definitions/packages'},
                            {'$ref': '#/definitions/compilers'},
                        ],
                    },
                },
            },
        },
    },
}
