# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys
import shutil

import ruamel.yaml

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.error
import spack.repo
import spack.schema.env
import spack.spec
import spack.util.spack_json as sjson
import spack.config
from spack.spec import Spec


#: environment variable used to indicate the active environment
spack_env_var = 'SPACK_ENV'


#: currently activated environment
_active_environment = None


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
    global _active_environment

    _active_environment = env
    prepare_config_scope(_active_environment)
    if use_env_repo:
        spack.repo.path.put_first(_active_environment.repo)

    tty.debug("Using environmennt '%s'" % _active_environment.name)


def deactivate():
    """Undo any configuration or repo settings modified by ``activate()``.

    Returns:
        (bool): True if an environment was deactivated, False if no
        environment was active.

    """
    global _active_environment

    if not _active_environment:
        return

    deactivate_config_scope(_active_environment)

    # use _repo so we only remove if a repo was actually constructed
    if _active_environment._repo:
        spack.repo.path.remove(_active_environment._repo)

    tty.debug("Deactivated environmennt '%s'" % _active_environment.name)
    _active_environment = None


def find_environment(args):
    """Find active environment from args, spack.yaml, or environment variable.

    This is called in ``spack.main`` to figure out which environment to
    activate.

    Check for an environment in this order:
        1. via ``spack -e ENV`` or ``spack -D DIR`` (arguments)
        2. as a spack.yaml file in the current directory, or
        3. via a path in the SPACK_ENV environment variable.

    If an environment is found, read it in.  If not, return None.

    Arguments:
        args (Namespace): argparse namespace wtih command arguments

    Returns:
        (Environment): a found environment, or ``None``
    """
    # try arguments
    env = getattr(args, 'env', None)

    # treat env as a name
    if env:
        if exists(env):
            return read(env)

    else:
        # if env was specified, see if it is a dirctory otherwise, look
        # at env_dir (env and env_dir are mutually exclusive)
        env = getattr(args, 'env_dir', None)

        # if no argument, look for a manifest file
        if not env:
            if os.path.exists(manifest_name):
                env = os.getcwd()

            # if no env, env_dir, or manifest try the environment
            if not env:
                env = os.environ.get(spack_env_var)

                # nothing was set; there's no active environment
                if not env:
                    return None

    # if we get here, env isn't the name of a spack environment; it has
    # to be a path to an environment, or there is something wrong.
    if is_env_dir(env):
        return Environment(env)

    raise SpackEnvironmentError('no environment in %s' % env)


def get_env(args, cmd_name, required=False):
    """Used by commands to get the active environment.

    This first checks for an ``env`` argument, then looks at the
    ``active`` environment.  We check args first because Spack's
    subcommand arguments are parsed *after* the ``-e`` and ``-D``
    arguments to ``spack``.  So there may be an ``env`` argument that is
    *not* the active environment, and we give it precedence.

    This is used by a number of commands for determining whether there is
    an active environment.

    If an environment is not found *and* is required, print an error
    message that says the calling command *needs* an active environment.

    Arguments:
        args (Namespace): argparse namespace wtih command arguments
        cmd_name (str): name of calling command
        required (bool): if ``True``, raise an exception when no environment
            is found; if ``False``, just return ``None``

    Returns:
        (Environment): if there is an arg or active environment
    """
    # try argument first
    env = getattr(args, 'env', None)
    if env:
        if exists(env):
            return read(env)
        elif is_env_dir(env):
            return Environment(env)
        else:
            raise SpackEnvironmentError('no environment in %s' % env)

    # try the active environment. This is set by find_environment() (above)
    if _active_environment:
        return _active_environment
    elif not required:
        return None
    else:
        tty.die(
            '`spack %s` requires an environment' % cmd_name,
            'activate an environment first:',
            '    spack env activate ENV',
            'or use:',
            '    spack -e ENV %s ...' % cmd_name)


def _root(name):
    """Non-validating version of root(), to be used internally."""
    return os.path.join(env_path, name)


def root(name):
    """Get the root directory for an environment by name."""
    validate_env_name(name)
    return _root(name)


def exists(name):
    """Whether an environment with this name exists or not."""
    if not valid_env_name(name):
        return False
    return os.path.isdir(root(name))


def active(name):
    """True if the named environment is active."""
    return _active_environment and name == _active_environment.name


def is_env_dir(path):
    """Whether a directory contains a spack environment."""
    return os.path.isdir(path) and os.path.exists(
        os.path.join(path, manifest_name))


def read(name):
    """Get an environment with the supplied name."""
    validate_env_name(name)
    if not exists(name):
        raise SpackEnvironmentError("no such environment '%s'" % name)
    return Environment(root(name))


def create(name, init_file=None):
    """Create a named environment in Spack."""
    validate_env_name(name)
    if exists(name):
        raise SpackEnvironmentError("'%s': environment already exists" % name)
    return Environment(root(name), init_file)


def config_dict(yaml_data):
    """Get the configuration scope section out of an spack.yaml"""
    key = spack.config.first_existing(yaml_data, env_schema_keys)
    return yaml_data[key]


def all_environment_names():
    """List the names of environments that currently exist."""
    # just return empty if the env path does not exist.  A read-only
    # operation like list should not try to create a directory.
    if not os.path.exists(env_path):
        return []

    candidates = sorted(os.listdir(env_path))
    names = []
    for candidate in candidates:
        yaml_path = os.path.join(_root(candidate), manifest_name)
        if valid_env_name(candidate) and os.path.exists(yaml_path):
            names.append(candidate)
    return names


