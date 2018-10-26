# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys
import shutil

import jsonschema
import ruamel.yaml

import llnl.util.filesystem as fs
import llnl.util.tty as tty
import llnl.util.tty.color as color

import spack.error
import spack.repo
import spack.schema.env
import spack.spec
import spack.util.spack_json as sjson
import spack.config
from spack.spec import Spec, CompilerSpec, FlagMap
from spack.version import VersionList


#: environment variable used to indicate the active environment
spack_env_var = 'SPACK_ENV'


#: currently activated environment
active = None


#: path where environments are stored in the spack tree
env_path = os.path.join(spack.paths.var_path, 'environments')


#: Name of the input yaml file for an environment
manifest_name = 'spack.yaml'


#: Name of the input yaml file for an environment
lockfile_name = 'spack.lock'


#: Name of the directory where environments store repos, logs, views
env_subdir_name = '.spack-env'


#: default spack.yaml file to put in new environments
default_manifest_yaml = """\
# This is a Spack Environment file.
#
# It describes a set of packages to be installed, along with
# configuration settings.
spack:
  # add package specs to the `specs` list
  specs:
  -
"""
#: regex for validating enviroment names
valid_environment_name_re = r'^\w[\w-]*$'

#: version of the lockfile format. Must increase monotonically.
lockfile_format_version = 1

#: legal first keys in the spack.yaml manifest file
env_schema_keys = ('spack', 'env')

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


def activate(env, use_env_repo=False):
    """Activate an environment.

    To activate an environment, we add its configuration scope to the
    existing Spack configuration, and we set active to the current
    environment.

    Arguments:
        env (Environment): the environment to activate
        use_env_repo (bool): use the packages exactly as they appear in the
            environment's repository

    TODO: Add support for views here.  Activation should set up the shell
    TODO: environment to use the activated spack environment.
    """
    global active

    active = env
    prepare_config_scope(active)
    if use_env_repo:
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

    deactivate_config_scope(active)

    # use _repo so we only remove if a repo was actually constructed
    if active._repo:
        spack.repo.path.remove(active._repo)

    tty.debug("Deactivated environmennt '%s'" % active.name)
    active = None


def disambiguate(env, env_dir=None):
    """Used to determine whether an environment is named or a directory."""
    if env:
        if exists(env):
            # treat env as a name
            return read(env)
        env_dir = env

    if not env_dir:
        env_dir = os.environ.get(spack_env_var)
        if not env_dir:
            return None

    if os.path.isdir(env_dir):
        if is_env_dir(env_dir):
            return Environment(env_dir)
        else:
            raise EnvError('no environment in %s' % env_dir)
        return

    return None


def root(name):
    """Get the root directory for an environment by name."""
    validate_env_name(name)
    return os.path.join(env_path, name)


def exists(name):
    """Whether an environment with this name exists or not."""
    if not valid_env_name(name):
        return False
    return os.path.isdir(root(name))


def is_env_dir(path):
    """Whether a directory contains a spack environment."""
    return os.path.isdir(path) and os.path.exists(
        os.path.join(path, manifest_name))


def read(name):
    """Get an environment with the supplied name."""
    validate_env_name(name)
    if not exists(name):
        raise EnvError("no such environment '%s'" % name)
    return Environment(root(name))


def create(name, init_file=None):
    """Create a named environment in Spack."""
    validate_env_name(name)
    if exists(name):
        raise EnvError("'%s': environment already exists" % name)
    return Environment(root(name), init_file)


def destroy(name):
    """Destroy a named environment."""
    validate_env_name(name)
    if not exists(name):
        raise EnvError("no such environment '%s'" % name)
    if not os.access(root(name), os.W_OK):
        raise EnvError(
            "insufficient permissions to modify environment: '%s'" % name)
    shutil.rmtree(root(name))


