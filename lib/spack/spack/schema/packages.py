# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for packages.yaml configuration files.

.. literalinclude:: _spack_root/lib/spack/spack/schema/packages.py
   :lines: 13-
"""


#: Properties for inclusion in other schemas
properties = {
    'packages': {
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
                    'target': {
                        'type': 'array',
                        'default': [],
                        # target names
                        'items': {'type': 'string'},
                    },
                    'compiler': {
                        'type': 'array',
                        'default': [],
                        'items': {'type': 'string'}},  # compiler specs
                    'buildable': {
                        'type':  'boolean',
                        'default': True,
                    },
                    'permissions': {
                        'type': 'object',
                        'additionalProperties': False,
                        'properties': {
                            'read': {
                                'type':  'string',
                                'enum': ['user', 'group', 'world'],
                            },
                            'write': {
                                'type':  'string',
                                'enum': ['user', 'group', 'world'],
                            },
                            'group': {
                                'type':  'string',
                            },
                        },
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
                    'variants': {
                        'oneOf': [
                            {'type': 'string'},
                            {'type': 'array',
                             'items': {'type': 'string'}}],
                    },
                    'externals': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'spec': {'type': 'string'},
                            },
                            'additionalProperties': True,
                            'required': ['spec']
                        }
                    },
                    # Deprecated properties, will trigger an error with a
                    # message telling how to update.
                    'paths': {'type': 'object'},
                    'modules': {'type': 'object'},
                },
                'deprecatedProperties': {
                    'properties': ['modules', 'paths'],
                    'message': 'the attributes "modules" and "paths" in '
                               'packages.yaml have been deprecated. Run '
                               '"spack config update packages" to update '
                               'your configuration',
                    'error': True
                }
            },
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack package configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}


def update(data):
    """Update the data in place to remove deprecated properties.

    Args:
        data (dict): dictionary to be updated

    Returns:
        True if data was changed, False otherwise
    """
    changed = False
    for cfg_object in data.values():
        externals = []
        paths = cfg_object.pop('paths', {})
        for spec, prefix in paths.items():
            externals.append({
                'spec': str(spec),
                'prefix': str(prefix)
            })
        modules = cfg_object.pop('modules', {})
        for spec, module in modules.items():
            externals.append({
                'spec': str(spec),
                'module': str(module)
            })
        if externals:
            changed = True
            cfg_object['externals'] = externals
    return changed
