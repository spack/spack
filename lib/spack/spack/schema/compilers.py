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
"""Schema for compilers.yaml configuration file.

.. literalinclude:: ../spack/schema/compilers.py
   :lines: 32-
"""


schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack compiler configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        'compilers': {
            'type': 'array',
            'items': {
                'compiler': {
                    'type': 'object',
                    'additionalProperties': False,
                    'required': [
                        'paths', 'spec', 'modules', 'operating_system'],
                    'properties': {
                        'paths': {
                            'type': 'object',
                            'required': ['cc', 'cxx', 'f77', 'fc'],
                            'additionalProperties': False,
                            'properties': {
                                'cc':  {'anyOf': [{'type': 'string'},
                                                  {'type': 'null'}]},
                                'cxx': {'anyOf': [{'type': 'string'},
                                                  {'type': 'null'}]},
                                'f77': {'anyOf': [{'type': 'string'},
                                                  {'type': 'null'}]},
                                'fc':  {'anyOf': [{'type': 'string'},
                                                  {'type': 'null'}]}}},
                        'flags': {
                            'type': 'object',
                            'additionalProperties': False,
                            'properties': {
                                'cflags': {'anyOf': [{'type': 'string'},
                                                     {'type': 'null'}]},
                                'cxxflags': {'anyOf': [{'type': 'string'},
                                                       {'type': 'null'}]},
                                'fflags': {'anyOf': [{'type': 'string'},
                                                     {'type': 'null'}]},
                                'cppflags': {'anyOf': [{'type': 'string'},
                                                       {'type': 'null'}]},
                                'ldflags': {'anyOf': [{'type': 'string'},
                                                      {'type': 'null'}]},
                                'ldlibs': {'anyOf': [{'type': 'string'},
                                                     {'type': 'null'}]}}},
                        'spec': {'type': 'string'},
                        'operating_system': {'type': 'string'},
                        'alias': {'anyOf': [{'type': 'string'},
                                            {'type': 'null'}]},
                        'modules': {'anyOf': [{'type': 'string'},
                                              {'type': 'null'},
                                              {'type': 'array'}]},
                        'environment': {
                            'type': 'object',
                            'default': {},
                            'additionalProperties': False,
                            'properties': {
                                'set': {
                                    'type': 'object',
                                    'patternProperties': {
                                        r'\w[\w-]*': {  # variable name
                                            'type': 'string'
                                        }
                                    }
                                }
                            }
                        },
                        'extra_rpaths': {
                            'type': 'array',
                            'default': [],
                            'items': {'type': 'string'}
                        }
                    },
                },
            },
        },
    },
}
