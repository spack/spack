# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty
import spack
import llnl.util.filesystem as fs
import spack.modules
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.schema.env
import spack.config
import spack.cmd.spec
import spack.cmd.install
import spack.cmd.uninstall
import spack.cmd.module
import spack.cmd.common.arguments as arguments
from spack.config import ConfigScope
from spack.spec import Spec, CompilerSpec, FlagMap
from spack.repo import Repo
from spack.version import VersionList
from contextlib import contextmanager

import argparse
try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest
import os
import sys
import shutil

description = "group a subset of packages"
section = "environment"
level = "long"

_db_dirname = fs.join_path(spack.paths.var_path, 'environments')


def get_env_root(name):
    """Given an environment name, determines its root directory"""
    return fs.join_path(_db_dirname, name)


def get_dotenv_dir(env_root):
    """@return Directory in an environment that is owned by Spack"""
    return fs.join_path(env_root, '.env')


def get_write_paths(env_root):
    """Determines the names of temporary and permanent directories to
    write machine-generated environment info."""
    tmp_new = fs.join_path(env_root, '.env.new')
    dest = get_dotenv_dir(env_root)
    tmp_old = fs.join_path(env_root, '.env.old')
    return tmp_new, dest, tmp_old


class Environment(object):
    def clear(self):
        self.user_specs = list()
        self.concretized_order = list()
        self.specs_by_hash = dict()

    def __init__(self, name):
        self.name = name
        self.clear()

        # Default config
        self.yaml = {
            'configs': ['<env>'],
            'specs': []
        }

    @property
    def path(self):
        return get_env_root(self.name)

    def repo_path(self):
        return fs.join_path(get_dotenv_dir(self.path), 'repo')

    def add(self, user_spec, report_existing=True):
        """Add a single user_spec (non-concretized) to the Environment"""
        query_spec = Spec(user_spec)
        existing = set(x for x in self.user_specs
                       if Spec(x).name == query_spec.name)
        if existing:
            if report_existing:
                tty.die("Package {0} was already added to {1}"
                        .format(query_spec.name, self.name))
            else:
                tty.msg("Package {0} was already added to {1}"
                        .format(query_spec.name, self.name))
        else:
            tty.msg('Adding %s to environment %s' % (user_spec, self.name))
            self.user_specs.append(user_spec)

    def remove(self, query_spec):
        """Remove specs from an environment that match a query_spec"""
        query_spec = Spec(query_spec)
        match_index = -1
        for i, spec in enumerate(self.user_specs):
            if Spec(spec).name == query_spec.name:
                match_index = i
                break

        if match_index < 0:
            tty.die("Not found: {0}".format(query_spec))

        del self.user_specs[match_index]
        if match_index < len(self.concretized_order):
            spec_hash = self.concretized_order[match_index]
            del self.concretized_order[match_index]
            del self.specs_by_hash[spec_hash]

    def concretize(self, force=False):
        """Concretize user_specs in an Environment, creating (fully
        concretized) specs.

        force: bool
           If set, re-concretize ALL specs, even those that were
           already concretized.
        """

        if force:
            # Clear previously concretized specs
            self.specs_by_hash = dict()
            self.concretized_order = list()

        num_concretized = len(self.concretized_order)
        new_specs = list()
        for user_spec in self.user_specs[num_concretized:]:
            tty.msg('Concretizing %s' % user_spec)

            spec = spack.cmd.parse_specs(user_spec)[0]
            spec.concretize()
            new_specs.append(spec)
            dag_hash = spec.dag_hash()
            self.specs_by_hash[dag_hash] = spec
            self.concretized_order.append(spec.dag_hash())

            # Display concretized spec to the user
            sys.stdout.write(spec.tree(
                recurse_dependencies=True, install_status=True,
                hashlen=7, hashes=True))

        return new_specs

    def install(self, install_args=None):
        """Do a `spack install` on all the (concretized)
        specs in an Environment."""

        # Make sure log directory exists
        logs = fs.join_path(self.path, 'logs')
        try:
            os.makedirs(logs)
        except OSError:
            if not os.path.isdir(logs):
                raise

        for concretized_hash in self.concretized_order:
            spec = self.specs_by_hash[concretized_hash]

            # Parse cli arguments and construct a dictionary
            # that will be passed to Package.do_install API
            kwargs = dict()
            if install_args:
                spack.cmd.install.update_kwargs_from_args(install_args, kwargs)
            with pushd(self.path):
                spec.package.do_install(**kwargs)

                # Link the resulting log file into logs dir
                logname = '%s-%s.log' % (spec.name, spec.dag_hash(7))
                logpath = fs.join_path(logs, logname)
                try:
                    os.remove(logpath)
                except OSError:
                    pass
                os.symlink(spec.package.build_log_path, logpath)

    def uninstall(self, args):
        """Uninstall all the specs in an Environment."""
        specs = self._get_environment_specs(recurse_dependencies=True)
        args.all = False
        spack.cmd.uninstall.uninstall_specs(args, specs)

    def list(self, stream, **kwargs):
        """List the specs in an environment."""
        for user_spec, concretized_hash in zip_longest(
                self.user_specs, self.concretized_order):

            stream.write('========= {0}\n'.format(user_spec))

            if concretized_hash:
                concretized_spec = self.specs_by_hash[concretized_hash]
                stream.write(concretized_spec.tree(**kwargs))

    def upgrade_dependency(self, dep_name, dry_run=False):
        # TODO: if you have
        # w -> x -> y
        # and
        # v -> x -> y
        # then it would be desirable to ensure that w and v refer to the
        # same x after upgrading y. This is not currently guaranteed.
        new_order = list()
        new_deps = list()
        for i, spec_hash in enumerate(self.concretized_order):
            spec = self.specs_by_hash[spec_hash]
            if dep_name in spec:
                if dry_run:
                    tty.msg("Would upgrade {0} for {1}"
                            .format(spec[dep_name].format(), spec.format()))
                else:
                    new_spec = upgrade_dependency_version(spec, dep_name)
                    new_order.append(new_spec.dag_hash())
                    self.specs_by_hash[new_spec.dag_hash()] = new_spec
                    new_deps.append(new_spec[dep_name])
            else:
                new_order.append(spec_hash)

        if not dry_run:
            self.concretized_order = new_order
            return new_deps[0] if new_deps else None

    def reset_os_and_compiler(self, compiler=None):
        new_order = list()
        new_specs_by_hash = {}
        for spec_hash in self.concretized_order:
            spec = self.specs_by_hash[spec_hash]
            new_spec = reset_os_and_compiler(spec, compiler)
            new_order.append(new_spec.dag_hash())
            new_specs_by_hash[new_spec.dag_hash()] = new_spec
        self.concretized_order = new_order
        self.specs_by_hash = new_specs_by_hash

    def _get_environment_specs(self, recurse_dependencies=True):
        """Returns the specs of all the packages in an environment.
        If these specs appear under different user_specs, only one copy
        is added to the list returned."""
        package_to_spec = {}
        spec_list = list()

        for spec_hash in self.concretized_order:
            spec = self.specs_by_hash[spec_hash]

            specs = spec.traverse(deptype=('link', 'run')) \
                if recurse_dependencies else (spec,)
            for dep in specs:
                if dep.name in package_to_spec:
                    tty.warn("{0} takes priority over {1}"
                             .format(package_to_spec[dep.name].format(),
                                     dep.format()))
                else:
                    package_to_spec[dep.name] = dep
                    spec_list.append(dep)

        return spec_list

    def to_dict(self):
        """Used in serializing to JSON"""
        concretized_order = list(self.concretized_order)
        concrete_specs = dict()
        for spec in self.specs_by_hash.values():
            for s in spec.traverse():
                if s.dag_hash() not in concrete_specs:
                    concrete_specs[s.dag_hash()] = (
                        s.to_node_dict(all_deps=True))
        format = {
            'user_specs': self.user_specs,
            'concretized_order': concretized_order,
            'concrete_specs': concrete_specs,
        }
        return format

    @staticmethod
    def from_dict(name, d):
        """Used in deserializing from JSON"""
        env = Environment(name)
        env.user_specs = list(d['user_specs'])
        env.concretized_order = list(d['concretized_order'])
        specs_dict = d['concrete_specs']

        hash_to_node_dict = specs_dict
        root_hashes = set(env.concretized_order)

        specs_by_hash = {}
        for dag_hash, node_dict in hash_to_node_dict.items():
            specs_by_hash[dag_hash] = Spec.from_node_dict(node_dict)

        for dag_hash, node_dict in hash_to_node_dict.items():
            for dep_name, dep_hash, deptypes in (
                    Spec.dependencies_from_node_dict(node_dict)):
                specs_by_hash[dag_hash]._add_dependency(
                    specs_by_hash[dep_hash], deptypes)

        env.specs_by_hash = dict(
            (x, y) for x, y in specs_by_hash.items() if x in root_hashes)

        return env


