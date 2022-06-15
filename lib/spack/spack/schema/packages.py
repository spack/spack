# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for packages.yaml configuration files.

.. literalinclude:: _spack_root/lib/spack/spack/schema/packages.py
   :lines: 13-
"""


def deprecate_paths_and_modules(instance, deprecated_properties):
    """Function to produce warning/error messages if "paths" and "modules" are
    found in "packages.yaml"

    Args:
        instance: instance of the configuration file
        deprecated_properties: deprecated properties in instance

    Returns:
        Warning/Error message to be printed
    """
    import copy
    import os.path

    import llnl.util.tty

    import spack.util.spack_yaml as syaml

    # Copy the instance to remove default attributes that are not related
    # to the part that needs to be reported
    instance_copy = copy.copy(instance)

    # Check if this configuration comes from an environment or not
    absolute_path = instance_copy._end_mark.name
    command_to_suggest = '$ spack config update packages'
    if os.path.basename(absolute_path) == 'spack.yaml':
        command_to_suggest = '$ spack env update <environment>'

    # Retrieve the relevant part of the configuration as YAML
    keys_to_be_removed = [
        x for x in instance_copy if x not in deprecated_properties
    ]
    for key in keys_to_be_removed:
        instance_copy.pop(key)
    yaml_as_str = syaml.dump_config(instance_copy, blame=True)

    if llnl.util.tty.is_debug():
        msg = 'OUTDATED CONFIGURATION FILE [file={0}]\n{1}'
        llnl.util.tty.debug(msg.format(absolute_path, yaml_as_str))

    msg = ('detected deprecated properties in {0}\nActivate the debug '
           'flag to have more information on the deprecated parts or '
           'run:\n\n\t{2}\n\nto update the file to the new format\n')
    return msg.format(
        absolute_path, yaml_as_str, command_to_suggest
    )


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
                                'prefix': {'type': 'string'},
                                'modules': {'type': 'array',
                                            'items': {'type': 'string'}},
                                'extra_attributes': {'type': 'object'}
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
                    'message': deprecate_paths_and_modules,
                    'error': False
                }
            },
        },
    },
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/draft-07/schema#',
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

        # If we don't have these deprecated attributes, continue
        if not any(x in cfg_object for x in ('paths', 'modules')):
            continue

        # If we arrive here we need to make some changes i.e.
        # we need to remove and eventually convert some attributes
        changed = True
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
                'modules': [str(module)]
            })
        if externals:
            cfg_object['externals'] = externals

    return changed
