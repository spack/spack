# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys
import shutil
from contextlib import contextmanager
from six.moves import zip_longest

import jsonschema
import ruamel.yaml

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.error
import spack.repo
import spack.schema.env
import spack.spec
import spack.util.spack_json as sjson
import spack.config
from spack.spec import Spec, CompilerSpec, FlagMap
from spack.version import VersionList


#: currently activated environment
active = None


#: path where environments are stored in the spack tree
env_path = os.path.join(spack.paths.var_path, 'environments')


#: Name of the input yaml file in an environment
env_yaml_name = 'env.yaml'


#: Name of the lock file with concrete specs
env_lock_name = 'env.lock'


#: default env.yaml file to put in new environments
default_env_yaml = """\
# This is a Spack Environment file.
#
# It describes a set of packages to be installed, along with
# configuration settings.
env:
  # add package specs to the `specs` list
  specs:
  -
"""
#: regex for validating enviroment names
valid_environment_name_re = r'^\w[\w-]*$'

#: version of the lockfile format. Must increase monotonically.
lockfile_format_version = 1

#: legal first keys in an environment.yaml file
env_schema_keys = ('env', 'spack')

#: jsonschema validator for environments
_validator = None


def valid_env_name(name):
    return re.match(valid_environment_name_re, name)


def validate_env_name(name):
    if not valid_env_name(name):
        raise ValueError((
            "'%s': names must start with a letter, and only contain "
            "letters, numbers, _, and -.") % name)
    return name


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
    if exact:
        spack.repo.path.put_first(active.repo)

    tty.debug("Using environmennt '%s'" % active.name)


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
    return os.path.join(env_path, name)


def exists(name):
    """Whether an environment exists or not."""
    return os.path.exists(root(name))


def manifest_path(name):
    return os.path.join(root(name), env_yaml_name)


def lockfile_path(name):
    return os.path.join(root(name), env_lock_name)


def dotenv_path(env_root):
    """@return Directory in an environment that is owned by Spack"""
    return os.path.join(env_root, '.env')


def repos_path(dotenv_path):
    return os.path.join(dotenv_path, 'repos')


def log_path(dotenv_path):
    return os.path.join(dotenv_path, 'logs')


def config_dict(yaml_data):
    """Get the configuration scope section out of an env.yaml"""
    key = spack.config.first_existing(yaml_data, env_schema_keys)
    return yaml_data[key]


def list_environments():
    """List the names of environments that currently exist."""
    # just return empty if the env path does not exist.  A read-only
    # operation like list should not try to create a directory.
    if not os.path.exists(env_path):
        return []

    candidates = sorted(os.listdir(env_path))
    names = []
    for candidate in candidates:
        yaml_path = os.path.join(root(candidate), env_yaml_name)
        if valid_env_name(candidate) and os.path.exists(yaml_path):
            names.append(candidate)
    return names


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


def validate(data, filename=None):
    global _validator
    if _validator is None:
        _validator = jsonschema.Draft4Validator(spack.schema.env.schema)
    try:
        _validator.validate(data)
    except jsonschema.ValidationError as e:
        raise spack.config.ConfigFormatError(
            e, data, filename, e.instance.lc.line + 1)


def _read_yaml(str_or_file):
    """Read YAML from a file for round-trip parsing."""
    data = ruamel.yaml.load(str_or_file, ruamel.yaml.RoundTripLoader)
    filename = getattr(str_or_file, 'name', None)
    validate(data, filename)
    return data


def _write_yaml(data, str_or_file):
    """Write YAML to a file preserving comments and dict order."""
    filename = getattr(str_or_file, 'name', None)
    validate(data, filename)
    ruamel.yaml.dump(data, str_or_file, Dumper=ruamel.yaml.RoundTripDumper,
                     default_flow_style=False)


