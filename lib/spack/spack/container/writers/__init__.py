# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Writers for different kind of recipes and related
convenience functions.
"""
import collections
import copy

import spack.environment
import spack.schema.env
import spack.tengine as tengine
import spack.util.spack_yaml as syaml

from spack.container.images import build_info, package_info

#: Caches all the writers that are currently supported
_writer_factory = {}


def writer(name):
    """Decorator to register a factory for a recipe writer.

    Each factory should take a configuration dictionary and return a
    properly configured writer that, when called, prints the
    corresponding recipe.
    """
    def _decorator(factory):
        _writer_factory[name] = factory
        return factory
    return _decorator


def create(configuration):
    """Returns a writer that conforms to the configuration passed as input.

    Args:
        configuration: how to generate the current recipe
    """
    name = spack.environment.config_dict(configuration)['container']['format']
    return _writer_factory[name](configuration)


def recipe(configuration):
    """Returns a recipe that conforms to the configuration passed as input.

    Args:
        configuration: how to generate the current recipe
    """
    return create(configuration)()


class PathContext(tengine.Context):
    """Generic context used to instantiate templates of recipes that
    install software in a common location and make it available
    directly via PATH.
    """
    def __init__(self, config):
        self.config = spack.environment.config_dict(config)
        self.container_config = self.config['container']

    @tengine.context_property
    def run(self):
        """Information related to the run image."""
        image = self.container_config['base']['image']
        Run = collections.namedtuple('Run', ['image'])
        return Run(image=image)

    @tengine.context_property
    def build(self):
        """Information related to the build image."""

        # Map the final image to the correct build image
        run_image = self.container_config['base']['image']
        spack_version = self.container_config['base']['spack']
        image, tag = build_info(run_image, spack_version)

        Build = collections.namedtuple('Build', ['image', 'tag'])
        return Build(image=image, tag=tag)

    @tengine.context_property
    def strip(self):
        """Whether or not to strip binaries in the image"""
        return self.container_config.get('strip', True)

    @tengine.context_property
    def paths(self):
        """Important paths in the image"""
        Paths = collections.namedtuple('Paths', [
            'environment', 'store', 'view'
        ])
        return Paths(
            environment='/opt/spack-environment',
            store='/opt/software',
            view='/opt/view'
        )

    @tengine.context_property
    def manifest(self):
        """The spack.yaml file that should be used in the image"""
        import jsonschema
        # Copy in the part of spack.yaml prescribed in the configuration file
        manifest = copy.deepcopy(self.config)
        manifest.pop('container')

        # Ensure that a few paths are where they need to be
        manifest.setdefault('config', syaml.syaml_dict())
        manifest['config']['install_tree'] = self.paths.store
        manifest['view'] = self.paths.view
        manifest = {'spack': manifest}

        # Validate the manifest file
        jsonschema.validate(manifest, schema=spack.schema.env.schema)

        return syaml.dump(manifest, default_flow_style=False).strip()

    @tengine.context_property
    def os_packages(self):
        """Additional system packages that are needed at run-time."""
        package_list = self.container_config.get('os_packages', None)
        if not package_list:
            return package_list

        image = self.container_config['base']['image']
        update, install, clean = package_info(image)
        Packages = collections.namedtuple(
            'Packages', ['update', 'install', 'list', 'clean']
        )
        return Packages(update=update, install=install,
                        list=package_list, clean=clean)

    @tengine.context_property
    def extra_instructions(self):
        Extras = collections.namedtuple('Extra', ['build', 'final'])
        extras = self.container_config.get('extra_instructions', {})
        build, final = extras.get('build', None), extras.get('final', None)
        return Extras(build=build, final=final)

    @tengine.context_property
    def labels(self):
        return self.container_config.get('labels', {})

    def __call__(self):
        """Returns the recipe as a string"""
        env = tengine.make_environment()
        t = env.get_template(self.template_name)
        return t.render(**self.to_dict())


# Import after function definition all the modules in this package,
# so that registration of writers will happen automatically
import spack.container.writers.singularity  # noqa
import spack.container.writers.docker  # noqa
