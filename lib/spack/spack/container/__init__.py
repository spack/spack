# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Package that provides functions and classes to
generate container recipes from a Spack environment
"""
import warnings

import spack.environment as ev
import spack.schema.env as env
import spack.util.spack_yaml as syaml

from .writers import recipe

__all__ = ['validate', 'recipe']


def validate(configuration_file):
    """Validate a Spack environment YAML file that is being used to generate a
    recipe for a container.

    Since a few attributes of the configuration must have specific values for
    the container recipe, this function returns a sanitized copy of the
    configuration in the input file. If any modification is needed, a warning
    will be issued.

    Args:
        configuration_file (str): path to the Spack environment YAML file

    Returns:
        A sanitized copy of the configuration stored in the input file
    """
    import jsonschema
    with open(configuration_file) as f:
        config = syaml.load(f)

    # Ensure we have a "container" attribute with sensible defaults set
    env_dict = ev.config_dict(config)
    env_dict.setdefault('container', {
        'format': 'docker',
        'images': {'os': 'ubuntu:18.04', 'spack': 'develop'}
    })
    env_dict['container'].setdefault('format', 'docker')
    env_dict['container'].setdefault(
        'images', {'os': 'ubuntu:18.04', 'spack': 'develop'}
    )

    # Remove attributes that are not needed / allowed in the
    # container recipe
    for subsection in ('cdash', 'gitlab_ci', 'modules'):
        if subsection in env_dict:
            msg = ('the subsection "{0}" in "{1}" is not used when generating'
                   ' container recipes and will be discarded')
            warnings.warn(msg.format(subsection, configuration_file))
            env_dict.pop(subsection)

    # Set the default value of the concretization strategy to "together" and
    # warn if the user explicitly set another value
    env_dict.setdefault('concretization', 'together')
    if env_dict['concretization'] != 'together':
        msg = ('the "concretization" attribute of the environment is set '
               'to "{0}" [the advised value is instead "together"]')
        warnings.warn(msg.format(env_dict['concretization']))

    # Check if the install tree was explicitly set to a custom value and warn
    # that it will be overridden
    environment_config = env_dict.get('config', {})
    if environment_config.get('install_tree', None):
        msg = ('the "config:install_tree" attribute has been set explicitly '
               'and will be overridden in the container image')
        warnings.warn(msg)

    # Likewise for the view
    environment_view = env_dict.get('view', None)
    if environment_view:
        msg = ('the "view" attribute has been set explicitly '
               'and will be overridden in the container image')
        warnings.warn(msg)

    jsonschema.validate(config, schema=env.schema)
    return config
