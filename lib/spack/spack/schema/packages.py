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
"""Schema for packages.yaml configuration files.

.. literalinclude:: ../spack/schema/packages.py
   :lines: 32-
"""


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack package configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        r'packages': {
            'type': 'object',
            'default': {},
            'additionalProperties': False,
            'patternProperties': {
                r'\w[\w-]*': {  # package name
                    'type': 'object',
                    'default': {},
                    'additionalProperties': False,
                    'properties': {
                        'version': {
                            'type': 'array',
                            'default': [],
                            # version strings
                            'items': {'anyOf': [{'type': 'string'},
                                                {'type': 'number'}]}},
                        'compiler': {
                            'type': 'array',
                            'default': [],
                            'items': {'type': 'string'}},  # compiler specs
                        'buildable': {
                            'type':  'boolean',
                            'default': True,
                        },
                        'modules': {
                            'type': 'object',
                            'default': {},
                        },
                        'providers': {
                            'type':  'object',
                            'default': {},
                            'additionalProperties': False,
                            'patternProperties': {
                                r'\w[\w-]*': {
                                    'type': 'array',
                                    'default': [],
                                    'items': {'type': 'string'}, }, }, },
                        'paths': {
                            'type': 'object',
                            'default': {},
                        },
                        'variants': {
                            'oneOf': [
                                {'type': 'string'},
                                {'type': 'array',
                                 'items': {'type': 'string'}}],
                        },
                    },
                },
            },
        },
    },
}
