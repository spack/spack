# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for the 'container' subsection of Spack environments."""

#: Represents a source/destination pair when copying objects
#: in a container image
_source_destination_pair = {
    'type': 'object',
    'properties': {
        'source': {'type': 'string'},
        'destination': {'type': 'string'}
    },
    'required': ['source', 'destination']
}

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
                    'enum': ['develop', '0.14', '0.14.0']
                }
            },
            'required': ['image', 'spack']
        },
        # Copy resources from host or previous stages into the container
        'copy': {
            'type': 'object',
            'properties': {
                'build': {
                    'type': 'array',
                    'items': _source_destination_pair
                },
                'final': {
                    'type': 'array',
                    'items': _source_destination_pair
                }
            },
            'additionalProperties': False
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
                'setup': {'type': 'string'},
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