def all_environments():
    """Generator for all named Environments."""
    for name in all_environment_names():
        yield read(name)


def validate(data, filename=None):
    import jsonschema
    try:
        spack.schema.Validator(spack.schema.env.schema).validate(data)
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
    def internal(self):
        """Whether this environment is managed by Spack."""
        return self.path.startswith(env_path)

    @property
    def name(self):
        """Human-readable representation of the environment.

        This is the path for directory environments, and just the name
        for named environments.
        """
        if self.internal:
            return os.path.basename(self.path)
        else:
            return self.path

    @property
    def active(self):
        """True if this environment is currently active."""
        return _active_environment and self.path == _active_environment.path

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

    def env_file_config_scope_name(self):
        """Name of the config scope of this environment's manifest file."""
        return 'env:%s' % self.name

    def env_file_config_scope(self):
        """Get the configuration scope for the environment's manifest file."""
        config_name = self.env_file_config_scope_name()
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
            raise SpackEnvironmentError(
                'cannot add anonymous specs to an environment!')
        elif not spack.repo.path.exists(spec.name):
            raise SpackEnvironmentError('no such package: %s' % spec.name)

        existing = set(s for s in self.user_specs if s.name == spec.name)
        if not existing:
            self.user_specs.append(spec)
        return bool(not existing)

    def remove(self, query_spec, force=False):
        """Remove specs from an environment that match a query_spec"""
        query_spec = Spec(query_spec)

        # try abstract specs first
        matches = []
        if not query_spec.concrete:
            matches = [s for s in self.user_specs if s.satisfies(query_spec)]

        if not matches:
            # concrete specs match against concrete specs in the env
            specs_hashes = zip(
                self.concretized_user_specs, self.concretized_order)
            matches = [
                s for s, h in specs_hashes if query_spec.dag_hash() == h]

        if not matches:
            raise SpackEnvironmentError("Not found: {0}".format(query_spec))

        for spec in matches:
            if spec in self.user_specs:
                self.user_specs.remove(spec)

            if force and spec in self.concretized_user_specs:
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

    def install(self, user_spec, concrete_spec=None, **install_args):
        """Install a single spec into an environment.

        This will automatically concretize the single spec, but it won't
        affect other as-yet unconcretized specs.
        """
        spec = Spec(user_spec)

        if self.add(spec):
            concrete = concrete_spec if concrete_spec else spec.concretized()
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

            if not spec.external:
                # Link the resulting log file into logs dir
                build_log_link = os.path.join(
                    log_path, '%s-%s.log' % (spec.name, spec.dag_hash(7)))
                if os.path.exists(build_log_link):
                    os.remove(build_log_link)
                os.symlink(spec.package.build_log_path, build_log_link)

    def all_specs_by_hash(self):
        """Map of hashes to spec for all specs in this environment."""
        hashes = {}
        for h in self.concretized_order:
            specs = self.specs_by_hash[h].traverse(deptype=('link', 'run'))
            for spec in specs:
                hashes[spec.dag_hash()] = spec
        return hashes

    def all_specs(self):
        """Return all specs, even those a user spec would shadow."""
        return sorted(self.all_specs_by_hash().values())

    def all_hashes(self):
        """Return all specs, even those a user spec would shadow."""
        return list(self.all_specs_by_hash().keys())

    def roots(self):
        """Specs explicitly requested by the user *in this environment*.

        Yields both added and installed specs that have user specs in
        `spack.yaml`.
        """
        concretized = dict(self.concretized_specs())
        for spec in self.user_specs:
            concrete = concretized.get(spec)
            yield concrete if concrete else spec

    def added_specs(self):
        """Specs that are not yet installed.

        Yields the user spec for non-concretized specs, and the concrete
        spec for already concretized but not yet installed specs.
        """
        concretized = dict(self.concretized_specs())
        for spec in self.user_specs:
            concrete = concretized.get(spec)
            if not concrete:
                yield spec
            elif not concrete.package.installed:
                yield concrete

    def concretized_specs(self):
        """Tuples of (user spec, concrete spec) for all concrete specs."""
        for s, h in zip(self.concretized_user_specs, self.concretized_order):
            yield (s, self.specs_by_hash[h])

    def removed_specs(self):
        """Tuples of (user spec, concrete spec) for all specs that will be
           removed on nexg concretize."""
        needed = set()
        for s, c in self.concretized_specs():
            if s in self.user_specs:
                for d in c.traverse():
                    needed.add(d)

        for s, c in self.concretized_specs():
            for d in c.traverse():
                if d not in needed:
                    yield d

    def _get_environment_specs(self, recurse_dependencies=True):
        """Returns the specs of all the packages in an environment.

        If these specs appear under different user_specs, only one copy
        is added to the list returned.
        """
        package_to_spec = {}
        spec_list = list()

        for spec_hash in self.concretized_order:
            spec = self.specs_by_hash[spec_hash]

            specs = (spec.traverse(deptype=('link', 'run'))
                     if recurse_dependencies else (spec,))

            for dep in specs:
                prior = package_to_spec.get(dep.name)
                if prior and prior != dep:
                    tty.debug("{0} takes priority over {1}"
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
        self._previous_active = _active_environment
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


class SpackEnvironmentError(spack.error.SpackError):
    """Superclass for all errors to do with Spack environments."""
