# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import collections.abc
import contextlib
import copy
import os
import pathlib
import re
import shutil
import stat
import sys
import time
import urllib.parse
import urllib.request
import warnings
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union

import llnl.util.filesystem as fs
import llnl.util.tty as tty
import llnl.util.tty.color as clr
from llnl.util.lang import dedupe
from llnl.util.link_tree import ConflictingSpecsError
from llnl.util.symlink import symlink

import spack.compilers
import spack.concretize
import spack.config
import spack.error
import spack.fetch_strategy
import spack.hash_types as ht
import spack.hooks
import spack.main
import spack.paths
import spack.repo
import spack.schema.env
import spack.spec
import spack.stage
import spack.store
import spack.subprocess_context
import spack.user_environment as uenv
import spack.util.cpus
import spack.util.environment
import spack.util.hash
import spack.util.lock as lk
import spack.util.parallel
import spack.util.path
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.util.url
import spack.version
from spack import traverse
from spack.filesystem_view import SimpleFilesystemView, inverse_view_func_parser, view_func_parser
from spack.installer import PackageInstaller
from spack.schema.env import TOP_LEVEL_KEY
from spack.spec import Spec
from spack.spec_list import InvalidSpecConstraintError, SpecList
from spack.util.path import substitute_path_variables
from spack.variant import UnknownVariantError

#: environment variable used to indicate the active environment
spack_env_var = "SPACK_ENV"


#: currently activated environment
_active_environment: Optional["Environment"] = None


#: default path where environments are stored in the spack tree
default_env_path = os.path.join(spack.paths.var_path, "environments")


#: Name of the input yaml file for an environment
manifest_name = "spack.yaml"


#: Name of the input yaml file for an environment
lockfile_name = "spack.lock"


#: Name of the directory where environments store repos, logs, views
env_subdir_name = ".spack-env"


def env_root_path():
    """Override default root path if the user specified it"""
    return spack.util.path.canonicalize_path(
        spack.config.get("config:environments_root", default=default_env_path)
    )


def check_disallowed_env_config_mods(scopes):
    for scope in scopes:
        with spack.config.use_configuration(scope):
            if spack.config.get("config:environments_root"):
                raise SpackEnvironmentError(
                    "Spack environments are prohibited from modifying 'config:environments_root' "
                    "because it can make the definition of the environment ill-posed. Please "
                    "remove from your environment and place it in a permanent scope such as "
                    "defaults, system, site, etc."
                )
    return scopes


def default_manifest_yaml():
    """default spack.yaml file to put in new environments"""
    return """\
# This is a Spack Environment file.
#
# It describes a set of packages to be installed, along with
# configuration settings.
spack:
  # add package specs to the `specs` list
  specs: []
  view: true
  concretizer:
    unify: {}
""".format(
        "true" if spack.config.get("concretizer:unify") else "false"
    )


#: regex for validating enviroment names
valid_environment_name_re = r"^\w[\w-]*$"

#: version of the lockfile format. Must increase monotonically.
lockfile_format_version = 5


READER_CLS = {
    1: spack.spec.SpecfileV1,
    2: spack.spec.SpecfileV1,
    3: spack.spec.SpecfileV2,
    4: spack.spec.SpecfileV3,
    5: spack.spec.SpecfileV4,
}


# Magic names
# The name of the standalone spec list in the manifest yaml
user_speclist_name = "specs"
# The name of the default view (the view loaded on env.activate)
default_view_name = "default"
# Default behavior to link all packages into views (vs. only root packages)
default_view_link = "all"


def installed_specs():
    """
    Returns the specs of packages installed in the active environment or None
    if no packages are installed.
    """
    env = spack.environment.active_environment()
    hashes = env.all_hashes() if env else None
    return spack.store.STORE.db.query(hashes=hashes)


def valid_env_name(name):
    return re.match(valid_environment_name_re, name)