class Environment(object):
    def __init__(self, name, env_yaml=None):
        """Create a new environment, optionally with an initialization file.

        Arguments:
            name (str): name for this environment
            env_yaml (str or file): raw YAML or a file to initialize the
                environment
        """
        self.name = validate_env_name(name)
        self.clear()

        # use read_yaml to preserve comments
        if env_yaml is None:
            env_yaml = default_env_yaml
        self.yaml = _read_yaml(env_yaml)

        # initialize user specs from the YAML
        spec_list = config_dict(self.yaml).get('specs')
        if spec_list:
            self.user_specs = [Spec(s) for s in spec_list if s is not None]

    def clear(self):
        self.user_specs = []              # current user specs
        self.concretized_user_specs = []  # user specs from last concretize
        self.concretized_order = []       # roots of last concretize, in order
        self.specs_by_hash = {}           # concretized specs by hash
        self._repo = None                 # RepoPath for this env (memoized)

    @property
    def path(self):
        return root(self.name)

    @property
    def manifest_path(self):
        return manifest_path(self.name)

    @property
    def lock_path(self):
        return lockfile_path(self.name)

    @property
    def dotenv_path(self):
        return dotenv_path(self.path)

    @property
    def repos_path(self):
        return repos_path(self.dotenv_path)

    @property
    def repo(self):
        if self._repo is None:
            self._repo = make_repo_path(self.repos_path)
        return self._repo

    def included_config_scopes(self):
        """List of included configuration scopes from the environment.

        Scopes are in order from lowest to highest precedence, i.e., the
        order they should be pushed on the stack, but the opposite of the
        order they appaer in the env.yaml file.
        """
        scopes = []

        # load config scopes added via 'include:', in reverse so that
        # highest-precedence scopes are last.
        includes = config_dict(self.yaml).get('include', [])
        for i, config_path in enumerate(reversed(includes)):
            # allow paths to contain environment variables
            config_path = config_path.format(**os.environ)

            # treat relative paths as relative to the environment
            if not os.path.isabs(config_path):
                config_path = os.path.join(self.path, config_path)
                config_path = os.path.normpath(os.path.realpath(config_path))

            if os.path.isdir(config_path):
                # directories are treated as regular ConfigScopes
                config_name = 'env:%s:%s' % (
                    self.name, os.path.basename(config_path))
                scope = spack.config.ConfigScope(config_name, config_path)
            else:
                # files are assumed to be SingleFileScopes
                base, ext = os.path.splitext(os.path.basename(config_path))
                config_name = 'env:%s:%s' % (self.name, base)
                scope = spack.config.SingleFileScope(
                    config_name, config_path, spack.schema.merged.schema)

            scopes.append(scope)

        return scopes

    def env_file_config_scope(self):
        """Get the configuration scope for the environment's manifest file."""
        config_name = 'env:%s' % self.name
        return spack.config.SingleFileScope(config_name,
                                            self.manifest_path,
                                            spack.schema.env.schema,
                                            [env_schema_keys])

    def config_scopes(self):
        """A list of all configuration scopes for this environment."""
        return self.included_config_scopes() + [self.env_file_config_scope()]

    def destroy(self):
        """Remove this environment from Spack entirely."""
        shutil.rmtree(self.path)

    def add(self, user_spec, report_existing=True):
        """Add a single user_spec (non-concretized) to the Environment

        Returns:
            (bool): True if the spec was added, False if it was already
                present and did not need to be added

        """
        spec = Spec(user_spec)

        existing = set(s for s in self.user_specs if s.name == spec.name)
        if not existing:
            self.user_specs.append(spec)
        return bool(not existing)

    def remove(self, query_spec):
        """Remove specs from an environment that match a query_spec"""
        query_spec = Spec(query_spec)
        matches = [s for s in self.user_specs if s.satisfies(query_spec)]

        if not matches:
            raise EnvError("Not found: {0}".format(query_spec))

        for spec in matches:
            self.user_specs.remove(spec)
            if spec in self.concretized_user_specs:
                i = self.concretized_user_specs.index(spec)
                del self.concretized_user_specs[i]

                dag_hash = self.concretized_order[i]
                del self.concretized_order[i]
                del self.specs_by_hash[dag_hash]

    def concretize(self, force=False):
        """Concretize user_specs in this environment.

        Only concretizes specs that haven't been concretized yet unless
        force is ``True``.

        This only modifies the environment in memory. ``write()`` will
        write out a lockfile containing concretized specs.

        Arguments:
            force (bool): re-concretize ALL specs, even those that were
               already concretized

        Return:
            (list): list of newly concretized specs

        """
        if force:
            # Clear previously concretized specs
            self.concretized_user_specs = []
            self.concretized_order = []
            self.specs_by_hash = {}

        # keep any concretized specs whose user specs are still in the manifest
        new_concretized_user_specs = []
        new_concretized_order = []
        new_specs_by_hash = {}
        for s, h in zip(self.concretized_user_specs, self.concretized_order):
            if s in self.user_specs:
                new_concretized_user_specs.append(s)
                new_concretized_order.append(h)
                new_specs_by_hash[h] = self.specs_by_hash[h]

        # concretize any new user specs that we haven't concretized yet
        new_specs = []
        for uspec in self.user_specs:
            if uspec not in new_concretized_user_specs:
                tty.msg('Concretizing %s' % uspec)
                cspec = uspec.concretized()
                dag_hash = cspec.dag_hash()

                new_concretized_user_specs.append(uspec)
                new_concretized_order.append(dag_hash)
                new_specs_by_hash[dag_hash] = cspec
                new_specs.append(cspec)

                # Display concretized spec to the user
                sys.stdout.write(cspec.tree(
                    recurse_dependencies=True, install_status=True,
                    hashlen=7, hashes=True))

        # save the new concretized state
        self.concretized_user_specs = new_concretized_user_specs
        self.concretized_order = new_concretized_order
        self.specs_by_hash = new_specs_by_hash

        # return only the newly concretized specs
        return new_specs

    def install(self, install_args=None):
        """Do a `spack install` on all the (concretized)
           specs in an Environment."""

        # Make sure log directory exists
        logs_dir = log_path(self.dotenv_path)
        fs.mkdirp(logs_dir)

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
                build_log_link = os.path.join(
                    logs_dir, '%s-%s.log' % (spec.name, spec.dag_hash(7)))
                if os.path.exists(build_log_link):
                    os.remove(build_log_link)
                os.symlink(spec.package.build_log_path, build_log_link)

    def uninstall(self, args):
        """Uninstall all the specs in an Environment."""
        specs = self._get_environment_specs(recurse_dependencies=True)
        args.all = False
        spack.cmd.uninstall.uninstall_specs(args, specs)

    def status(self, stream, **kwargs):
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

    def _to_lockfile_dict(self):
        """Create a dictionary to store a lockfile for this environment."""
        concrete_specs = {}
        for spec in self.specs_by_hash.values():
            for s in spec.traverse():
                dag_hash = s.dag_hash()
                if dag_hash not in concrete_specs:
                    concrete_specs[dag_hash] = s.to_node_dict(all_deps=True)

        hash_spec_list = zip(
            self.concretized_order, self.concretized_user_specs)

        # this is the lockfile we'll write out
        data = {
            # metadata about the format
            '_meta': {
                'file-type': 'spack-lockfile',
                'lockfile-version': lockfile_format_version,
            },

            # users specs + hashes are the 'roots' of the environment
            'roots': [{
                'hash': h,
                'spec': str(s)
            } for h, s in hash_spec_list],

            # Concrete specs by hash, including dependencies
            'concrete_specs': concrete_specs,
        }

        return data

    def _read_lockfile_dict(self, d):
        """Read a lockfile dictionary into this environment."""
        roots = d['roots']
        self.concretized_user_specs = [Spec(r['spec']) for r in roots]
        self.concretized_order = [r['hash'] for r in roots]

        json_specs_by_hash = d['concrete_specs']
        root_hashes = set(self.concretized_order)

        specs_by_hash = {}
        for dag_hash, node_dict in json_specs_by_hash.items():
            specs_by_hash[dag_hash] = Spec.from_node_dict(node_dict)

        for dag_hash, node_dict in json_specs_by_hash.items():
            for dep_name, dep_hash, deptypes in (
                    Spec.dependencies_from_node_dict(node_dict)):
                specs_by_hash[dag_hash]._add_dependency(
                    specs_by_hash[dep_hash], deptypes)

        self.specs_by_hash = dict(
            (x, y) for x, y in specs_by_hash.items() if x in root_hashes)

    def write(self, dump_packages=None):
        """Writes an in-memory environment to its location on disk.

        Arguments:
            dump_packages (list of Spec): specs of packages whose
                package.py files should be written to the env's repo
        """
        # ensure path in var/spack/environments
        fs.mkdirp(self.path)

        if self.specs_by_hash:
            # ensure the prefix/.env directory exists
            tmp_env = '%s.tmp' % self.dotenv_path
            fs.mkdirp(tmp_env)

            # dump package.py files for specified specs
            tmp_repos_path = repos_path(tmp_env)
            dump_packages = dump_packages or []
            for spec in dump_packages:
                for dep in spec.traverse():
                    if not dep.concrete:
                        raise ValueError('specs passed to environment.write() '
                                         'must be concrete!')

                    root = os.path.join(tmp_repos_path, dep.namespace)
                    repo = spack.repo.create_or_construct(root, dep.namespace)
                    pkg_dir = repo.dirname_for_package_name(dep.name)

                    fs.mkdirp(pkg_dir)
                    spack.repo.path.dump_provenance(dep, pkg_dir)

            # move the new .env directory into place.
            move_move_rm(tmp_env, self.dotenv_path)

            # write the lock file last
            with write_tmp_and_move(self.lock_path) as f:
                sjson.dump(self._to_lockfile_dict(), stream=f)
        else:
            if os.path.exists(self.lock_path):
                os.unlink(self.lock_path)

        # invalidate _repo cache
        self._repo = None

        # put the new user specs in the YAML
        yaml_spec_list = config_dict(self.yaml).setdefault('specs', [])
        yaml_spec_list[:] = [str(s) for s in self.user_specs]

        # if all that worked, write out the manifest file at the top level
        with write_tmp_and_move(self.manifest_path) as f:
            _write_yaml(self.yaml, f)