def reset_os_and_compiler(spec, compiler=None):
    spec = spec.copy()
    for x in spec.traverse():
        x.compiler = None
        x.architecture = None
        x.compiler_flags = FlagMap(x)
        x._concrete = False
        x._hash = None
    if compiler:
        spec.compiler = CompilerSpec(compiler)
    spec.concretize()
    return spec


def upgrade_dependency_version(spec, dep_name):
    spec = spec.copy()
    for x in spec.traverse():
        x._concrete = False
        x._normal = False
        x._hash = None
    spec[dep_name].versions = VersionList(':')
    spec.concretize()
    return spec


def check_consistent_env(env_root):
    tmp_new, dest, tmp_old = get_write_paths(env_root)
    if os.path.exists(tmp_new) or os.path.exists(tmp_old):
        tty.die("Partial write state, run 'spack env repair'")


def write(environment, new_repo=None):
    """Writes an in-memory environment back to its location on disk,
    in an atomic manner."""

    tmp_new, dest, tmp_old = get_write_paths(get_env_root(environment.name))

    # Write the machine-generated stuff
    fs.mkdirp(tmp_new)
    # create one file for the environment object
    with open(fs.join_path(tmp_new, 'environment.json'), 'w') as f:
        sjson.dump(environment.to_dict(), stream=f)

    dest_repo_dir = fs.join_path(tmp_new, 'repo')
    if new_repo:
        shutil.copytree(new_repo.root, dest_repo_dir)
    elif os.path.exists(environment.repo_path()):
        shutil.copytree(environment.repo_path(), dest_repo_dir)

    # Swap in new directory atomically
    if os.path.exists(dest):
        shutil.move(dest, tmp_old)
    shutil.move(tmp_new, dest)
    if os.path.exists(tmp_old):
        shutil.rmtree(tmp_old)


