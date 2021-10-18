# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for bootstrap.yaml configuration file."""

#: Schema of a single source
_source_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'type': {'type': 'string'},
        'info': {'type': 'object'}
    },
    'additionalProperties': False,
    'required': ['name', 'description', 'type']
}

properties = {
    'bootstrap': {
        'type': 'object',
        'properties': {
            'enable': {'type': 'boolean'},
            'root': {
                'type': 'string'
            },
            'sources': {
                'type': 'array',
                'items': _source_schema
            },
            'trusted': {
                'type': 'object',
                'patternProperties': {r'\w[\w-]*': {'type': 'boolean'}}
            }
        }
    }
}

#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack bootstrap configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}


def update(data):
    """Update the data in place to update deprecated properties.

    Args:
        data (dict): dictionary to be updated

    Returns:
        True if data was changed, False otherwise
    """
    # renamed: "trusted:github-actions" -> "trusted:official-spack-binaries"
    # renamed: "trusted:spack-install" -> "trusted:build-from-sources"
    changed = False

    trusted = data.get('trusted', None)

    if trusted:
        if 'github-actions' in trusted:
            trusted['official-spack-binaries'] = trusted['github-actions']
            del trusted['github-actions']
            changed = True

        if 'spack-install' in trusted:
            trusted['build-from-sources'] = trusted['spack-install']
            del trusted['spack-install']
            changed = True

    return changed