def validate_env_name(name):
    if not valid_env_name(name):
        raise ValueError(
            (
                "'%s': names must start with a letter, and only contain "
                "letters, numbers, _, and -."
            )
            % name
        )
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
    """
    global _active_environment

    # Fail early to avoid ending in an invalid state
    if not isinstance(env, Environment):
        raise TypeError("`env` should be of type {0}".format(Environment.__name__))

    # Check if we need to reinitialize the store due to pushing the configuration
    # below.
    install_tree_before = spack.config.get("config:install_tree")
    upstreams_before = spack.config.get("upstreams")
    prepare_config_scope(env)
    install_tree_after = spack.config.get("config:install_tree")
    upstreams_after = spack.config.get("upstreams")
    if install_tree_before != install_tree_after or upstreams_before != upstreams_after:
        # Hack to store the state of the store before activation
        env.store_token = spack.store.reinitialize()

    if use_env_repo:
        spack.repo.PATH.put_first(env.repo)

    tty.debug("Using environment '%s'" % env.name)

    # Do this last, because setting up the config must succeed first.
    _active_environment = env


def deactivate():
    """Undo any configuration or repo settings modified by ``activate()``."""
    global _active_environment

    if not _active_environment:
        return

    # If we attached a store token on activation, restore the previous state
    # and consume the token
    if hasattr(_active_environment, "store_token"):
        spack.store.restore(_active_environment.store_token)
        delattr(_active_environment, "store_token")
    deactivate_config_scope(_active_environment)

    # use _repo so we only remove if a repo was actually constructed
    if _active_environment._repo:
        spack.repo.PATH.remove(_active_environment._repo)

    tty.debug("Deactivated environment '%s'" % _active_environment.name)

    _active_environment = None


def active_environment() -> Optional["Environment"]:
    """Returns the active environment when there is any"""
    return _active_environment


def _root(name):
    """Non-validating version of root(), to be used internally."""
    return os.path.join(env_root_path(), name)


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
    return os.path.isdir(path) and os.path.exists(os.path.join(path, manifest_name))


def read(name):
    """Get an environment with the supplied name."""
    validate_env_name(name)
    if not exists(name):
        raise SpackEnvironmentError("no such environment '%s'" % name)
    return Environment(root(name))


def create(
    name: str,
    init_file: Optional[Union[str, pathlib.Path]] = None,
    with_view: Optional[Union[str, pathlib.Path, bool]] = None,
    keep_relative: bool = False,
) -> "Environment":
    """Create a managed environment in Spack and returns it.

    A managed environment is created in a root directory managed by this Spack instance, so that
    Spack can keep track of them.

    Files with suffix ``.json`` or ``.lock`` are considered lockfiles. Files with any other name
    are considered manifest files.

    Args:
        name: name of the managed environment
        init_file: either a lockfile, a manifest file, or None
        with_view: whether a view should be maintained for the environment. If the value is a
            string, it specifies the path to the view
        keep_relative: if True, develop paths are copied verbatim into the new environment file,
            otherwise they are made absolute
    """
    environment_dir = environment_dir_from_name(name, exists_ok=False)
    return create_in_dir(
        environment_dir, init_file=init_file, with_view=with_view, keep_relative=keep_relative
    )


def create_in_dir(
    manifest_dir: Union[str, pathlib.Path],
    init_file: Optional[Union[str, pathlib.Path]] = None,
    with_view: Optional[Union[str, pathlib.Path, bool]] = None,
    keep_relative: bool = False,
) -> "Environment":
    """Create an environment in the directory passed as input and returns it.

    Files with suffix ``.json`` or ``.lock`` are considered lockfiles. Files with any other name
    are considered manifest files.

    Args:
        manifest_dir: directory where to create the environment.
        init_file: either a lockfile, a manifest file, or None
        with_view: whether a view should be maintained for the environment. If the value is a
            string, it specifies the path to the view
        keep_relative: if True, develop paths are copied verbatim into the new environment file,
            otherwise they are made absolute
    """
    initialize_environment_dir(manifest_dir, envfile=init_file)

    if with_view is None and keep_relative:
        return Environment(manifest_dir)

    manifest = EnvironmentManifestFile(manifest_dir)

    if with_view is not None:
        manifest.set_default_view(with_view)

    if not keep_relative and init_file is not None and str(init_file).endswith(manifest_name):
        init_file = pathlib.Path(init_file)
        manifest.absolutify_dev_paths(init_file.parent)

    manifest.flush()

    return Environment(manifest_dir)


def environment_dir_from_name(name: str, exists_ok: bool = True) -> str:
    """Returns the directory associated with a named environment.

    Args:
        name: name of the environment
        exists_ok: if False, raise an error if the environment exists already

    Raises:
        SpackEnvironmentError: if exists_ok is False and the environment exists already
    """
    if not exists_ok and exists(name):
        raise SpackEnvironmentError(f"'{name}': environment already exists at {root(name)}")

    ensure_env_root_path_exists()
    validate_env_name(name)
    return root(name)


def ensure_env_root_path_exists():
    if not os.path.isdir(env_root_path()):
        fs.mkdirp(env_root_path())


def all_environment_names():
    """List the names of environments that currently exist."""
    # just return empty if the env path does not exist.  A read-only
    # operation like list should not try to create a directory.
    if not os.path.exists(env_root_path()):
        return []

    candidates = sorted(os.listdir(env_root_path()))
    names = []
    for candidate in candidates:
        yaml_path = os.path.join(_root(candidate), manifest_name)
        if valid_env_name(candidate) and os.path.exists(yaml_path):
            names.append(candidate)
    return names


def all_environments():
    """Generator for all managed Environments."""
    for name in all_environment_names():
        yield read(name)


def _read_yaml(str_or_file):
    """Read YAML from a file for round-trip parsing."""
    data = syaml.load_config(str_or_file)
    filename = getattr(str_or_file, "name", None)
    default_data = spack.config.validate(data, spack.schema.env.schema, filename)
    return data, default_data


def _write_yaml(data, str_or_file):
    """Write YAML to a file preserving comments and dict order."""
    filename = getattr(str_or_file, "name", None)
    spack.config.validate(data, spack.schema.env.schema, filename)
    syaml.dump_config(data, str_or_file, default_flow_style=False)


def _eval_conditional(string):
    """Evaluate conditional definitions using restricted variable scope."""
    valid_variables = spack.util.environment.get_host_environment()
    valid_variables.update({"re": re, "env": os.environ})
    return eval(string, valid_variables)


def _is_dev_spec_and_has_changed(spec):
    """Check if the passed spec is a dev build and whether it has changed since the
    last installation"""
    # First check if this is a dev build and in the process already try to get
    # the dev_path
    dev_path_var = spec.variants.get("dev_path", None)
    if not dev_path_var:
        return False

    # Now we can check whether the code changed since the last installation
    if not spec.installed:
        # Not installed -> nothing to compare against
        return False

    _, record = spack.store.STORE.db.query_by_spec_hash(spec.dag_hash())
    mtime = fs.last_modification_time_recursive(dev_path_var.value)
    return mtime > record.installation_time


def _error_on_nonempty_view_dir(new_root):
    """Defensively error when the target view path already exists and is not an
    empty directory. This usually happens when the view symlink was removed, but
    not the directory it points to. In those cases, it's better to just error when
    the new view dir is non-empty, since it indicates the user removed part but not
    all of the view, and it likely in an inconsistent state."""
    # Check if the target path lexists
    try:
        st = os.lstat(new_root)
    except (IOError, OSError):
        return

    # Empty directories are fine
    if stat.S_ISDIR(st.st_mode) and len(os.listdir(new_root)) == 0:
        return

    # Anything else is an error
    raise SpackEnvironmentViewError(
        "Failed to generate environment view, because the target {} already "
        "exists or is not empty. To update the view, remove this path, and run "
        "`spack env view regenerate`".format(new_root)
    )


class ViewDescriptor:
    def __init__(
        self,
        base_path,
        root,
        projections={},
        select=[],
        exclude=[],
        link=default_view_link,
        link_type="symlink",
    ):
        self.base = base_path
        self.raw_root = root
        self.root = spack.util.path.canonicalize_path(root, default_wd=base_path)
        self.projections = projections
        self.select = select
        self.exclude = exclude
        self.link_type = view_func_parser(link_type)
        self.link = link

    def select_fn(self, spec):
        return any(spec.satisfies(s) for s in self.select)

    def exclude_fn(self, spec):
        return not any(spec.satisfies(e) for e in self.exclude)

    def update_root(self, new_path):
        self.raw_root = new_path
        self.root = spack.util.path.canonicalize_path(new_path, default_wd=self.base)

    def __eq__(self, other):
        return all(
            [
                self.root == other.root,
                self.projections == other.projections,
                self.select == other.select,
                self.exclude == other.exclude,
                self.link == other.link,
                self.link_type == other.link_type,
            ]
        )

    def to_dict(self):
        ret = syaml.syaml_dict([("root", self.raw_root)])
        if self.projections:
            ret["projections"] = self.projections
        if self.select:
            ret["select"] = self.select
        if self.exclude:
            ret["exclude"] = self.exclude
        if self.link_type:
            ret["link_type"] = inverse_view_func_parser(self.link_type)
        if self.link != default_view_link:
            ret["link"] = self.link
        return ret

    @staticmethod
    def from_dict(base_path, d):
        return ViewDescriptor(
            base_path,
            d["root"],
            d.get("projections", {}),
            d.get("select", []),
            d.get("exclude", []),
            d.get("link", default_view_link),
            d.get("link_type", "symlink"),
        )

    @property
    def _current_root(self):
        if not os.path.islink(self.root):
            return None

        root = os.readlink(self.root)
        if os.path.isabs(root):
            return root

        root_dir = os.path.dirname(self.root)
        return os.path.join(root_dir, root)

    def _next_root(self, specs):
        content_hash = self.content_hash(specs)
        root_dir = os.path.dirname(self.root)
        root_name = os.path.basename(self.root)
        return os.path.join(root_dir, "._%s" % root_name, content_hash)

    def content_hash(self, specs):
        d = syaml.syaml_dict(
            [
                ("descriptor", self.to_dict()),
                ("specs", [(spec.dag_hash(), spec.prefix) for spec in sorted(specs)]),
            ]
        )
        contents = sjson.dump(d)
        return spack.util.hash.b32_hash(contents)

    def get_projection_for_spec(self, spec):
        """Get projection for spec relative to view root

        Getting the projection from the underlying root will get the temporary
        projection. This gives the permanent projection relative to the root
        symlink.
        """
        view = self.view()
        view_path = view.get_projection_for_spec(spec)
        rel_path = os.path.relpath(view_path, self._current_root)
        return os.path.join(self.root, rel_path)

    def view(self, new=None):
        """
        Generate the FilesystemView object for this ViewDescriptor

        By default, this method returns a FilesystemView object rooted at the
        current underlying root of this ViewDescriptor (self._current_root)

        Raise if new is None and there is no current view

        Arguments:
            new (str or None): If a string, create a FilesystemView
                rooted at that path. Default None. This should only be used to
                regenerate the view, and cannot be used to access specs.
        """
        root = new if new else self._current_root
        if not root:
            # This can only be hit if we write a future bug
            msg = (
                "Attempting to get nonexistent view from environment. "
                "View root is at %s" % self.root
            )
            raise SpackEnvironmentViewError(msg)
        return SimpleFilesystemView(
            root,
            spack.store.STORE.layout,
            ignore_conflicts=True,
            projections=self.projections,
            link=self.link_type,
        )

    def __contains__(self, spec):
        """Is the spec described by the view descriptor

        Note: This does not claim the spec is already linked in the view.
        It merely checks that the spec is selected if a select operation is
        specified and is not excluded if an exclude operator is specified.
        """
        if self.select:
            if not self.select_fn(spec):
                return False

        if self.exclude:
            if not self.exclude_fn(spec):
                return False

        return True

    def specs_for_view(self, concretized_root_specs):
        """
        From the list of concretized user specs in the environment, flatten
        the dags, and filter selected, installed specs, remove duplicates on dag hash.
        """
        # With deps, requires traversal
        if self.link == "all" or self.link == "run":
            deptype = ("run") if self.link == "run" else ("link", "run")
            specs = list(
                traverse.traverse_nodes(
                    concretized_root_specs, deptype=deptype, key=traverse.by_dag_hash
                )
            )
        else:
            specs = list(dedupe(concretized_root_specs, key=traverse.by_dag_hash))

        # Filter selected, installed specs
        with spack.store.STORE.db.read_transaction():
            specs = [s for s in specs if s in self and s.installed]

        return specs

    def regenerate(self, concretized_root_specs):
        specs = self.specs_for_view(concretized_root_specs)

        # To ensure there are no conflicts with packages being installed
        # that cannot be resolved or have repos that have been removed
        # we always regenerate the view from scratch.
        # We will do this by hashing the view contents and putting the view
        # in a directory by hash, and then having a symlink to the real
        # view in the root. The real root for a view at /dirname/basename
        # will be /dirname/._basename_<hash>.
        # This allows for atomic swaps when we update the view

        # cache the roots because the way we determine which is which does
        # not work while we are updating
        new_root = self._next_root(specs)
        old_root = self._current_root

        if new_root == old_root:
            tty.debug("View at %s does not need regeneration." % self.root)
            return

        _error_on_nonempty_view_dir(new_root)

        # construct view at new_root
        if specs:
            tty.msg("Updating view at {0}".format(self.root))

        view = self.view(new=new_root)

        root_dirname = os.path.dirname(self.root)
        tmp_symlink_name = os.path.join(root_dirname, "._view_link")

        # Create a new view
        try:
            fs.mkdirp(new_root)
            view.add_specs(*specs, with_dependencies=False)

            # create symlink from tmp_symlink_name to new_root
            if os.path.exists(tmp_symlink_name):
                os.unlink(tmp_symlink_name)
            symlink(new_root, tmp_symlink_name)

            # mv symlink atomically over root symlink to old_root
            fs.rename(tmp_symlink_name, self.root)
        except Exception as e:
            # Clean up new view and temporary symlink on any failure.
            try:
                shutil.rmtree(new_root, ignore_errors=True)
                os.unlink(tmp_symlink_name)
            except (IOError, OSError):
                pass

            # Give an informative error message for the typical error case: two specs, same package
            # project to same prefix.
            if isinstance(e, ConflictingSpecsError):
                spec_a = e.args[0].format(color=clr.get_color_when())
                spec_b = e.args[1].format(color=clr.get_color_when())
                raise SpackEnvironmentViewError(
                    f"The environment view in {self.root} could not be created, "
                    "because the following two specs project to the same prefix:\n"
                    f"    {spec_a}, and\n"
                    f"    {spec_b}.\n"
                    "    To resolve this issue:\n"
                    "        a. use `concretization:unify:true` to ensure there is only one "
                    "package per spec in the environment, or\n"
                    "        b. disable views with `view:false`, or\n"
                    "        c. create custom view projections."
                ) from e
            raise

        # Remove the old root when it's in the same folder as the new root. This guards
        # against removal of an arbitrary path when the original symlink in self.root
        # was not created by the environment, but by the user.
        if (
            old_root
            and os.path.exists(old_root)
            and os.path.samefile(os.path.dirname(new_root), os.path.dirname(old_root))
        ):
            try:
                shutil.rmtree(old_root)
            except (IOError, OSError) as e:
                msg = "Failed to remove old view at %s\n" % old_root
                msg += str(e)
                tty.warn(msg)


def _create_environment(path):
    return Environment(path)


class Environment:
    """A Spack environment, which bundles together configuration and a list of specs."""

    def __init__(self, manifest_dir: Union[str, pathlib.Path]) -> None:
        """An environment can be constructed from a directory containing a "spack.yaml" file, and
        optionally a consistent "spack.lock" file.

        Args:
            manifest_dir: directory with the "spack.yaml" associated with the environment
        """
        self.path = os.path.abspath(str(manifest_dir))

        self.txlock = lk.Lock(self._transaction_lock_path)

        self._unify = None
        self.new_specs: List[Spec] = []
        self.new_installs: List[Spec] = []
        self.views: Dict[str, ViewDescriptor] = {}

        #: Specs from "spack.yaml"
        self.spec_lists: Dict[str, SpecList] = {user_speclist_name: SpecList()}
        #: Dev-build specs from "spack.yaml"
        self.dev_specs: Dict[str, Any] = {}
        #: User specs from the last concretization
        self.concretized_user_specs: List[Spec] = []
        #: Roots associated with the last concretization, in order
        self.concretized_order: List[Spec] = []
        #: Concretized specs by hash
        self.specs_by_hash: Dict[str, Spec] = {}
        #: Repository for this environment (memoized)
        self._repo = None
        #: Previously active environment
        self._previous_active = None

        with lk.ReadTransaction(self.txlock):
            self.manifest = EnvironmentManifestFile(manifest_dir)
            self._read()

    @property
    def unify(self):
        if self._unify is None:
            self._unify = spack.config.get("concretizer:unify", False)
        return self._unify

    @unify.setter
    def unify(self, value):
        self._unify = value

    def __reduce__(self):
        return _create_environment, (self.path,)

    def _re_read(self):
        """Reinitialize the environment object."""
        self.clear(re_read=True)
        self.manifest = EnvironmentManifestFile(self.path)
        self._read()

    def _read(self):
        self._construct_state_from_manifest()

        if os.path.exists(self.lock_path):
            with open(self.lock_path) as f:
                read_lock_version = self._read_lockfile(f)

            if read_lock_version == 1:
                tty.debug(f"Storing backup of {self.lock_path} at {self._lock_backup_v1_path}")
                shutil.copy(self.lock_path, self._lock_backup_v1_path)

    def write_transaction(self):
        """Get a write lock context manager for use in a `with` block."""
        return lk.WriteTransaction(self.txlock, acquire=self._re_read)

    def _construct_state_from_manifest(self):
        """Read manifest file and set up user specs."""
        self.spec_lists = collections.OrderedDict()
        env_configuration = self.manifest[TOP_LEVEL_KEY]
        for item in env_configuration.get("definitions", []):
            entry = copy.deepcopy(item)
            when = _eval_conditional(entry.pop("when", "True"))
            assert len(entry) == 1
            if when:
                name, spec_list = next(iter(entry.items()))
                user_specs = SpecList(name, spec_list, self.spec_lists.copy())
                if name in self.spec_lists:
                    self.spec_lists[name].extend(user_specs)
                else:
                    self.spec_lists[name] = user_specs

        spec_list = env_configuration.get(user_speclist_name, [])
        user_specs = SpecList(
            user_speclist_name, [s for s in spec_list if s], self.spec_lists.copy()
        )
        self.spec_lists[user_speclist_name] = user_specs

        enable_view = env_configuration.get("view")
        # enable_view can be boolean, string, or None
        if enable_view is True or enable_view is None:
            self.views = {default_view_name: ViewDescriptor(self.path, self.view_path_default)}
        elif isinstance(enable_view, str):
            self.views = {default_view_name: ViewDescriptor(self.path, enable_view)}
        elif enable_view:
            path = self.path
            self.views = dict(
                (name, ViewDescriptor.from_dict(path, values))
                for name, values in enable_view.items()
            )
        else:
            self.views = {}

        # Retrieve dev-build packages:
        self.dev_specs = copy.deepcopy(env_configuration.get("develop", {}))
        for name, entry in self.dev_specs.items():
            # spec must include a concrete version
            assert Spec(entry["spec"]).versions.concrete_range_as_version
            # default path is the spec name
            if "path" not in entry:
                self.dev_specs[name]["path"] = name

    @property
    def user_specs(self):
        return self.spec_lists[user_speclist_name]

    def clear(self, re_read=False):
        """Clear the contents of the environment

        Arguments:
            re_read (bool): If True, do not clear ``new_specs`` nor
                ``new_installs`` values. These values cannot be read from
                yaml, and need to be maintained when re-reading an existing
                environment.
        """
        self.spec_lists = {user_speclist_name: SpecList()}  # specs from yaml
        self.dev_specs = {}  # dev-build specs from yaml
        self.concretized_user_specs = []  # user specs from last concretize
        self.concretized_order = []  # roots of last concretize, in order
        self.specs_by_hash = {}  # concretized specs by hash
        self.invalidate_repository_cache()
        self._previous_active = None  # previously active environment
        if not re_read:
            # things that cannot be recreated from file
            self.new_specs = []  # write packages for these on write()
            self.new_installs = []  # write modules for these on write()

    @property
    def internal(self):
        """Whether this environment is managed by Spack."""
        return self.path.startswith(env_root_path())

    @property
    def name(self):
        """Human-readable representation of the environment.

        This is the path for directory environments, and just the name
        for managed environments.
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
    def _transaction_lock_path(self):
        """The location of the lock file used to synchronize multiple
        processes updating the same environment.
        """
        return os.path.join(self.env_subdir_path, "transaction_lock")

    @property
    def lock_path(self):
        """Path to spack.lock file in this environment."""
        return os.path.join(self.path, lockfile_name)

    @property
    def _lock_backup_v1_path(self):
        """Path to backup of v1 lockfile before conversion to v2"""
        return self.lock_path + ".backup.v1"

    @property
    def env_subdir_path(self):
        """Path to directory where the env stores repos, logs, views."""
        return os.path.join(self.path, env_subdir_name)

    @property
    def repos_path(self):
        return os.path.join(self.path, env_subdir_name, "repos")

    @property
    def log_path(self):
        return os.path.join(self.path, env_subdir_name, "logs")

    @property
    def config_stage_dir(self):
        """Directory for any staged configuration file(s)."""
        return os.path.join(self.env_subdir_path, "config")

    @property
    def view_path_default(self):
        # default path for environment views
        return os.path.join(self.env_subdir_path, "view")

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
        includes = self.manifest[TOP_LEVEL_KEY].get("include", [])
        missing = []
        for i, config_path in enumerate(reversed(includes)):
            # allow paths to contain spack config/environment variables, etc.
            config_path = substitute_path_variables(config_path)

            include_url = urllib.parse.urlparse(config_path)

            # Transform file:// URLs to direct includes.
            if include_url.scheme == "file":
                config_path = urllib.request.url2pathname(include_url.path)

            # Any other URL should be fetched.
            elif include_url.scheme in ("http", "https", "ftp"):
                # Stage any remote configuration file(s)
                staged_configs = (
                    os.listdir(self.config_stage_dir)
                    if os.path.exists(self.config_stage_dir)
                    else []
                )
                remote_path = urllib.request.url2pathname(include_url.path)
                basename = os.path.basename(remote_path)
                if basename in staged_configs:
                    # Do NOT re-stage configuration files over existing
                    # ones with the same name since there is a risk of
                    # losing changes (e.g., from 'spack config update').
                    tty.warn(
                        "Will not re-stage configuration from {0} to avoid "
                        "losing changes to the already staged file of the "
                        "same name.".format(remote_path)
                    )

                    # Recognize the configuration stage directory
                    # is flattened to ensure a single copy of each
                    # configuration file.
                    config_path = self.config_stage_dir
                    if basename.endswith(".yaml"):
                        config_path = os.path.join(config_path, basename)
                else:
                    staged_path = spack.config.fetch_remote_configs(
                        config_path, self.config_stage_dir, skip_existing=True
                    )
                    if not staged_path:
                        raise SpackEnvironmentError(
                            "Unable to fetch remote configuration {0}".format(config_path)
                        )
                    config_path = staged_path

            elif include_url.scheme:
                raise ValueError(
                    "Unsupported URL scheme for environment include: {}".format(config_path)
                )

            # treat relative paths as relative to the environment
            if not os.path.isabs(config_path):
                config_path = os.path.join(self.path, config_path)
                config_path = os.path.normpath(os.path.realpath(config_path))

            if os.path.isdir(config_path):
                # directories are treated as regular ConfigScopes
                config_name = "env:%s:%s" % (self.name, os.path.basename(config_path))
                tty.debug("Creating ConfigScope {0} for '{1}'".format(config_name, config_path))
                scope = spack.config.ConfigScope(config_name, config_path)
            elif os.path.exists(config_path):
                # files are assumed to be SingleFileScopes
                config_name = "env:%s:%s" % (self.name, config_path)
                tty.debug(
                    "Creating SingleFileScope {0} for '{1}'".format(config_name, config_path)
                )
                scope = spack.config.SingleFileScope(
                    config_name, config_path, spack.schema.merged.schema
                )
            else:
                missing.append(config_path)
                continue

            scopes.append(scope)

        if missing:
            msg = "Detected {0} missing include path(s):".format(len(missing))
            msg += "\n   {0}".format("\n   ".join(missing))
            raise spack.config.ConfigFileError(msg)

        return scopes

    def env_file_config_scope_name(self):
        """Name of the config scope of this environment's manifest file."""
        return "env:%s" % self.name

    def env_file_config_scope(self):
        """Get the configuration scope for the environment's manifest file."""
        config_name = self.env_file_config_scope_name()
        return spack.config.SingleFileScope(
            config_name, self.manifest_path, spack.schema.env.schema, [TOP_LEVEL_KEY]
        )

    def config_scopes(self):
        """A list of all configuration scopes for this environment."""
        return check_disallowed_env_config_mods(
            self.included_config_scopes() + [self.env_file_config_scope()]
        )

    def destroy(self):
        """Remove this environment from Spack entirely."""
        shutil.rmtree(self.path)

    def update_stale_references(self, from_list=None):
        """Iterate over spec lists updating references."""
        if not from_list:
            from_list = next(iter(self.spec_lists.keys()))
        index = list(self.spec_lists.keys()).index(from_list)

        # spec_lists is an OrderedDict, all list entries after the modified
        # list may refer to the modified list. Update stale references
        for i, (name, speclist) in enumerate(
            list(self.spec_lists.items())[index + 1 :], index + 1
        ):
            new_reference = dict((n, self.spec_lists[n]) for n in list(self.spec_lists.keys())[:i])
            speclist.update_reference(new_reference)

    def add(self, user_spec, list_name=user_speclist_name):
        """Add a single user_spec (non-concretized) to the Environment

        Returns:
            (bool): True if the spec was added, False if it was already
                present and did not need to be added

        """
        spec = Spec(user_spec)

        if list_name not in self.spec_lists:
            raise SpackEnvironmentError(f"No list {list_name} exists in environment {self.name}")

        if list_name == user_speclist_name:
            if spec.anonymous:
                raise SpackEnvironmentError("cannot add anonymous specs to an environment")
            elif not spack.repo.PATH.exists(spec.name) and not spec.abstract_hash:
                virtuals = spack.repo.PATH.provider_index.providers.keys()
                if spec.name not in virtuals:
                    msg = "no such package: %s" % spec.name
                    raise SpackEnvironmentError(msg)

        list_to_change = self.spec_lists[list_name]
        existing = str(spec) in list_to_change.yaml_list
        if not existing:
            list_to_change.add(str(spec))
            self.update_stale_references(list_name)
            if list_name == user_speclist_name:
                self.manifest.add_user_spec(str(user_spec))
            else:
                self.manifest.add_definition(str(user_spec), list_name=list_name)

        return bool(not existing)

    def change_existing_spec(
        self,
        change_spec: Spec,
        list_name: str = user_speclist_name,
        match_spec: Optional[Spec] = None,
        allow_changing_multiple_specs=False,
    ):
        """
        Find the spec identified by `match_spec` and change it to `change_spec`.

        Arguments:
            change_spec: defines the spec properties that
                need to be changed. This will not change attributes of the
                matched spec unless they conflict with `change_spec`.
            list_name: identifies the spec list in the environment that
                should be modified
            match_spec: if set, this identifies the spec
                that should be changed. If not set, it is assumed we are
                looking for a spec with the same name as `change_spec`.
        """
        if not (change_spec.name or (match_spec and match_spec.name)):
            raise ValueError(
                "Must specify a spec name to identify a single spec"
                " in the environment that will be changed"
            )
        match_spec = match_spec or Spec(change_spec.name)

        list_to_change = self.spec_lists[list_name]
        if list_to_change.is_matrix:
            raise SpackEnvironmentError(
                "Cannot directly change specs in matrices:"
                " specify a named list that is not a matrix"
            )

        matches = list((idx, x) for idx, x in enumerate(list_to_change) if x.satisfies(match_spec))
        if len(matches) == 0:
            raise ValueError(
                "There are no specs named {0} in {1}".format(match_spec.name, list_name)
            )
        elif len(matches) > 1 and not allow_changing_multiple_specs:
            raise ValueError("{0} matches multiple specs".format(str(match_spec)))

        for idx, spec in matches:
            override_spec = Spec.override(spec, change_spec)
            self.spec_lists[list_name].specs[idx] = override_spec
            if list_name == user_speclist_name:
                self.manifest.override_user_spec(str(override_spec), idx=idx)
            else:
                self.manifest.override_definition(
                    str(spec), override=str(override_spec), list_name=list_name
                )
        self.update_stale_references(from_list=list_name)
        self._construct_state_from_manifest()

    def remove(self, query_spec, list_name=user_speclist_name, force=False):
        """Remove specs from an environment that match a query_spec"""
        err_msg_header = (
            f"cannot remove {query_spec} from '{list_name}' definition "
            f"in {self.manifest.manifest_file}"
        )
        query_spec = Spec(query_spec)
        try:
            list_to_change = self.spec_lists[list_name]
        except KeyError as e:
            msg = f"{err_msg_header}, since '{list_name}' does not exist"
            raise SpackEnvironmentError(msg) from e

        if not query_spec.concrete:
            matches = [s for s in list_to_change if s.satisfies(query_spec)]

        else:
            # concrete specs match against concrete specs in the env
            # by dag hash.
            specs_hashes = zip(self.concretized_user_specs, self.concretized_order)
            matches = [s for s, h in specs_hashes if query_spec.dag_hash() == h]

        if not matches:
            raise SpackEnvironmentError(f"{err_msg_header}, no spec matches")

        old_specs = set(self.user_specs)
        new_specs = set()
        for spec in matches:
            if spec not in list_to_change:
                continue
            try:
                list_to_change.remove(spec)
                self.update_stale_references(list_name)
                new_specs = set(self.user_specs)
            except spack.spec_list.SpecListError:
                # define new specs list
                new_specs = set(self.user_specs)
                msg = f"Spec '{spec}' is part of a spec matrix and "
                msg += f"cannot be removed from list '{list_to_change}'."
                if force:
                    msg += " It will be removed from the concrete specs."
                    # Mock new specs, so we can remove this spec from concrete spec lists
                    new_specs.remove(spec)
                tty.warn(msg)
            else:
                if list_name == user_speclist_name:
                    self.manifest.remove_user_spec(str(spec))
                else:
                    self.manifest.remove_definition(str(spec), list_name=list_name)

        # If force, update stale concretized specs
        for spec in old_specs - new_specs:
            if force and spec in self.concretized_user_specs:
                i = self.concretized_user_specs.index(spec)
                del self.concretized_user_specs[i]

                dag_hash = self.concretized_order[i]
                del self.concretized_order[i]
                del self.specs_by_hash[dag_hash]

    def develop(self, spec: Spec, path: str, clone: bool = False) -> bool:
        """Add dev-build info for package

        Args:
            spec: Set constraints on development specs. Must include a
                concrete version.
            path: Path to find code for developer builds. Relative
                paths will be resolved relative to the environment.
            clone: Clone the package code to the path.
                If clone is False Spack will assume the code is already present
                at ``path``.

        Return:
            (bool): True iff the environment was changed.
        """
        spec = spec.copy()  # defensive copy since we access cached attributes

        if not spec.versions.concrete:
            raise SpackEnvironmentError("Cannot develop spec %s without a concrete version" % spec)

        for name, entry in self.dev_specs.items():
            if name == spec.name:
                e_spec = Spec(entry["spec"])
                e_path = entry["path"]

                if e_spec == spec:
                    if path == e_path:
                        tty.msg("Spec %s already configured for development" % spec)
                        return False
                    else:
                        tty.msg("Updating development path for spec %s" % spec)
                        break
                else:
                    msg = "Updating development spec for package "
                    msg += "%s with path %s" % (spec.name, path)
                    tty.msg(msg)
                    break
        else:
            tty.msg("Configuring spec %s for development at path %s" % (spec, path))

        if clone:
            # "steal" the source code via staging API. We ask for a stage
            # to be created, then copy it afterwards somewhere else. It would be
            # better if we can create the `source_path` directly into its final
            # destination.
            abspath = spack.util.path.canonicalize_path(path, default_wd=self.path)
            pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
            # We construct a package class ourselves, rather than asking for
            # Spec.package, since Spec only allows this when it is concrete
            package = pkg_cls(spec)
            if isinstance(package.fetcher, spack.fetch_strategy.GitFetchStrategy):
                package.fetcher.get_full_repo = True
                # If we retrieved this version before and cached it, we may have
                # done so without cloning the full git repo; likewise, any
                # mirror might store an instance with truncated history.
                package.stage.disable_mirrors()

            package.stage.steal_source(abspath)

        # If it wasn't already in the list, append it
        entry = {"path": path, "spec": str(spec)}
        self.dev_specs[spec.name] = entry
        self.manifest.add_develop_spec(spec.name, entry=entry.copy())
        return True

    def undevelop(self, spec):
        """Remove develop info for abstract spec ``spec``.

        returns True on success, False if no entry existed."""
        spec = Spec(spec)  # In case it's a spec object
        if spec.name in self.dev_specs:
            del self.dev_specs[spec.name]
            self.manifest.remove_develop_spec(spec.name)
            return True
        return False

    def is_develop(self, spec):
        """Returns true when the spec is built from local sources"""
        return spec.name in self.dev_specs

    def concretize(self, force=False, tests=False):
        """Concretize user_specs in this environment.

        Only concretizes specs that haven't been concretized yet unless
        force is ``True``.

        This only modifies the environment in memory. ``write()`` will
        write out a lockfile containing concretized specs.

        Arguments:
            force (bool): re-concretize ALL specs, even those that were
               already concretized
            tests (bool or list or set): False to run no tests, True to test
                all packages, or a list of package names to run tests for some

        Returns:
            List of specs that have been concretized. Each entry is a tuple of
            the user spec and the corresponding concretized spec.
        """
        if force:
            # Clear previously concretized specs
            self.concretized_user_specs = []
            self.concretized_order = []
            self.specs_by_hash = {}

        # Remove concrete specs that no longer correlate to a user spec
        for spec in set(self.concretized_user_specs) - set(self.user_specs):
            self.deconcretize(spec)

        # Pick the right concretization strategy
        if self.unify == "when_possible":
            return self._concretize_together_where_possible(tests=tests)

        if self.unify is True:
            return self._concretize_together(tests=tests)

        if self.unify is False:
            return self._concretize_separately(tests=tests)

        msg = "concretization strategy not implemented [{0}]"
        raise SpackEnvironmentError(msg.format(self.unify))

    def deconcretize(self, spec):
        # spec has to be a root of the environment
        index = self.concretized_user_specs.index(spec)
        dag_hash = self.concretized_order.pop(index)
        del self.concretized_user_specs[index]

        # If this was the only user spec that concretized to this concrete spec, remove it
        if dag_hash not in self.concretized_order:
            del self.specs_by_hash[dag_hash]

    def _get_specs_to_concretize(
        self,
    ) -> Tuple[Set[spack.spec.Spec], Set[spack.spec.Spec], List[spack.spec.Spec]]:
        """Compute specs to concretize for unify:true and unify:when_possible.

        This includes new user specs and any already concretized specs.

        Returns:
            Tuple of new user specs, user specs to keep, and the specs to concretize.

        """
        # Exit early if the set of concretized specs is the set of user specs
        new_user_specs = set(self.user_specs) - set(self.concretized_user_specs)
        kept_user_specs = set(self.user_specs) & set(self.concretized_user_specs)
        if not new_user_specs:
            return new_user_specs, kept_user_specs, []

        concrete_specs_to_keep = [
            concrete
            for abstract, concrete in self.concretized_specs()
            if abstract in kept_user_specs
        ]

        specs_to_concretize = list(new_user_specs) + concrete_specs_to_keep
        return new_user_specs, kept_user_specs, specs_to_concretize

    def _concretize_together_where_possible(
        self, tests: bool = False
    ) -> List[Tuple[spack.spec.Spec, spack.spec.Spec]]:
        # Avoid cyclic dependency
        import spack.solver.asp

        # Exit early if the set of concretized specs is the set of user specs
        new_user_specs, _, specs_to_concretize = self._get_specs_to_concretize()
        if not new_user_specs:
            return []

        old_concrete_to_abstract = {
            concrete: abstract for (abstract, concrete) in self.concretized_specs()
        }

        self.concretized_user_specs = []
        self.concretized_order = []
        self.specs_by_hash = {}

        result_by_user_spec = {}
        solver = spack.solver.asp.Solver(configuration=spack.config.CONFIG)
        for result in solver.solve_in_rounds(specs_to_concretize, tests=tests):
            result_by_user_spec.update(result.specs_by_input)

        result = []
        for abstract, concrete in sorted(result_by_user_spec.items()):
            # If the "abstract" spec is a concrete spec from the previous concretization
            # translate it back to an abstract spec. Otherwise, keep the abstract spec
            abstract = old_concrete_to_abstract.get(abstract, abstract)
            if abstract in new_user_specs:
                result.append((abstract, concrete))
            self._add_concrete_spec(abstract, concrete)

        return result

    def _concretize_together(
        self, tests: bool = False
    ) -> List[Tuple[spack.spec.Spec, spack.spec.Spec]]:
        """Concretization strategy that concretizes all the specs
        in the same DAG.
        """
        # Exit early if the set of concretized specs is the set of user specs
        new_user_specs, kept_user_specs, specs_to_concretize = self._get_specs_to_concretize()
        if not new_user_specs:
            return []

        self.concretized_user_specs = []
        self.concretized_order = []
        self.specs_by_hash = {}

        try:
            concrete_specs: List[spack.spec.Spec] = spack.concretize.concretize_specs_together(
                *specs_to_concretize, tests=tests
            )
        except spack.error.UnsatisfiableSpecError as e:
            # "Enhance" the error message for multiple root specs, suggest a less strict
            # form of concretization.
            if len(self.user_specs) > 1:
                e.message += ". "
                if kept_user_specs:
                    e.message += (
                        "Couldn't concretize without changing the existing environment. "
                        "If you are ok with changing it, try `spack concretize --force`. "
                    )
                e.message += (
                    "You could consider setting `concretizer:unify` to `when_possible` "
                    "or `false` to allow multiple versions of some packages."
                )
            raise

        # set() | set() does not preserve ordering, even though sets are ordered
        ordered_user_specs = list(new_user_specs) + list(kept_user_specs)
        concretized_specs = [x for x in zip(ordered_user_specs, concrete_specs)]
        for abstract, concrete in concretized_specs:
            self._add_concrete_spec(abstract, concrete)

        # zip truncates the longer list, which is exactly what we want here
        return list(zip(new_user_specs, concrete_specs))

    def _concretize_separately(self, tests=False):
        """Concretization strategy that concretizes separately one
        user spec after the other.
        """
        import spack.bootstrap

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

        # Concretize any new user specs that we haven't concretized yet
        arguments, root_specs = [], []
        for uspec, uspec_constraints in zip(self.user_specs, self.user_specs.specs_as_constraints):
            if uspec not in old_concretized_user_specs:
                root_specs.append(uspec)
                arguments.append((uspec_constraints, tests))

        # Ensure we don't try to bootstrap clingo in parallel
        if spack.config.get("config:concretizer", "clingo") == "clingo":
            with spack.bootstrap.ensure_bootstrap_configuration():
                spack.bootstrap.ensure_core_dependencies()

        # Ensure all the indexes have been built or updated, since
        # otherwise the processes in the pool may timeout on waiting
        # for a write lock. We do this indirectly by retrieving the
        # provider index, which should in turn trigger the update of
        # all the indexes if there's any need for that.
        _ = spack.repo.PATH.provider_index

        # Ensure we have compilers in compilers.yaml to avoid that
        # processes try to write the config file in parallel
        _ = spack.compilers.get_compiler_config()

        # Early return if there is nothing to do
        if len(arguments) == 0:
            return []

        # Solve the environment in parallel on Linux
        start = time.time()
        max_processes = min(
            len(arguments),  # Number of specs
            spack.config.get("config:build_jobs"),  # Cap on build jobs
        )

        # TODO: revisit this print as soon as darwin is parallel too
        msg = "Starting concretization"
        if sys.platform != "darwin":
            pool_size = spack.util.parallel.num_processes(max_processes=max_processes)
            if pool_size > 1:
                msg = msg + " pool with {0} processes".format(pool_size)
        tty.msg(msg)

        concretized_root_specs = spack.util.parallel.parallel_map(
            _concretize_task, arguments, max_processes=max_processes, debug=tty.is_debug()
        )

        finish = time.time()
        tty.msg("Environment concretized in %.2f seconds." % (finish - start))
        by_hash = {}
        for abstract, concrete in zip(root_specs, concretized_root_specs):
            self._add_concrete_spec(abstract, concrete)
            by_hash[concrete.dag_hash()] = concrete

        # Unify the specs objects, so we get correct references to all parents
        self._read_lockfile_dict(self._to_lockfile_dict())

        # Re-attach information on test dependencies
        if tests:
            # This is slow, but the information on test dependency is lost
            # after unification or when reading from a lockfile.
            for h in self.specs_by_hash:
                current_spec, computed_spec = self.specs_by_hash[h], by_hash[h]
                for node in computed_spec.traverse():
                    test_edges = node.edges_to_dependencies(deptype="test")
                    for current_edge in test_edges:
                        test_dependency = current_edge.spec
                        if test_dependency in current_spec[node.name]:
                            continue
                        current_spec[node.name].add_dependency_edge(
                            test_dependency.copy(), deptypes="test", virtuals=current_edge.virtuals
                        )

        results = [
            (abstract, self.specs_by_hash[h])
            for abstract, h in zip(self.concretized_user_specs, self.concretized_order)
        ]
        return results

    def concretize_and_add(self, user_spec, concrete_spec=None, tests=False):
        """Concretize and add a single spec to the environment.

        Concretize the provided ``user_spec`` and add it along with the
        concretized result to the environment. If the given ``user_spec`` was
        already present in the environment, this does not add a duplicate.
        The concretized spec will be added unless the ``user_spec`` was
        already present and an associated concrete spec was already present.

        Args:
            concrete_spec: if provided, then it is assumed that it is the
                result of concretizing the provided ``user_spec``
        """
        if self.unify is True:
            msg = (
                "cannot install a single spec in an environment that is "
                "configured to be concretized together. Run instead:\n\n"
                "    $ spack add <spec>\n"
                "    $ spack install\n"
            )
            raise SpackEnvironmentError(msg)

        spec = Spec(user_spec)

        if self.add(spec):
            concrete = concrete_spec or spec.concretized(tests=tests)
            self._add_concrete_spec(spec, concrete)
        else:
            # spec might be in the user_specs, but not installed.
            # TODO: Redo name-based comparison for old style envs
            spec = next(s for s in self.user_specs if s.satisfies(user_spec))
            concrete = self.specs_by_hash.get(spec.dag_hash())
            if not concrete:
                concrete = spec.concretized(tests=tests)
                self._add_concrete_spec(spec, concrete)

        return concrete

    @property
    def default_view(self):
        if not self.views:
            raise SpackEnvironmentError("{0} does not have a view enabled".format(self.name))

        if default_view_name not in self.views:
            raise SpackEnvironmentError(
                "{0} does not have a default view enabled".format(self.name)
            )

        return self.views[default_view_name]

    def update_default_view(self, path_or_bool: Union[str, bool]) -> None:
        """Updates the path of the default view.

        If the argument passed as input is False the default view is deleted, if present. The
        manifest will have an entry "view: false".

        If the argument passed as input is True a default view is created, if not already present.
        The manifest will have an entry "view: true". If a default view is already declared, it
        will be left untouched.

        If the argument passed as input is a path a default view pointing to that path is created,
        if not present already. If a default view is already declared, only its "root" will be
        changed.

        Args:
            path_or_bool: either True, or False or a path
        """
        view_path = self.view_path_default if path_or_bool is True else path_or_bool

        # We don't have the view, and we want to remove it
        if default_view_name not in self.views and path_or_bool is False:
            return

        # We want to enable the view, but we have it already
        if default_view_name in self.views and path_or_bool is True:
            return

        # We have the view, and we want to set it to the same path
        if default_view_name in self.views and self.default_view.root == view_path:
            return

        self.delete_default_view()
        if path_or_bool is False:
            self.views.pop(default_view_name, None)
            self.manifest.remove_default_view()
            return

        # If we had a default view already just update its path,
        # else create a new one and add it to views
        if default_view_name in self.views:
            self.default_view.update_root(view_path)
        else:
            self.views[default_view_name] = ViewDescriptor(self.path, view_path)

        self.manifest.set_default_view(self._default_view_as_yaml())

    def delete_default_view(self) -> None:
        """Deletes the default view associated with this environment."""
        if default_view_name not in self.views:
            return

        try:
            view = pathlib.Path(self.default_view.root)
            shutil.rmtree(view.resolve())
            view.unlink()
        except FileNotFoundError as e:
            msg = f"[ENVIRONMENT] error trying to delete the default view: {str(e)}"
            tty.debug(msg)

    def regenerate_views(self):
        if not self.views:
            tty.debug("Skip view update, this environment does not maintain a view")
            return

        for view in self.views.values():
            view.regenerate(self.concrete_roots())

    def check_views(self):
        """Checks if the environments default view can be activated."""
        try:
            # This is effectively a no-op, but it touches all packages in the
            # default view if they are installed.
            for view_name, view in self.views.items():
                for spec in self.concrete_roots():
                    if spec in view and spec.package and spec.installed:
                        msg = '{0} in view "{1}"'
                        tty.debug(msg.format(spec.name, view_name))

        except (spack.repo.UnknownPackageError, spack.repo.UnknownNamespaceError) as e:
            tty.warn(e)
            tty.warn(
                "Environment %s includes out of date packages or repos. "
                "Loading the environment view will require reconcretization." % self.name
            )

    def _env_modifications_for_default_view(self, reverse=False):
        all_mods = spack.util.environment.EnvironmentModifications()

        visited = set()

        errors = []
        for root_spec in self.concrete_roots():
            if root_spec in self.default_view and root_spec.installed and root_spec.package:
                for spec in root_spec.traverse(deptype="run", root=True):
                    if spec.name in visited:
                        # It is expected that only one instance of the package
                        # can be added to the environment - do not attempt to
                        # add multiple.
                        tty.debug(
                            "Not adding {0} to shell modifications: "
                            "this package has already been added".format(
                                spec.format("{name}/{hash:7}")
                            )
                        )
                        continue
                    else:
                        visited.add(spec.name)

                    try:
                        mods = uenv.environment_modifications_for_spec(spec, self.default_view)
                    except Exception as e:
                        msg = "couldn't get environment settings for %s" % spec.format(
                            "{name}@{version} /{hash:7}"
                        )
                        errors.append((msg, str(e)))
                        continue

                    all_mods.extend(mods.reversed() if reverse else mods)

        return all_mods, errors

    def add_default_view_to_env(self, env_mod):
        """
        Collect the environment modifications to activate an environment using the
        default view. Removes duplicate paths.

        Args:
            env_mod (spack.util.environment.EnvironmentModifications): the environment
                modifications object that is modified.
        """
        if default_view_name not in self.views:
            # No default view to add to shell
            return env_mod

        env_mod.extend(uenv.unconditional_environment_modifications(self.default_view))

        mods, errors = self._env_modifications_for_default_view()
        env_mod.extend(mods)
        if errors:
            for err in errors:
                tty.warn(*err)

        # deduplicate paths from specs mapped to the same location
        for env_var in env_mod.group_by_name():
            env_mod.prune_duplicate_paths(env_var)

        return env_mod

    def rm_default_view_from_env(self, env_mod):
        """
        Collect the environment modifications to deactivate an environment using the
        default view. Reverses the action of ``add_default_view_to_env``.

        Args:
            env_mod (spack.util.environment.EnvironmentModifications): the environment
                modifications object that is modified.
        """
        if default_view_name not in self.views:
            # No default view to add to shell
            return env_mod

        env_mod.extend(uenv.unconditional_environment_modifications(self.default_view).reversed())

        mods, _ = self._env_modifications_for_default_view(reverse=True)
        env_mod.extend(mods)

        return env_mod

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

    def _get_overwrite_specs(self):
        # Find all dev specs that were modified.
        changed_dev_specs = [
            s
            for s in traverse.traverse_nodes(
                self.concrete_roots(), order="breadth", key=traverse.by_dag_hash
            )
            if _is_dev_spec_and_has_changed(s)
        ]

        # Collect their hashes, and the hashes of their installed parents.
        # Notice: with order=breadth all changed dev specs are at depth 0,
        # even if they occur as parents of one another.
        return [
            spec.dag_hash()
            for depth, spec in traverse.traverse_nodes(
                changed_dev_specs,
                root=True,
                order="breadth",
                depth=True,
                direction="parents",
                key=traverse.by_dag_hash,
            )
            if depth == 0 or spec.installed
        ]

    def _install_log_links(self, spec):
        if not spec.external:
            # Make sure log directory exists
            log_path = self.log_path
            fs.mkdirp(log_path)

            with fs.working_dir(self.path):
                # Link the resulting log file into logs dir
                build_log_link = os.path.join(
                    log_path, "%s-%s.log" % (spec.name, spec.dag_hash(7))
                )
                if os.path.lexists(build_log_link):
                    os.remove(build_log_link)
                symlink(spec.package.build_log_path, build_log_link)

    def _partition_roots_by_install_status(self):
        """Partition root specs into those that do not have to be passed to the
        installer, and those that should be, taking into account development
        specs. This is done in a single read transaction per environment instead
        of per spec."""
        installed, uninstalled = [], []
        with spack.store.STORE.db.read_transaction():
            for concretized_hash in self.concretized_order:
                spec = self.specs_by_hash[concretized_hash]
                if not spec.installed or (
                    spec.satisfies("dev_path=*") or spec.satisfies("^dev_path=*")
                ):
                    uninstalled.append(spec)
                else:
                    installed.append(spec)
        return installed, uninstalled

    def uninstalled_specs(self):
        """Return root specs that are not installed, or are installed, but
        are development specs themselves or have those among their dependencies."""
        return self._partition_roots_by_install_status()[1]

    def install_all(self, **install_args):
        """Install all concretized specs in an environment.

        Note: this does not regenerate the views for the environment;
        that needs to be done separately with a call to write().

        Args:
            install_args (dict): keyword install arguments
        """
        self.install_specs(None, **install_args)

    def install_specs(self, specs=None, **install_args):
        tty.debug("Assessing installation status of environment packages")
        # If "spack install" is invoked repeatedly for a large environment
        # where all specs are already installed, the operation can take
        # a large amount of time due to repeatedly acquiring and releasing
        # locks. As a small optimization, drop already installed root specs.
        installed_roots, uninstalled_roots = self._partition_roots_by_install_status()
        if specs:
            specs_to_install = [s for s in specs if s not in installed_roots]
            specs_dropped = [s for s in specs if s in installed_roots]
        else:
            specs_to_install = uninstalled_roots
            specs_dropped = installed_roots

        # We need to repeat the work of the installer thanks to the above optimization:
        # Already installed root specs should be marked explicitly installed in the
        # database.
        if specs_dropped:
            with spack.store.STORE.db.write_transaction():  # do all in one transaction
                for spec in specs_dropped:
                    spack.store.STORE.db.update_explicit(spec, True)

        if not specs_to_install:
            tty.msg("All of the packages are already installed")
        else:
            tty.debug("Processing {0} uninstalled specs".format(len(specs_to_install)))

        specs_to_overwrite = self._get_overwrite_specs()
        tty.debug("{0} specs need to be overwritten".format(len(specs_to_overwrite)))

        install_args["overwrite"] = install_args.get("overwrite", []) + specs_to_overwrite

        installs = []
        for spec in specs_to_install:
            pkg_install_args = install_args.copy()
            pkg_install_args["explicit"] = spec in self.roots()
            installs.append((spec.package, pkg_install_args))

        try:
            builder = PackageInstaller(installs)
            builder.install()
        finally:
            # Ensure links are set appropriately
            for spec in specs_to_install:
                if spec.installed:
                    self.new_installs.append(spec)
                    try:
                        self._install_log_links(spec)
                    except OSError as e:
                        tty.warn(
                            "Could not install log links for {0}: {1}".format(spec.name, str(e))
                        )

    def all_specs_generator(self) -> Iterable[Spec]:
        """Returns a generator for all concrete specs"""
        return traverse.traverse_nodes(self.concrete_roots(), key=traverse.by_dag_hash)

    def all_specs(self) -> List[Spec]:
        """Returns a list of all concrete specs"""
        return list(self.all_specs_generator())

    def all_hashes(self):
        """Return hashes of all specs."""
        return [s.dag_hash() for s in self.all_specs_generator()]

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
        # use a transaction to avoid overhead of repeated calls
        # to `package.spec.installed`
        with spack.store.STORE.db.read_transaction():
            concretized = dict(self.concretized_specs())
            for spec in self.user_specs:
                concrete = concretized.get(spec)
                if not concrete:
                    yield spec
                elif not concrete.installed:
                    yield concrete

    def concretized_specs(self):
        """Tuples of (user spec, concrete spec) for all concrete specs."""
        for s, h in zip(self.concretized_user_specs, self.concretized_order):
            yield (s, self.specs_by_hash[h])

    def concrete_roots(self):
        """Same as concretized_specs, except it returns the list of concrete
        roots *without* associated user spec"""
        return [root for _, root in self.concretized_specs()]

    def get_by_hash(self, dag_hash: str) -> List[Spec]:
        # If it's not a partial hash prefix we can early exit
        early_exit = len(dag_hash) == 32
        matches = []
        for spec in traverse.traverse_nodes(
            self.concrete_roots(), key=traverse.by_dag_hash, order="breadth"
        ):
            if spec.dag_hash().startswith(dag_hash):
                matches.append(spec)
                if early_exit:
                    break
        return matches

    def get_one_by_hash(self, dag_hash):
        """Returns the single spec from the environment which matches the
        provided hash.  Raises an AssertionError if no specs match or if
        more than one spec matches."""
        hash_matches = self.get_by_hash(dag_hash)
        assert len(hash_matches) == 1
        return hash_matches[0]

    def all_matching_specs(self, *specs: spack.spec.Spec) -> List[Spec]:
        """Returns all concretized specs in the environment satisfying any of the input specs"""
        return [
            s
            for s in traverse.traverse_nodes(self.concrete_roots(), key=traverse.by_dag_hash)
            if any(s.satisfies(t) for t in specs)
        ]

    @spack.repo.autospec
    def matching_spec(self, spec):
        """
        Given a spec (likely not concretized), find a matching concretized
        spec in the environment.

        The matching spec does not have to be installed in the environment,
        but must be concrete (specs added with `spack add` without an
        intervening `spack concretize` will not be matched).

        If there is a single root spec that matches the provided spec or a
        single dependency spec that matches the provided spec, then the
        concretized instance of that spec will be returned.

        If multiple root specs match the provided spec, or no root specs match
        and multiple dependency specs match, then this raises an error
        and reports all matching specs.
        """
        env_root_to_user = {root.dag_hash(): user for user, root in self.concretized_specs()}
        root_matches, dep_matches = [], []

        for env_spec in traverse.traverse_nodes(
            specs=[root for _, root in self.concretized_specs()],
            key=traverse.by_dag_hash,
            order="breadth",
        ):
            if not env_spec.satisfies(spec):
                continue

            # If the spec is concrete, then there is no possibility of multiple matches,
            # and we immediately return the single match
            if spec.concrete:
                return env_spec

            # Distinguish between environment roots and deps. Specs that are both
            # are classified as environment roots.
            user_spec = env_root_to_user.get(env_spec.dag_hash())
            if user_spec:
                root_matches.append((env_spec, user_spec))
            else:
                dep_matches.append(env_spec)

        # No matching spec
        if not root_matches and not dep_matches:
            return None

        # Single root spec, any number of dep specs => return root spec.
        if len(root_matches) == 1:
            return root_matches[0][0]

        if not root_matches and len(dep_matches) == 1:
            return dep_matches[0]

        # More than one spec matched, and either multiple roots matched or
        # none of the matches were roots
        # If multiple root specs match, it is assumed that the abstract
        # spec will most-succinctly summarize the difference between them
        # (and the user can enter one of these to disambiguate)
        fmt_str = "{hash:7}  " + spack.spec.DEFAULT_FORMAT
        color = clr.get_color_when()
        match_strings = [
            f"Root spec {abstract.format(color=color)}\n  {concrete.format(fmt_str, color=color)}"
            for concrete, abstract in root_matches
        ]
        match_strings.extend(
            f"Dependency spec\n  {s.format(fmt_str, color=color)}" for s in dep_matches
        )
        matches_str = "\n".join(match_strings)

        raise SpackEnvironmentError(
            f"{spec} matches multiple specs in the environment {self.name}: \n{matches_str}"
        )

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
        specs = [self.specs_by_hash[h] for h in self.concretized_order]

        if recurse_dependencies:
            specs.extend(
                traverse.traverse_nodes(
                    specs, root=False, deptype=("link", "run"), key=traverse.by_dag_hash
                )
            )

        return specs

    def _to_lockfile_dict(self):
        """Create a dictionary to store a lockfile for this environment."""
        concrete_specs = {}
        for s in traverse.traverse_nodes(self.specs_by_hash.values(), key=traverse.by_dag_hash):
            spec_dict = s.node_dict_with_hashes(hash=ht.dag_hash)
            # Assumes no legacy formats, since this was just created.
            spec_dict[ht.dag_hash.name] = s.dag_hash()
            concrete_specs[s.dag_hash()] = spec_dict

        hash_spec_list = zip(self.concretized_order, self.concretized_user_specs)

        spack_dict = {"version": spack.spack_version}
        spack_commit = spack.main.get_spack_commit()
        if spack_commit:
            spack_dict["type"] = "git"
            spack_dict["commit"] = spack_commit
        else:
            spack_dict["type"] = "release"

        # this is the lockfile we'll write out
        data = {
            # metadata about the format
            "_meta": {
                "file-type": "spack-lockfile",
                "lockfile-version": lockfile_format_version,
                "specfile-version": spack.spec.SPECFILE_FORMAT_VERSION,
            },
            # spack version information
            "spack": spack_dict,
            # users specs + hashes are the 'roots' of the environment
            "roots": [{"hash": h, "spec": str(s)} for h, s in hash_spec_list],
            # Concrete specs by hash, including dependencies
            "concrete_specs": concrete_specs,
        }

        return data

    def _read_lockfile(self, file_or_json):
        """Read a lockfile from a file or from a raw string."""
        lockfile_dict = sjson.load(file_or_json)
        self._read_lockfile_dict(lockfile_dict)
        return lockfile_dict["_meta"]["lockfile-version"]

    def _read_lockfile_dict(self, d):
        """Read a lockfile dictionary into this environment."""
        self.specs_by_hash = {}

        roots = d["roots"]
        self.concretized_user_specs = [Spec(r["spec"]) for r in roots]
        self.concretized_order = [r["hash"] for r in roots]
        json_specs_by_hash = d["concrete_specs"]

        # Track specs by their lockfile key.  Currently spack uses the finest
        # grained hash as the lockfile key, while older formats used the build
        # hash or a previous incarnation of the DAG hash (one that did not
        # include build deps or package hash).
        specs_by_hash = {}

        # Track specs by their DAG hash, allows handling DAG hash collisions
        first_seen = {}
        current_lockfile_format = d["_meta"]["lockfile-version"]
        try:
            reader = READER_CLS[current_lockfile_format]
        except KeyError:
            msg = (
                f"Spack {spack.__version__} cannot read the lockfile '{self.lock_path}', using "
                f"the v{current_lockfile_format} format."
            )
            if lockfile_format_version < current_lockfile_format:
                msg += " You need to use a newer Spack version."
            raise SpackEnvironmentError(msg)

        # First pass: Put each spec in the map ignoring dependencies
        for lockfile_key, node_dict in json_specs_by_hash.items():
            spec = reader.from_node_dict(node_dict)
            if not spec._hash:
                # in v1 lockfiles, the hash only occurs as a key
                spec._hash = lockfile_key
            specs_by_hash[lockfile_key] = spec

        # Second pass: For each spec, get its dependencies from the node dict
        # and add them to the spec
        for lockfile_key, node_dict in json_specs_by_hash.items():
            name, data = reader.name_and_data(node_dict)
            for _, dep_hash, deptypes, _, virtuals in reader.dependencies_from_node_dict(data):
                specs_by_hash[lockfile_key]._add_dependency(
                    specs_by_hash[dep_hash], deptypes=deptypes, virtuals=virtuals
                )

        # Traverse the root specs one at a time in the order they appear.
        # The first time we see each DAG hash, that's the one we want to
        # keep.  This is only required as long as we support older lockfile
        # formats where the mapping from DAG hash to lockfile key is possibly
        # one-to-many.
        for lockfile_key in self.concretized_order:
            for s in specs_by_hash[lockfile_key].traverse():
                if s.dag_hash() not in first_seen:
                    first_seen[s.dag_hash()] = s

        # Now make sure concretized_order and our internal specs dict
        # contains the keys used by modern spack (i.e. the dag_hash
        # that includes build deps and package hash).
        self.concretized_order = [
            specs_by_hash[h_key].dag_hash() for h_key in self.concretized_order
        ]

        for spec_dag_hash in self.concretized_order:
            self.specs_by_hash[spec_dag_hash] = first_seen[spec_dag_hash]

    def write(self, regenerate: bool = True) -> None:
        """Writes an in-memory environment to its location on disk.

        Write out package files for each newly concretized spec.  Also
        regenerate any views associated with the environment and run post-write
        hooks, if regenerate is True.

        Args:
            regenerate: regenerate views and run post-write hooks as well as writing if True.
        """
        self.manifest_uptodate_or_warn()
        if self.specs_by_hash:
            self.ensure_env_directory_exists(dot_env=True)
            self.update_environment_repository()
            self.manifest.flush()
            # Write the lock file last. This is useful for Makefiles
            # with `spack.lock: spack.yaml` rules, where the target
            # should be newer than the prerequisite to avoid
            # redundant re-concretization.
            self.update_lockfile()
        else:
            self.ensure_env_directory_exists(dot_env=False)
            with fs.safe_remove(self.lock_path):
                self.manifest.flush()

        if regenerate:
            self.regenerate_views()
            spack.hooks.post_env_write(self)

        self._reset_new_specs_and_installs()

    def _reset_new_specs_and_installs(self) -> None:
        self.new_specs = []
        self.new_installs = []

    def update_lockfile(self) -> None:
        with fs.write_tmp_and_move(self.lock_path) as f:
            sjson.dump(self._to_lockfile_dict(), stream=f)

    def ensure_env_directory_exists(self, dot_env: bool = False) -> None:
        """Ensure that the root directory of the environment exists

        Args:
            dot_env: if True also ensures that the <root>/.env directory exists
        """
        fs.mkdirp(self.path)
        if dot_env:
            fs.mkdirp(self.env_subdir_path)

    def update_environment_repository(self) -> None:
        """Updates the repository associated with the environment."""
        for spec in traverse.traverse_nodes(self.new_specs):
            if not spec.concrete:
                raise ValueError("specs passed to environment.write() must be concrete!")

            self._add_to_environment_repository(spec)

    def _add_to_environment_repository(self, spec_node: Spec) -> None:
        """Add the root node of the spec to the environment repository"""
        repository_dir = os.path.join(self.repos_path, spec_node.namespace)
        repository = spack.repo.create_or_construct(repository_dir, spec_node.namespace)
        pkg_dir = repository.dirname_for_package_name(spec_node.name)
        fs.mkdirp(pkg_dir)
        spack.repo.PATH.dump_provenance(spec_node, pkg_dir)

    def manifest_uptodate_or_warn(self):
        """Emits a warning if the manifest file is not up-to-date."""
        if not is_latest_format(self.manifest_path):
            ver = ".".join(str(s) for s in spack.spack_version_info[:2])
            msg = (
                'The environment "{}" is written to disk in a deprecated format. '
                "Please update it using:\n\n"
                "\tspack env update {}\n\n"
                "Note that versions of Spack older than {} may not be able to "
                "use the updated configuration."
            )
            warnings.warn(msg.format(self.name, self.name, ver))

    def _default_view_as_yaml(self):
        """This internal function assumes the default view is set"""
        path = self.default_view.raw_root
        if (
            self.default_view == ViewDescriptor(self.path, self.view_path_default)
            and len(self.views) == 1
        ):
            return True

        if self.default_view == ViewDescriptor(self.path, path) and len(self.views) == 1:
            return path

        return self.default_view.to_dict()

    def invalidate_repository_cache(self):
        self._repo = None

    def __enter__(self):
        self._previous_active = _active_environment
        activate(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        deactivate()
        if self._previous_active:
            activate(self._previous_active)


def yaml_equivalent(first, second) -> bool:
    """Returns whether two spack yaml items are equivalent, including overrides"""
    # YAML has timestamps and dates, but we don't use them yet in schemas
    if isinstance(first, dict):
        return isinstance(second, dict) and _equiv_dict(first, second)
    elif isinstance(first, list):
        return isinstance(second, list) and _equiv_list(first, second)
    elif isinstance(first, bool):
        return isinstance(second, bool) and first is second
    elif isinstance(first, int):
        return isinstance(second, int) and first == second
    elif first is None:
        return second is None
    else:  # it's a string
        return isinstance(second, str) and first == second


def _equiv_list(first, second):
    """Returns whether two spack yaml lists are equivalent, including overrides"""
    if len(first) != len(second):
        return False
    return all(yaml_equivalent(f, s) for f, s in zip(first, second))


def _equiv_dict(first, second):
    """Returns whether two spack yaml dicts are equivalent, including overrides"""
    if len(first) != len(second):
        return False
    same_values = all(yaml_equivalent(fv, sv) for fv, sv in zip(first.values(), second.values()))
    same_keys_with_same_overrides = all(
        fk == sk and getattr(fk, "override", False) == getattr(sk, "override", False)
        for fk, sk in zip(first.keys(), second.keys())
    )
    return same_values and same_keys_with_same_overrides


def display_specs(concretized_specs):
    """Displays the list of specs returned by `Environment.concretize()`.

    Args:
        concretized_specs (list): list of specs returned by
            `Environment.concretize()`
    """

    def _tree_to_display(spec):
        return spec.tree(
            recurse_dependencies=True,
            format=spack.spec.DISPLAY_FORMAT,
            status_fn=spack.spec.Spec.install_status,
            hashlen=7,
            hashes=True,
        )

    for user_spec, concrete_spec in concretized_specs:
        tty.msg("Concretized {0}".format(user_spec))
        sys.stdout.write(_tree_to_display(concrete_spec))
        print("")


def _concretize_from_constraints(spec_constraints, tests=False):
    # Accept only valid constraints from list and concretize spec
    # Get the named spec even if out of order
    root_spec = [s for s in spec_constraints if s.name]
    if len(root_spec) != 1:
        m = "The constraints %s are not a valid spec " % spec_constraints
        m += "concretization target. all specs must have a single name "
        m += "constraint for concretization."
        raise InvalidSpecConstraintError(m)
    spec_constraints.remove(root_spec[0])

    invalid_constraints = []
    while True:
        # Attach all anonymous constraints to one named spec
        s = root_spec[0].copy()
        for c in spec_constraints:
            if c not in invalid_constraints:
                s.constrain(c)
        try:
            return s.concretized(tests=tests)
        except spack.spec.InvalidDependencyError as e:
            invalid_deps_string = ["^" + d for d in e.invalid_deps]
            invalid_deps = [
                c
                for c in spec_constraints
                if any(c.satisfies(invd) for invd in invalid_deps_string)
            ]
            if len(invalid_deps) != len(invalid_deps_string):
                raise e
            invalid_constraints.extend(invalid_deps)
        except UnknownVariantError as e:
            invalid_variants = e.unknown_variants
            inv_variant_constraints = [
                c for c in spec_constraints if any(name in c.variants for name in invalid_variants)
            ]
            if len(inv_variant_constraints) != len(invalid_variants):
                raise e
            invalid_constraints.extend(inv_variant_constraints)


def _concretize_task(packed_arguments):
    spec_constraints, tests = packed_arguments
    with tty.SuppressOutput(msg_enabled=False):
        return _concretize_from_constraints(spec_constraints, tests)


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
        spack.config.CONFIG.push_scope(scope)


def deactivate_config_scope(env):
    """Remove any scopes from env from the global config path."""
    for scope in env.config_scopes():
        spack.config.CONFIG.remove_scope(scope.name)


def manifest_file(env_name_or_dir):
    """Return the absolute path to a manifest file given the environment
    name or directory.

    Args:
        env_name_or_dir (str): either the name of a valid environment
            or a directory where a manifest file resides

    Raises:
        AssertionError: if the environment is not found
    """
    env_dir = None
    if is_env_dir(env_name_or_dir):
        env_dir = os.path.abspath(env_name_or_dir)
    elif exists(env_name_or_dir):
        env_dir = os.path.abspath(root(env_name_or_dir))

    assert env_dir, "environment not found [env={0}]".format(env_name_or_dir)
    return os.path.join(env_dir, manifest_name)


def update_yaml(manifest, backup_file):
    """Update a manifest file from an old format to the current one.

    Args:
        manifest (str): path to a manifest file
        backup_file (str): file where to copy the original manifest

    Returns:
        True if the manifest was updated, False otherwise.

    Raises:
        AssertionError: in case anything goes wrong during the update
    """
    # Check if the environment needs update
    with open(manifest) as f:
        data = syaml.load(f)

    top_level_key = _top_level_key(data)
    needs_update = spack.schema.env.update(data[top_level_key])
    if not needs_update:
        msg = "No update needed [manifest={0}]".format(manifest)
        tty.debug(msg)
        return False

    # Copy environment to a backup file and update it
    msg = (
        'backup file "{0}" already exists on disk. Check its content '
        "and remove it before trying to update again."
    )
    assert not os.path.exists(backup_file), msg.format(backup_file)

    shutil.copy(manifest, backup_file)
    with open(manifest, "w") as f:
        syaml.dump_config(data, f)
    return True


def _top_level_key(data):
    """Return the top level key used in this environment

    Args:
        data (dict): raw yaml data of the environment

    Returns:
        Either 'spack' or 'env'
    """
    msg = 'cannot find top level attribute "spack" or "env"' "in the environment"
    assert any(x in data for x in ("spack", "env")), msg
    if "spack" in data:
        return "spack"
    return "env"


def is_latest_format(manifest):
    """Return False if the manifest file exists and is not in the latest schema format.

    Args:
        manifest (str): manifest file to be analyzed
    """
    try:
        with open(manifest) as f:
            data = syaml.load(f)
    except (OSError, IOError):
        return True
    top_level_key = _top_level_key(data)
    changed = spack.schema.env.update(data[top_level_key])
    return not changed


@contextlib.contextmanager
def no_active_environment():
    """Deactivate the active environment for the duration of the context. Has no
    effect when there is no active environment."""
    env = active_environment()
    try:
        deactivate()
        yield
    finally:
        # TODO: we don't handle `use_env_repo` here.
        if env:
            activate(env)


def initialize_environment_dir(
    environment_dir: Union[str, pathlib.Path], envfile: Optional[Union[str, pathlib.Path]]
) -> None:
    """Initialize an environment directory starting from an envfile.

    Files with suffix .json or .lock are considered lockfiles. Files with any other name
    are considered manifest files.

    Args:
        environment_dir: directory where the environment should be placed
        envfile: manifest file or lockfile used to initialize the environment

    Raises:
        SpackEnvironmentError: if the directory can't be initialized
    """
    environment_dir = pathlib.Path(environment_dir)
    target_lockfile = environment_dir / lockfile_name
    target_manifest = environment_dir / manifest_name
    if target_manifest.exists():
        msg = f"cannot initialize environment, {target_manifest} already exists"
        raise SpackEnvironmentError(msg)

    if target_lockfile.exists():
        msg = f"cannot initialize environment, {target_lockfile} already exists"
        raise SpackEnvironmentError(msg)

    def _ensure_env_dir():
        try:
            environment_dir.mkdir(parents=True, exist_ok=True)
        except FileExistsError as e:
            msg = f"cannot initialize the environment, '{environment_dir}' already exists"
            raise SpackEnvironmentError(msg) from e

    if envfile is None:
        _ensure_env_dir()
        target_manifest.write_text(default_manifest_yaml())
        return

    envfile = pathlib.Path(envfile)
    if not envfile.exists() or not envfile.is_file():
        msg = f"cannot initialize environment, {envfile} is not a valid file"
        raise SpackEnvironmentError(msg)

    _ensure_env_dir()

    # When we have a lockfile we should copy that and produce a consistent default manifest
    if str(envfile).endswith(".lock") or str(envfile).endswith(".json"):
        shutil.copy(envfile, target_lockfile)
        # This constructor writes a spack.yaml which is consistent with the root
        # specs in the spack.lock
        try:
            EnvironmentManifestFile.from_lockfile(environment_dir)
        except Exception as e:
            msg = f"cannot initialize environment, '{environment_dir}' from lockfile"
            raise SpackEnvironmentError(msg) from e
        return

    shutil.copy(envfile, target_manifest)


class EnvironmentManifestFile(collections.abc.Mapping):
    """Manages the in-memory representation of a manifest file, and its synchronization
    with the actual manifest on disk.
    """

    @staticmethod
    def from_lockfile(manifest_dir: Union[pathlib.Path, str]) -> "EnvironmentManifestFile":
        """Returns an environment manifest file compatible with the lockfile already present in
        the environment directory.

        This function also writes a spack.yaml file that is consistent with the spack.lock
        already existing in the directory.

        Args:
             manifest_dir: directory where the lockfile is
        """
        manifest_dir = pathlib.Path(manifest_dir)
        lockfile = manifest_dir / lockfile_name
        with lockfile.open("r") as f:
            data = sjson.load(f)
        user_specs = data["roots"]

        default_content = manifest_dir / manifest_name
        default_content.write_text(default_manifest_yaml())
        manifest = EnvironmentManifestFile(manifest_dir)
        for item in user_specs:
            manifest.add_user_spec(item["spec"])
        manifest.flush()
        return manifest

    def __init__(self, manifest_dir: Union[pathlib.Path, str]) -> None:
        self.manifest_dir = pathlib.Path(manifest_dir)
        self.manifest_file = self.manifest_dir / manifest_name

        if not self.manifest_file.exists():
            msg = f"cannot find '{manifest_name}' in {self.manifest_dir}"
            raise SpackEnvironmentError(msg)

        with self.manifest_file.open() as f:
            raw, with_defaults_added = _read_yaml(f)

        #: Pristine YAML content, without defaults being added
        self.pristine_yaml_content = raw
        #: YAML content with defaults added by Spack, if they're missing
        self.yaml_content = with_defaults_added
        self.changed = False

    def add_user_spec(self, user_spec: str) -> None:
        """Appends the user spec passed as input to the list of root specs.

        Args:
            user_spec: user spec to be appended
        """
        self.pristine_configuration.setdefault("specs", []).append(user_spec)
        self.configuration.setdefault("specs", []).append(user_spec)
        self.changed = True

    def remove_user_spec(self, user_spec: str) -> None:
        """Removes the user spec passed as input from the list of root specs

        Args:
            user_spec: user spec to be removed

        Raises:
            SpackEnvironmentError: when the user spec is not in the list
        """
        try:
            self.pristine_configuration["specs"].remove(user_spec)
            self.configuration["specs"].remove(user_spec)
        except ValueError as e:
            msg = f"cannot remove {user_spec} from {self}, no such spec exists"
            raise SpackEnvironmentError(msg) from e
        self.changed = True

    def override_user_spec(self, user_spec: str, idx: int) -> None:
        """Overrides the user spec at index idx with the one passed as input.

        Args:
            user_spec: new user spec
            idx: index of the spec to be overridden

        Raises:
            SpackEnvironmentError: when the user spec cannot be overridden
        """
        try:
            self.pristine_configuration["specs"][idx] = user_spec
            self.configuration["specs"][idx] = user_spec
        except ValueError as e:
            msg = f"cannot override {user_spec} from {self}"
            raise SpackEnvironmentError(msg) from e
        self.changed = True

    def add_definition(self, user_spec: str, list_name: str) -> None:
        """Appends a user spec to the first active definition mathing the name passed as argument.

        Args:
            user_spec: user spec to be appended
            list_name: name of the definition where to append

        Raises:
            SpackEnvironmentError: is no valid definition exists already
        """
        defs = self.pristine_configuration.get("definitions", [])
        msg = f"cannot add {user_spec} to the '{list_name}' definition, no valid list exists"

        for idx, item in self._iterate_on_definitions(defs, list_name=list_name, err_msg=msg):
            item[list_name].append(user_spec)
            break

        self.configuration["definitions"][idx][list_name].append(user_spec)
        self.changed = True

    def remove_definition(self, user_spec: str, list_name: str) -> None:
        """Removes a user spec from an active definition that matches the name passed as argument.

        Args:
            user_spec: user spec to be removed
            list_name: name of the definition where to remove the spec from

        Raises:
            SpackEnvironmentError: if the user spec cannot be removed from the list,
                or the list does not exist
        """
        defs = self.pristine_configuration.get("definitions", [])
        msg = (
            f"cannot remove {user_spec} from the '{list_name}' definition, "
            f"no valid list exists"
        )

        for idx, item in self._iterate_on_definitions(defs, list_name=list_name, err_msg=msg):
            try:
                item[list_name].remove(user_spec)
                break
            except ValueError:
                pass

        self.configuration["definitions"][idx][list_name].remove(user_spec)
        self.changed = True

    def override_definition(self, user_spec: str, *, override: str, list_name: str) -> None:
        """Overrides a user spec from an active definition that matches the name passed
        as argument.

        Args:
            user_spec: user spec to be overridden
            override: new spec to be used
            list_name: name of the definition where to override the spec

        Raises:
            SpackEnvironmentError: if the user spec cannot be overridden
        """
        defs = self.pristine_configuration.get("definitions", [])
        msg = f"cannot override {user_spec} with {override} in the '{list_name}' definition"

        for idx, item in self._iterate_on_definitions(defs, list_name=list_name, err_msg=msg):
            try:
                sub_index = item[list_name].index(user_spec)
                item[list_name][sub_index] = override
                break
            except ValueError:
                pass

        self.configuration["definitions"][idx][list_name][sub_index] = override
        self.changed = True

    def _iterate_on_definitions(self, definitions, *, list_name, err_msg):
        """Iterates on definitions, returning the active ones matching a given name."""

        def extract_name(_item):
            names = list(x for x in _item if x != "when")
            assert len(names) == 1, f"more than one name in {_item}"
            return names[0]

        for idx, item in enumerate(definitions):
            name = extract_name(item)
            if name != list_name:
                continue

            condition_str = item.get("when", "True")
            if not _eval_conditional(condition_str):
                continue

            yield idx, item
        else:
            raise SpackEnvironmentError(err_msg)

    def set_default_view(self, view: Union[bool, str, pathlib.Path, Dict[str, str]]) -> None:
        """Sets the default view root in the manifest to the value passed as input.

        Args:
            view: If the value is a string or a path, it specifies the path to the view. If
                True the default view is used for the environment, if False there's no view.
        """
        if isinstance(view, dict):
            self.pristine_configuration["view"][default_view_name].update(view)
            self.configuration["view"][default_view_name].update(view)
            self.changed = True
            return

        if not isinstance(view, bool):
            view = str(view)

        self.pristine_configuration["view"] = view
        self.configuration["view"] = view
        self.changed = True

    def remove_default_view(self) -> None:
        """Removes the default view from the manifest file"""
        view_data = self.pristine_configuration.get("view")
        if isinstance(view_data, collections.abc.Mapping):
            self.pristine_configuration["view"].pop(default_view_name)
            self.configuration["view"].pop(default_view_name)
            self.changed = True
            return

        self.set_default_view(view=False)

    def add_develop_spec(self, pkg_name: str, entry: Dict[str, str]) -> None:
        """Adds a develop spec to the manifest file

        Args:
            pkg_name: name of the package to be developed
            entry: spec and path of the developed package
        """
        # The environment sets the path to pkg_name is that is implicit
        if entry["path"] == pkg_name:
            entry.pop("path")

        self.pristine_configuration.setdefault("develop", {}).setdefault(pkg_name, {}).update(
            entry
        )
        self.configuration.setdefault("develop", {}).setdefault(pkg_name, {}).update(entry)
        self.changed = True

    def remove_develop_spec(self, pkg_name: str) -> None:
        """Removes a develop spec from the manifest file

        Args:
            pkg_name: package to be removed from development

        Raises:
            SpackEnvironmentError: if there is nothing to remove
        """
        try:
            del self.pristine_configuration["develop"][pkg_name]
        except KeyError as e:
            msg = f"cannot remove '{pkg_name}' from develop specs in {self}, entry does not exist"
            raise SpackEnvironmentError(msg) from e
        del self.configuration["develop"][pkg_name]
        self.changed = True

    def absolutify_dev_paths(self, init_file_dir: Union[str, pathlib.Path]) -> None:
        """Normalizes the dev paths in the environment with respect to the directory where the
        initialization file resides.

        Args:
            init_file_dir: directory with the "spack.yaml" used to initialize the environment.
        """
        init_file_dir = pathlib.Path(init_file_dir).absolute()
        for _, entry in self.pristine_configuration.get("develop", {}).items():
            expanded_path = os.path.normpath(str(init_file_dir / entry["path"]))
            entry["path"] = str(expanded_path)

        for _, entry in self.configuration.get("develop", {}).items():
            expanded_path = os.path.normpath(str(init_file_dir / entry["path"]))
            entry["path"] = str(expanded_path)
        self.changed = True

    def flush(self) -> None:
        """Synchronizes the object with the manifest file on disk."""
        if not self.changed:
            return

        with fs.write_tmp_and_move(os.path.realpath(self.manifest_file)) as f:
            _write_yaml(self.pristine_yaml_content, f)
        self.changed = False

    @property
    def pristine_configuration(self):
        """Return the dictionaries in the pristine YAML, without the top level attribute"""
        return self.pristine_yaml_content[TOP_LEVEL_KEY]

    @property
    def configuration(self):
        """Return the dictionaries in the YAML, without the top level attribute"""
        return self.yaml_content[TOP_LEVEL_KEY]

    def __len__(self):
        return len(self.yaml_content)

    def __getitem__(self, key):
        return self.yaml_content[key]

    def __iter__(self):
        return iter(self.yaml_content)

    def __str__(self):
        return str(self.manifest_file)


class SpackEnvironmentError(spack.error.SpackError):
    """Superclass for all errors to do with Spack environments."""


class SpackEnvironmentViewError(SpackEnvironmentError):
    """Class for errors regarding view generation."""