def repair(environment_name):
    """Recovers from crash during critical section of write().
    Possibilities:

        tmp_new, dest
        tmp_new, tmp_old
        tmp_old, dest
    """
    tmp_new, dest, tmp_old = get_write_paths(get_env_root(environment_name))
    if os.path.exists(tmp_old):
        if not os.path.exists(dest):
            shutil.move(tmp_new, dest)
        else:
            shutil.rmtree(tmp_old)
        tty.info("Previous update completed")
    elif os.path.exists(tmp_new):
        tty.info("Previous update did not complete")
    else:
        tty.info("Previous update may have completed")

    if os.path.exists(tmp_new):
        shutil.rmtree(tmp_new)


def read(environment_name):
    # Check that env is in a consistent state on disk
    env_root = get_env_root(environment_name)

    # Read env.yaml file
    env_yaml = spack.config._read_config_file(
        fs.join_path(env_root, 'env.yaml'),
        spack.schema.env.schema)

    dotenv_dir = get_dotenv_dir(env_root)
    with open(fs.join_path(dotenv_dir, 'environment.json'), 'r') as f:
        environment_dict = sjson.load(f)
    environment = Environment.from_dict(environment_name, environment_dict)
    if env_yaml:
        environment.yaml = env_yaml['env']

    return environment


