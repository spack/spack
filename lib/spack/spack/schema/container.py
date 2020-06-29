# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for the 'container' subsection of Spack environments."""

#: Schema for the container attribute included in Spack environments
container_schema = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        # The recipe formats that are currently supported by the command
        'format': {
            'type': 'string',
            'enum': ['docker', 'singularity']
        },
        # Describes the base image to start from and the version
        # of Spack to be used
        'base': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'image': {
                    'type': 'string',
                    'enum': ['ubuntu:18.04',
                             'ubuntu:16.04',
                             'centos:7',
                             'centos:6']
                },
                'spack': {
                    'type': 'string',
                    'enum': [
                        'develop',
                        '0.14', '0.14.0', '0.14.1', '0.14.2', '0.14.3'
                    ]
                }
            },
            'required': ['image', 'spack']
        },
        # Whether or not to strip installed binaries
        'strip': {
            'type': 'boolean',
            'default': True
        },
        # Additional system packages that are needed at runtime
        'os_packages': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        },
        # Add labels to the image
        'labels': {
            'type': 'object',
        },
        # Add a custom extra section at the bottom of a stage
        'extra_instructions': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'build': {'type': 'string'},
                'final': {'type': 'string'}
            }
        },
        # Reserved for properties that are specific to each format
        'singularity': {
            'type': 'object',
            'additionalProperties': False,
            'default': {},
            'properties': {
                'runscript': {'type': 'string'},
                'startscript': {'type': 'string'},
                'test': {'type': 'string'},
                'help': {'type': 'string'}
            }
        },
        'docker': {
            'type': 'object',
            'additionalProperties': False,
            'default': {},
        }
    }
}

properties = {'container': container_schema}
