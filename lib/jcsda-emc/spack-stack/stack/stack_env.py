import subprocess
import spack
import os
import logging
import spack.util.spack_yaml as syaml
import spack.environment as ev
import shutil
import llnl.util.tty as tty
import spack.config
import copy

default_manifest_yaml = """\
# This is a Spack Environment file.
#
# It describes a set of packages to be installed, along with
# configuration settings.
# Includes are in order of highest precedence first.
# Site configs take precedence over the base packages.yaml.
spack:

  view: false

"""

valid_configs = ['compilers.yaml', 'config.yaml', 'mirrors.yaml',
                 'modules.yaml', 'packages.yaml', 'concretizer.yaml']

# Hidden file in top-level spack-stack dir so this module can
# find relative config files. Assuming Spack is a submodule of
# spack-stack.
check_file = '.spackstack'


# Find spack-stack directory assuming this Spack instance
# is a submodule of spack-stack.
def stack_path(*paths):
    stack_dir = os.path.dirname(spack.paths.spack_root)

    if not os.path.exists(os.path.join(stack_dir, check_file)):
        raise Exception('Not a submodule of spack-stack')

    return os.path.join(stack_dir, *paths)


site_path = stack_path('configs', 'sites')
app_path = stack_path('configs', 'apps')

# Use SPACK_STACK_DIR for these configs because changes in these
# files should be tracked as part of the repo.
common_includes = ['${SPACK_STACK_DIR}/configs/common/modules.yaml',
                   '${SPACK_STACK_DIR}/configs/common/config.yaml']


def get_git_revision_short_hash(path) -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'],
                                   cwd=path).decode('ascii').strip()


def stack_hash():
    return get_git_revision_short_hash(stack_path())


def spack_hash():
    return get_git_revision_short_hash(spack.paths.spack_root)


class StackEnv(object):
    """ Represents a spack.yaml environment based on different
    configurations of sites and specs. Can be created through an envs.yaml or
    through the command line. Uses Spack's library
    to maintain an internal state that represents the yaml and can be
    written out with write().
    The output is a pure Spack environment.
    """

    def __init__(self, **kwargs):
        """
        Construct properties directly from kwargs so they can be passed in
        through a dictionary (input file), or named args
        for command-line usage.
        """

        self.dir = kwargs.get('dir')
        self.app = kwargs.get('app', None)
        self.name = kwargs.get('name')

        self.specs = []
        self.includes = []

        # Config can be either name in apps dir or an absolute path to
        # to a spack.yaml to be used as a template. If None then empty
        # template is used.
        if not self.app:
            self.env_yaml = syaml.load_config(default_manifest_yaml)
            self.app_path = None
        else:
            if os.path.isabs(self.app):
                self.app_path = self.app
                template = self.app
            elif os.path.exists(os.path.join(app_path, self.app)):
                self.app_path = os.path.join(app_path, self.app)
                template = os.path.join(app_path, self.app, 'spack.yaml')
            else:
                raise Exception('App: "{}" does not exist'.format(self.app))

            with open(template, 'r') as f:
                self.env_yaml = syaml.load_config(f)

        self.site = kwargs.get('site', None)
        if self.site == 'none':
            self.site = None
        self.desc = kwargs.get('desc', None)
        self.compiler = kwargs.get('compiler', None)
        self.mpi = kwargs.get('mpi', None)
        self.base_packages = kwargs.get('base_packages', None)
        self.install_prefix = kwargs.get('install_prefix', None)
        self.mirror = kwargs.get('mirror', None)
        self.upstream = kwargs.get('upstreams', None)

        if not self.name:
            site = self.site if self.site else 'default'
            self.name = '{}.{}'.format(self.app, self.site)

    def env_dir(self):
        """env_dir is <dir>/<name>"""
        return os.path.join(self.dir, self.name)

    def add_specs(self, specs):
        self.specs.extend(specs)

    def add_includes(self, includes):
        self.includes.extend(includes)

    def site_configs_dir(self):
        site_configs_dir = os.path.join(site_path, self.site)
        return site_configs_dir

    def _copy_site_includes(self):
        """Copy site directory into environment"""
        if not self.site:
            raise Exception('Site is not set')

        site_name = 'site'
        self.includes.append(site_name)
        env_site_dir = os.path.join(self.env_dir(), site_name)
        shutil.copytree(self.site_configs_dir(), env_site_dir)

    def _copy_package_includes(self):
        """Copy base packages into environment"""
        if not self.base_packages:
            raise Exception('base_packages is not set')

        self.add_includes(['packages.yaml'])
        shutil.copy(self.base_packages, self.env_dir())

    def write(self):
        """Write environment out to a spack.yaml in <env_dir>/<name>.
        Will create env_dir if it does not exist.
        """
        env_dir = self.env_dir()
        env_yaml = self.env_yaml

        if os.path.exists(env_dir):
            raise Exception("Environment '{}' already exists.".format(env_dir))

        os.makedirs(env_dir, exist_ok=True)

        self.add_includes(common_includes)

        if self.site != 'none':
            self._copy_site_includes()

        if self.base_packages:
            self._copy_package_includes()

        # No way to add to env includes using pure Spack.
        env_yaml['spack']['include'] = self.includes

        # Write out file with includes filled in.
        env_file = os.path.join(env_dir, 'spack.yaml')
        with open(env_file, 'w') as f:
            # Write header with hashes.
            header = 'spack-stack hash: {}\nspack hash: {}'
            env_yaml.yaml_set_start_comment(
                header.format(stack_hash(), spack_hash()))
            syaml.dump_config(env_yaml, stream=f)

        # Activate empty env and add specs/packages.
        env = ev.Environment(path=env_dir, init_file=env_file)
        ev.activate(env)
        env_scope = env.env_file_config_scope_name()

        # Save original data in spack.yaml because it has higest precedence.
        # spack.config.add will overwrite as it goes.
        # Precedence order (high to low) is original spack.yaml,
        # then common configs, then site configs.
        original_sections = {}
        for key in spack.config.section_schemas.keys():
            section = spack.config.get(key, scope=env_scope)
            if section:
                original_sections[key] = copy.deepcopy(section)

        # Commonly used config settings
        if self.compiler:
            compiler = 'packages:all::compiler:[{}]'.format(self.compiler)
            spack.config.add(compiler, scope=env_scope)
        if self.mpi:
            mpi = 'packages:all::providers:mpi:[{}]'.format(self.mpi)
            spack.config.add(mpi, scope=env_scope)
        if self.install_prefix:
            # Modules can go in <prefix>/modulefiles by default
            prefix = 'config:install_tree:root:{}'.format(self.install_prefix)
            spack.config.add(prefix, scope=env_scope)
            module_prefix = os.path.join(self.install_prefix, "modulefiles")
            lmod_prefix = 'config:module_roots:lmod:{}'.format(module_prefix)
            tcl_prefix = 'config:module_roots:tcl:{}'.format(module_prefix)
            spack.config.add(lmod_prefix, scope=env_scope)
            spack.config.add(tcl_prefix, scope=env_scope)

        # Merge the original spack.yaml template back in
        # so it has the higest precedence
        for section in spack.config.section_schemas.keys():
            original = original_sections.get(section, {})
            existing = spack.config.get(section, scope=env_scope)
            new = spack.config.merge_yaml(existing, original)
            if section in existing:
                spack.config.set(section, new[section], env_scope)

        with env.write_transaction():
            specs = spack.cmd.parse_specs(self.specs)
            for spec in specs:
                env.add(spec)

            env.write()

        ev.deactivate()

        logging.info('Successfully wrote environment at {}'.format(env_file))