# =============== Modifies Environment

def environment_create(args):
    if os.path.exists(get_env_root(args.environment)):
        raise tty.die("Environment already exists: " + args.environment)

    _environment_create(args.environment)


def _environment_create(name, init_config=None):
    environment = Environment(name)

    user_specs = list()
    config_sections = {}
    if init_config:
        for key, val in init_config.items():
            if key == 'user_specs':
                user_specs.extend(val)
            else:
                config_sections[key] = val

    for user_spec in user_specs:
        environment.add(user_spec)

    write(environment)

    # When creating the environment, the user may specify configuration
    # to place in the environment initially. Spack does not interfere
    # with this configuration after initialization so it is handled here
    if len(config_sections) > 0:
        config_basedir = fs.join_path(environment.path, 'config')
        os.mkdir(config_basedir)
        for key, val in config_sections.items():
            yaml_section = syaml.dump({key: val}, default_flow_style=False)
            yaml_file = '{0}.yaml'.format(key)
            yaml_path = fs.join_path(config_basedir, yaml_file)
            with open(yaml_path, 'w') as f:
                f.write(yaml_section)


def environment_add(args):
    check_consistent_env(get_env_root(args.environment))
    environment = read(args.environment)
    parsed_specs = spack.cmd.parse_specs(args.package)

    if args.all:
        # Don't allow command-line specs with --all
        if len(parsed_specs) > 0:
            tty.die('Cannot specify --all and specs too on the command line')

        yaml_specs = environment.yaml['specs']
        if len(yaml_specs) == 0:
            tty.msg('No specs to add from env.yaml')

        # Add list of specs from env.yaml file
        for user_spec, _ in yaml_specs.items():    # OrderedDict
            environment.add(str(user_spec), report_existing=False)
    else:
        for spec in parsed_specs:
            environment.add(str(spec))

    write(environment)


def environment_remove(args):
    check_consistent_env(get_env_root(args.environment))
    environment = read(args.environment)
    if args.all:
        environment.clear()
    else:
        for spec in spack.cmd.parse_specs(args.package):
            environment.remove(spec.format())
    write(environment)


def environment_spec(args):
    environment = read(args.environment)
    prepare_repository(environment, use_repo=args.use_repo)
    prepare_config_scope(environment)
    spack.cmd.spec.spec(None, args)


def environment_concretize(args):
    check_consistent_env(get_env_root(args.environment))
    environment = read(args.environment)
    _environment_concretize(
        environment, use_repo=args.use_repo, force=args.force)


def _environment_concretize(environment, use_repo=False, force=False):
    """Function body separated out to aid in testing."""

    # Change global search paths
    repo = prepare_repository(environment, use_repo=use_repo)
    prepare_config_scope(environment)

    new_specs = environment.concretize(force=force)

    for spec in new_specs:
        for dep in spec.traverse():
            dump_to_environment_repo(dep, repo)

    # Moves <env>/.env.new to <env>/.env
    write(environment, repo)

# =============== Does not Modify Environment


def environment_install(args):
    check_consistent_env(get_env_root(args.environment))
    environment = read(args.environment)
    prepare_repository(environment, use_repo=args.use_repo)
    environment.install(args)


def environment_uninstall(args):
    check_consistent_env(get_env_root(args.environment))
    environment = read(args.environment)
    prepare_repository(environment)
    environment.uninstall(args)

# =======================================


def dump_to_environment_repo(spec, repo):
    dest_pkg_dir = repo.dirname_for_package_name(spec.name)
    if not os.path.exists(dest_pkg_dir):
        spack.repo.path.dump_provenance(spec, dest_pkg_dir)