def read(env_name):
    """Read environment state from disk."""
    env_root = root(env_name)
    if not os.path.isdir(env_root):
        raise EnvError("no such environment '%s'" % env_name)
    if not os.access(env_root, os.R_OK):
        raise EnvError("can't read environment '%s'" % env_name)

    # read yaml file
    with open(manifest_path(env_name)) as f:
        env = Environment(env_name, f.read())

    # read lockfile, if it exists
    lock_path = lockfile_path(env_name)
    if os.path.exists(lock_path):
        with open(lock_path) as f:
            lockfile_dict = sjson.load(f)
        env._read_lockfile_dict(lockfile_dict)

    return env


def move_move_rm(src, dest):
    """Move dest out of the way, put src in its place."""

    dirname = os.path.dirname(dest)
    basename = os.path.basename(dest)
    old = os.path.join(dirname, '.%s.old' % basename)

    if os.path.exists(dest):
        shutil.move(dest, old)
    shutil.move(src, dest)
    if os.path.exists(old):
        shutil.rmtree(old)


@contextmanager
def write_tmp_and_move(filename):
    """Write to a temporary file, then move into place."""
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    tmp = os.path.join(dirname, '.%s.tmp' % basename)
    with open(tmp, 'w') as f:
        yield f
    shutil.move(tmp, filename)


def make_repo_path(root):
    """Make a RepoPath from the repo subdirectories in an environment."""
    path = spack.repo.RepoPath()

    if os.path.isdir(root):
        for repo_root in os.listdir(root):
            repo_root = os.path.join(root, repo_root)

            if not os.path.isdir(repo_root):
                continue

            repo = spack.repo.Repo(repo_root)
            path.put_last(repo)

    return path


def prepare_config_scope(env):
    """Add env's scope to the global configuration search path."""
    for scope in env.config_scopes():
        spack.config.config.push_scope(scope)


class EnvError(spack.error.SpackError):
    """Superclass for all errors to do with Spack environments.

    Note that this is called ``EnvError`` to distinguish it from the
    builtin ``EnvironmentError``.
    """