def config_dict(yaml_data):
    """Get the configuration scope section out of an spack.yaml"""
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
        yaml_path = os.path.join(root(candidate), manifest_name)
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
    def __init__(self, path, init_file=None):
        """Create a new environment.

        The environment can be optionally initialized with either a
        spack.yaml or spack.lock file.

        Arguments:
            path (str): path to the root directory of this environment
            init_file (str or file object): filename or file object to
                initialize the environment
        """
        self.path = os.path.abspath(path)
        self.clear()

        if init_file:
            # initialize the environment from a file if provided
            with fs.open_if_filename(init_file) as f:
                if hasattr(f, 'name') and f.name.endswith('.lock'):
                    # Initialize the environment from a lockfile
                    self._read_lockfile(f)
                    self._set_user_specs_from_lockfile()
                    self.yaml = _read_yaml(default_manifest_yaml)
                else:
                    # Initialize the environment from a spack.yaml file
                    self._read_manifest(f)
        else:
            # read lockfile, if it exists
            if os.path.exists(self.lock_path):
                with open(self.lock_path) as f:
                    self._read_lockfile(f)

            if os.path.exists(self.manifest_path):
                # read the spack.yaml file, if exists
                with open(self.manifest_path) as f:
                    self._read_manifest(f)

            elif self.concretized_user_specs:
                # if not, take user specs from the lockfile
                self._set_user_specs_from_lockfile()
                self.yaml = _read_yaml(default_manifest_yaml)
            else:
                # if there's no manifest or lockfile, use the default
                self._read_manifest(default_manifest_yaml)

    def _read_manifest(self, f):
        """Read manifest file and set up user specs."""
        self.yaml = _read_yaml(f)
        spec_list = config_dict(self.yaml).get('specs')
        if spec_list:
            self.user_specs = [Spec(s) for s in spec_list if s]

    def _set_user_specs_from_lockfile(self):
        """Copy user_specs from a read-in lockfile."""
        self.user_specs = [Spec(s) for s in self.concretized_user_specs]

    def clear(self):
        self.user_specs = []              # current user specs
        self.concretized_user_specs = []  # user specs from last concretize
        self.concretized_order = []       # roots of last concretize, in order
        self.specs_by_hash = {}           # concretized specs by hash
        self.new_specs = []               # write packages for these on write()
        self._repo = None                 # RepoPath for this env (memoized)
        self._previous_active = None      # previously active environment

    @property
    def name(self):
        return os.path.basename(self.path)

    @property
    def manifest_path(self):
        """Path to spack.yaml file in this environment."""
        return os.path.join(self.path, manifest_name)

    @property
    def lock_path(self):
        """Path to spack.lock file in this environment."""
        return os.path.join(self.path, lockfile_name)

    @property
    def env_subdir_path(self):
        """Path to directory where the env stores repos, logs, views."""
        return os.path.join(self.path, env_subdir_name)

    @property
    def repos_path(self):
        return os.path.join(self.path, env_subdir_name, 'repos')

    @property
    def log_path(self):
        return os.path.join(self.path, env_subdir_name, 'logs')

    @property
    def repo(self):
        if self._repo is None:
            self._repo = make_repo_path(self.repos_path)
        return self._repo

    def included_config_scopes(self):
        """List of included configuration scopes from the environment.

        Scopes are listed in the YAML file in order from highest to
        lowest precedence, so configuration from earlier scope will take
        precedence over later ones.

        This routine returns them in the order they should be pushed onto
        the internal scope stack (so, in reverse, from lowest to highest).
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

    def add(self, user_spec):
        """Add a single user_spec (non-concretized) to the Environment

        Returns:
            (bool): True if the spec was added, False if it was already
                present and did not need to be added

        """
        spec = Spec(user_spec)
        if not spec.name:
            raise EnvError('cannot add anonymous specs to an environment!')
        elif not spack.repo.path.exists(spec.name):
            raise EnvError('no such package: %s' % spec.name)

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
        """
        if force:
            # Clear previously concretized specs
            self.concretized_user_specs = []
            self.concretized_order = []
            self.specs_by_hash = {}

        # keep any concretized specs whose user specs are still in the manifest
        old_concretized_user_specs = self.concretized_user_specs
        old_concretized_order = self.concretized_order
        old_specs_by_hash = self.specs_by_hash

        self.concretized_user_specs = []
        self.concretized_order = []
        self.specs_by_hash = {}

        for s, h in zip(old_concretized_user_specs, old_concretized_order):
            if s in self.user_specs:
                concrete = old_specs_by_hash[h]
                self._add_concrete_spec(s, concrete, new=False)

        # concretize any new user specs that we haven't concretized yet
        for uspec in self.user_specs:
            if uspec not in old_concretized_user_specs:
                tty.msg('Concretizing %s' % uspec)
                concrete = uspec.concretized()
                self._add_concrete_spec(uspec, concrete)

                # Display concretized spec to the user
                sys.stdout.write(concrete.tree(
                    recurse_dependencies=True, install_status=True,
                    hashlen=7, hashes=True))

    def install(self, user_spec, install_args=None):
        """Install a single spec into an environment.

        This will automatically concretize the single spec, but it won't
        affect other as-yet unconcretized specs.
        """
        spec = Spec(user_spec)

        if self.add(spec):
            concrete = spec.concretized()
            self._add_concrete_spec(spec, concrete)
        else:
            # spec might be in the user_specs, but not installed.
            spec = next(s for s in self.user_specs if s.name == spec.name)
            concrete = self.specs_by_hash.get(spec.dag_hash())
            if not concrete:
                concrete = spec.concretized()
                self._add_concrete_spec(spec, concrete)

        concrete.package.do_install(**install_args)

    def _add_concrete_spec(self, spec, concrete, new=True):
        """Called when a new concretized spec is added to the environment.

        This ensures that all internal data structures are kept in sync.

        Arguments:
            spec (Spec): user spec that resulted in the concrete spec
            concrete (Spec): spec concretized within this environment
            new (bool): whether to write this spec's package to the env
                repo on write()
        """
        assert concrete.concrete

        # when a spec is newly concretized, we need to make a note so
        # that we can write its package to the env repo on write()
        if new:
            self.new_specs.append(concrete)

        # update internal lists of specs
        self.concretized_user_specs.append(spec)

        h = concrete.dag_hash()
        self.concretized_order.append(h)
        self.specs_by_hash[h] = concrete

    def install_all(self, args=None):
        """Install all concretized specs in an environment."""

        # Make sure log directory exists
        log_path = self.log_path
        fs.mkdirp(log_path)

        for concretized_hash in self.concretized_order:
            spec = self.specs_by_hash[concretized_hash]

            # Parse cli arguments and construct a dictionary
            # that will be passed to Package.do_install API
            kwargs = dict()
            if args:
                spack.cmd.install.update_kwargs_from_args(args, kwargs)

            with fs.working_dir(self.path):
                spec.package.do_install(**kwargs)

                # Link the resulting log file into logs dir
                build_log_link = os.path.join(
                    log_path, '%s-%s.log' % (spec.name, spec.dag_hash(7)))
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
        if self.path.startswith(env_path):
            name = os.path.basename(self.path)
        else:
            name = self.path

        tty.msg('In environment %s' % name)

        concretized = [(spec, self.specs_by_hash[h])
                       for spec, h in zip(self.concretized_user_specs,
                                          self.concretized_order)]

        added = [s for s in self.user_specs
                 if s not in self.concretized_user_specs]
        removed = [(s, c) for s, c in concretized if s not in self.user_specs]
        current = [(s, c) for s, c in concretized if s in self.user_specs]

        def write_kind(s):
            color.cwrite('@c{%s}\n' % str(s), stream)

        def write_user_spec(s, c):
            color.cwrite('@%s{----} %s\n' % (c, str(s)), stream)

        if added:
            write_kind('added:')
        for s in added:
            write_user_spec(s, 'g')

        if current:
            if added:
                stream.write('\n')
            write_kind('concrete:')
        for s, c in current:
            write_user_spec(s, 'K')
            stream.write(c.tree(**kwargs))

        if removed:
            if added or current:
                stream.write('\n')
            write_kind('removed:')
        for s, c in removed:
            write_user_spec(s, 'r')
            stream.write(c.tree(**kwargs))

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

    def _read_lockfile(self, file_or_json):
        """Read a lockfile from a file or from a raw string."""
        lockfile_dict = sjson.load(file_or_json)
        self._read_lockfile_dict(lockfile_dict)

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

    def write(self):
        """Writes an in-memory environment to its location on disk.

        This will also write out package files for each newly concretized spec.
        """
        # ensure path in var/spack/environments
        fs.mkdirp(self.path)

        if self.specs_by_hash:
            # ensure the prefix/.env directory exists
            fs.mkdirp(self.env_subdir_path)

            for spec in self.new_specs:
                for dep in spec.traverse():
                    if not dep.concrete:
                        raise ValueError('specs passed to environment.write() '
                                         'must be concrete!')

                    root = os.path.join(self.repos_path, dep.namespace)
                    repo = spack.repo.create_or_construct(root, dep.namespace)
                    pkg_dir = repo.dirname_for_package_name(dep.name)

                    fs.mkdirp(pkg_dir)
                    spack.repo.path.dump_provenance(dep, pkg_dir)
            self.new_specs = []

            # write the lock file last
            with fs.write_tmp_and_move(self.lock_path) as f:
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
        with fs.write_tmp_and_move(self.manifest_path) as f:
            _write_yaml(self.yaml, f)

    def __enter__(self):
        self._previous_active = active
        activate(self)
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        deactivate()
        if self._previous_active:
            activate(self._previous_active)


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


def deactivate_config_scope(env):
    """Remove any scopes from env from the global config path."""
    for scope in env.config_scopes():
        spack.config.config.remove_scope(scope.name)


class EnvError(spack.error.SpackError):
    """Superclass for all errors to do with Spack environments.

    Note that this is called ``EnvError`` to distinguish it from the
    builtin ``EnvironmentError``.
    """