def prepare_repository(environment, remove=None, use_repo=False):
    """Adds environment's repository to the global search path of repos"""
    import tempfile
    repo_stage = tempfile.mkdtemp()
    new_repo_dir = fs.join_path(repo_stage, 'repo')
    if os.path.exists(environment.repo_path()):
        shutil.copytree(environment.repo_path(), new_repo_dir)
    else:
        spack.repo.create_repo(new_repo_dir, environment.name)
    if remove:
        remove_dirs = []
        repo = Repo(new_repo_dir)
        for pkg_name in remove:
            remove_dirs.append(repo.dirname_for_package_name(pkg_name))
        for d in remove_dirs:
            shutil.rmtree(d)
    repo = Repo(new_repo_dir)
    if use_repo:
        spack.repo.put_first(repo)
    return repo


def prepare_config_scope(environment):
    """Adds environment's scope to the global search path
    of configuration scopes"""

    # Load up configs
    for config_spec in environment.yaml['configs']:
        config_name = os.path.split(config_spec)[1]
        if config_name == '<env>':
            # Use default config for the environment; doesn't have to exist
            config_dir = fs.join_path(environment.path, 'config')
            if not os.path.isdir(config_dir):
                continue
            config_name = environment.name
        else:
            # Use external user-provided config
            config_dir = os.path.normpath(os.path.join(
                environment.path, config_spec.format(**os.environ)))
            if not os.path.isdir(config_dir):
                tty.die('Spack config %s (%s) not found' %
                        (config_name, config_dir))

        tty.msg('Using Spack config %s scope at %s' %
                (config_name, config_dir))
        spack.config.config.push_scope(ConfigScope(config_name, config_dir))


def environment_relocate(args):
    environment = read(args.environment)
    prepare_repository(environment, use_repo=args.use_repo)
    environment.reset_os_and_compiler(compiler=args.compiler)
    write(environment)


def environment_list(args):
    # TODO? option to list packages w/ multiple instances?
    environment = read(args.environment)
    import sys
    environment.list(
        sys.stdout, recurse_dependencies=args.recurse_dependencies,
        hashes=args.long or args.very_long,
        hashlen=None if args.very_long else 7,
        install_status=args.install_status)


def environment_stage(args):
    environment = read(args.environment)
    prepare_repository(environment, use_repo=args.use_repo)
    for spec in environment.specs_by_hash.values():
        for dep in spec.traverse():
            dep.package.do_stage()


def environment_location(args):
    environment = read(args.environment)
    print(environment.path)


@contextmanager
def redirect_stdout(ofname):
    """Redirects STDOUT to (by default) a file within the environment;
    or else a user-specified filename."""
    with open(ofname, 'w') as f:
        original = sys.stdout
        sys.stdout = f
        yield
        sys.stdout = original


@contextmanager
def pushd(dir):
    original = os.getcwd()
    os.chdir(dir)
    yield
    os.chdir(original)


def environment_loads(args):
    # Set the module types that have been selected
    module_types = args.module_type
    if module_types is None:
        # If no selection has been made select all of them
        module_types = ['tcl']

    module_types = list(set(module_types))

    environment = read(args.environment)
    recurse_dependencies = args.recurse_dependencies
    args.recurse_dependencies = False
    ofname = fs.join_path(environment.path, 'loads')
    with redirect_stdout(ofname):
        specs = environment._get_environment_specs(
            recurse_dependencies=recurse_dependencies)
        spack.cmd.module.loads(module_types, specs, args)

    print('To load this environment, type:')
    print('   source %s' % ofname)


def environment_upgrade_dependency(args):
    environment = read(args.environment)
    repo = prepare_repository(
        environment, use_repo=args.use_repo, remove=[args.dep_name])
    new_dep = environment.upgrade_dependency(args.dep_name, args.dry_run)
    if not args.dry_run and new_dep:
        dump_to_environment_repo(new_dep, repo)
        write(environment, repo)


