##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import os
import sys
import shutil
import tempfile
from six.moves import zip_longest

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.error
import spack.repo
import spack.schema.env
import spack.util.spack_json as sjson
from spack.config import ConfigScope
from spack.spec import Spec, CompilerSpec, FlagMap
from spack.version import VersionList


#: currently activated environment
active = None


#: path where environments are stored in the spack tree
env_path = fs.join_path(spack.paths.var_path, 'environments')


def activate(name, exact=False):
    """Activate an environment.

    To activate an environment, we add its configuration scope to the
    existing Spack configuration, and we set active to the current
    environment.

    Arguments:
        name (str): name of the environment to activate
        exact (bool): use the packages exactly as they appear in the
            environment's repository

    TODO: Add support for views here.  Activation should set up the shell
    TODO: environment to use the activated spack environment.
    """
    global active

    active = read(name)
    prepare_config_scope(active)
    prepare_repository(active, use_repo=exact)

    tty.msg("Using environmennt '%s'" % active.name)


def deactivate():
    """Undo any configuration or repo settings modified by ``activate()``.

    Returns:
        (bool): True if an environment was deactivated, False if no
        environment was active.

    """
    global active
    if not active:
        return


def root(name):
    """Get the root directory for an environment by name."""
    return fs.join_path(env_path, name)


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


def _reset_os_and_compiler(spec, compiler=None):
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


def _upgrade_dependency_version(spec, dep_name):
    spec = spec.copy()
    for x in spec.traverse():
        x._concrete = False
        x._normal = False
        x._hash = None
    spec[dep_name].versions = VersionList(':')
    spec.concretize()
    return spec


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
        return root(self.name)

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
            with fs.working_dir(self.path):
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
                    new_spec = _upgrade_dependency_version(spec, dep_name)
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
            new_spec = _reset_os_and_compiler(spec, compiler)
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


def check_consistency(name):
    """check whether an environment directory is consistent"""
    env_root = root(name)
    tmp_new, dest, tmp_old = get_write_paths(env_root)
    if os.path.exists(tmp_new) or os.path.exists(tmp_old):
        tty.die("Partial write state, run 'spack env repair'")


def write(environment, new_repo=None):
    """Writes an in-memory environment back to its location on disk,
    in an atomic manner."""

    tmp_new, dest, tmp_old = get_write_paths(root(environment.name))

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
    tmp_new, dest, tmp_old = get_write_paths(root(environment_name))
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
    """Read environment state from disk."""
    # Check that env is in a consistent state on disk
    env_root = root(environment_name)

    if not os.path.isdir(env_root):
        raise EnvError("no such environment '%s'" % environment_name)
    if not os.access(env_root, os.R_OK):
        raise EnvError("can't read environment '%s'" % environment_name)

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


def dump_to_environment_repo(spec, repo):
    dest_pkg_dir = repo.dirname_for_package_name(spec.name)
    if not os.path.exists(dest_pkg_dir):
        spack.repo.path.dump_provenance(spec, dest_pkg_dir)


def prepare_repository(environment, remove=None, use_repo=False):
    """Adds environment's repository to the global search path of repos"""
    repo_stage = tempfile.mkdtemp()
    new_repo_dir = fs.join_path(repo_stage, 'repo')
    if os.path.exists(environment.repo_path()):
        shutil.copytree(environment.repo_path(), new_repo_dir)
    else:
        spack.repo.create_repo(new_repo_dir, environment.name)
    if remove:
        remove_dirs = []
        repo = spack.repo.Repo(new_repo_dir)
        for pkg_name in remove:
            remove_dirs.append(repo.dirname_for_package_name(pkg_name))
        for d in remove_dirs:
            shutil.rmtree(d)
    repo = spack.repo.Repo(new_repo_dir)
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

        spack.config.config.push_scope(ConfigScope(config_name, config_dir))


class EnvError(spack.error.SpackError):
    """Superclass for all errors to do with Spack environments.

    Note that this is called ``EnvError`` to distinguish it from the
    builtin ``EnvironmentError``.
    """