def add_use_repo_argument(cmd_parser):
    cmd_parser.add_argument(
        '--use-env-repo', action='store_true', dest='use_repo',
        help='Use package definitions stored in the environment'
    )


def setup_parser(subparser):
    subparser.add_argument(
        'environment',
        help="The environment you are working with"
    )

    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='environment_command')

    create_parser = sp.add_parser('create', help='Make an environment')
    create_parser.add_argument(
        '--init-file', dest='init_file',
        help='File with user specs to add and configuration yaml to use'
    )

    add_parser = sp.add_parser('add', help='Add a spec to an environment')
    add_parser.add_argument(
        '-a', '--all', action='store_true', dest='all',
        help="Add all specs listed in env.yaml")
    add_parser.add_argument(
        'package',
        nargs=argparse.REMAINDER,
        help="Spec of the package to add"
    )

    remove_parser = sp.add_parser(
        'remove', help='Remove a spec from this environment')
    remove_parser.add_argument(
        '-a', '--all', action='store_true', dest='all',
        help="Remove all specs from (clear) the environment")
    remove_parser.add_argument(
        'package',
        nargs=argparse.REMAINDER,
        help="Spec of the package to remove"
    )

    spec_parser = sp.add_parser(
        'spec', help='Concretize sample spec')
    spack.cmd.spec.add_common_arguments(spec_parser)
    add_use_repo_argument(spec_parser)

    concretize_parser = sp.add_parser(
        'concretize', help='Concretize user specs')
    concretize_parser.add_argument(
        '-f', '--force', action='store_true',
        help="Re-concretize even if already concretized.")
    add_use_repo_argument(concretize_parser)

    relocate_parser = sp.add_parser(
        'relocate',
        help='Reconcretize environment with new OS and/or compiler')
    relocate_parser.add_argument(
        '--compiler',
        help="Compiler spec to use"
    )
    add_use_repo_argument(relocate_parser)

    list_parser = sp.add_parser('list', help='List specs in an environment')
    arguments.add_common_arguments(
        list_parser,
        ['recurse_dependencies', 'long', 'very_long', 'install_status'])

    loads_parser = sp.add_parser(
        'loads',
        help='List modules for an installed environment '
        '(see spack module loads)')
    spack.cmd.modules.add_loads_arguments(loads_parser)

    sp.add_parser(
        'location',
        help='Print the root directory of the environment')

    upgrade_parser = sp.add_parser(
        'upgrade',
        help='''Upgrade a dependency package in an environment to the latest
version''')
    upgrade_parser.add_argument(
        'dep_name', help='Dependency package to upgrade')
    upgrade_parser.add_argument(
        '--dry-run', action='store_true', dest='dry_run',
        help="Just show the updates that would take place")
    add_use_repo_argument(upgrade_parser)

    stage_parser = sp.add_parser(
        'stage',
        help='Download all source files for all packages in an environment')
    add_use_repo_argument(stage_parser)

    config_update_parser = sp.add_parser(
        'update-config',
        help='Add config yaml file to environment')
    config_update_parser.add_argument(
        'config_files',
        nargs=argparse.REMAINDER,
        help="Configuration files to add"
    )

    install_parser = sp.add_parser(
        'install',
        help='Install all concretized specs in an environment')
    spack.cmd.install.add_common_arguments(install_parser)
    add_use_repo_argument(install_parser)

    uninstall_parser = sp.add_parser(
        'uninstall',
        help='Uninstall all concretized specs in an environment')
    spack.cmd.uninstall.add_common_arguments(uninstall_parser)


def env(parser, args, **kwargs):
    action = {
        'create': environment_create,
        'add': environment_add,
        'spec': environment_spec,
        'concretize': environment_concretize,
        'list': environment_list,
        'loads': environment_loads,
        'location': environment_location,
        'remove': environment_remove,
        'relocate': environment_relocate,
        'upgrade': environment_upgrade_dependency,
        'stage': environment_stage,
        'install': environment_install,
        'uninstall': environment_uninstall
    }
    action[args.environment_command](args)
