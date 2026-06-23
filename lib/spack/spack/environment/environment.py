# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import collections.abc
import contextlib
import glob
import os
import pathlib
import re
import shutil
import stat
import uuid
import warnings
from collections.abc import KeysView
from itertools import zip_longest
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

import spack
import spack.config
import spack.deptypes as dt
import spack.error
import spack.filesystem_view as fsv
import spack.hash_types as ht
import spack.installer_dispatch
import spack.llnl.util.filesystem as fs
import spack.llnl.util.tty as tty
import spack.llnl.util.tty.color as clr
import spack.package_base
import spack.paths
import spack.repo
import spack.schema.env
import spack.schema.spec_list
import spack.spec
import spack.store
import spack.user_environment as uenv
import spack.util.environment
import spack.util.hash
import spack.util.lock as lk
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.variant as vt
from spack import traverse
from spack.config import substitute_path_variables
from spack.enums import ConfigScopePriority
from spack.llnl.util.filesystem import copy_tree, islink, readlink
from spack.llnl.util.lang import stable_partition
from spack.schema.env import TOP_LEVEL_KEY
from spack.spec import Spec
from spack.spec_filter import SpecFilter
from spack.util.link_tree import ConflictingSpecsError

from .list import SpecList, SpecListError, SpecListParser

SpecPair = Tuple[Spec, Spec]

DEFAULT_USER_SPEC_GROUP = "default"

#: environment variable used to indicate the active environment
spack_env_var = "SPACK_ENV"

#: environment variable used to indicate the active environment view
spack_env_view_var = "SPACK_ENV_VIEW"

#: currently activated environment
_active_environment: Optional["Environment"] = None

# This is used in spack.main to bypass env failures if the command is `spack config edit`
# It is used in spack.cmd.config to get the path to a failed env for `spack config edit`
#: Validation error for a currently activate environment that failed to parse
_active_environment_error: Optional[spack.config.ConfigFormatError] = None

#: default path where environments are stored in the spack tree
default_env_path = os.path.join(spack.paths.var_path, "environments")


#: Name of the input yaml file for an environment
manifest_name = "spack.yaml"


#: Name of the input yaml file for an environment
lockfile_name = "spack.lock"


#: Name of the directory where environments store repos, logs, views, configs
env_subdir_name = ".spack-env"

#: Name of the file inside the view to mark it as Spack-owned with content hash for currency checks
MARKER_FILE = ".spack-view"


def env_root_path() -> str:
    """Override default root path if the user specified it"""
    return spack.config.canonicalize_path(
        spack.config.get("config:environments_root", default=default_env_path)
    )


def environment_name(path: Union[str, pathlib.Path]) -> str:
    """Human-readable representation of the environment.

    This is the path for independent environments, and just the name
    for managed environments.
    """
    env_root = pathlib.Path(env_root_path()).resolve()
    path_path = pathlib.Path(path)

    # For a managed environment created in Spack, env.path is ENV_ROOT/NAME
    # For a tracked environment from `spack env track`, the path is symlinked to ENV_ROOT/NAME
    # So if ENV_ROOT/NAME resolves to env.path we know the environment is tracked/managed.
    # Otherwise, it is an independent environment and  we return the path.
    #
    # We resolve both paths fully because the env_root itself could also be a symlink,
    # and any directory in env.path could be a symlink.
    if (env_root / path_path.name).resolve() == path_path.resolve():
        return path_path.name
    else:
        return str(path)


def ensure_no_disallowed_env_config_mods(scope: spack.config.ConfigScope) -> None:
    config = scope.get_section("config")
    if config and "environments_root" in config["config"]:
        raise SpackEnvironmentError(
            "Spack environments are prohibited from modifying 'config:environments_root' "
            "because it can make the definition of the environment ill-posed. Please "
            "remove from your environment and place it in a permanent scope such as "
            "defaults, system, site, etc."
        )


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
""".format("true" if spack.config.get("concretizer:unify") else "false")


sep_re = re.escape(os.sep)

#: regex for validating environment names
valid_environment_name_re = rf"^\w[{sep_re}\w-]*$"

#: version of the lockfile format. Must increase monotonically.
CURRENT_LOCKFILE_VERSION = 7


READER_CLS = {
    1: spack.spec.SpecfileV1,
    2: spack.spec.SpecfileV1,
    3: spack.spec.SpecfileV2,
    4: spack.spec.SpecfileV3,
    5: spack.spec.SpecfileV4,
    6: spack.spec.SpecfileV5,
    7: spack.spec.SpecfileV5,
}


# Magic names
# The name of the standalone spec list in the manifest yaml
USER_SPECS_KEY = "specs"
# The name of the default view (the view loaded on env.activate)
default_view_name = "default"
# Default behavior to link all packages into views (vs. only root packages)
default_view_link = "all"

# (DEPRECATED) Use as the heading/name in the manifest is deprecated.
# The key for any concrete specs included in a lockfile.
lockfile_include_key = "include_concrete"

# The name/heading for include paths in the manifest file.
manifest_include_name = "include"


def installed_specs():
    """
    Returns the specs of packages installed in the active environment or None
    if no packages are installed.
    """
    env = active_environment()
    hashes = env.all_hashes() if env else None
    return spack.store.STORE.db.query(hashes=hashes)


def valid_env_name(name):
    return re.match(valid_environment_name_re, name)


def validate_env_name(name):
    if not valid_env_name(name):
        raise ValueError(
            f"{name}: names may only contain letters, numbers, _, and -, and may not start with -."
        )
    return name


def activate(env, use_env_repo=False):
    """Activate an environment.

    To activate an environment, we add its manifest's configuration scope to the
    existing Spack configuration, and we set active to the current environment.

    Arguments:
        env (Environment): the environment to activate
        use_env_repo (bool): use the packages exactly as they appear in the
            environment's repository
    """
    global _active_environment

    try:
        _active_environment = env

        # Fail early to avoid ending in an invalid state
        if not isinstance(env, Environment):
            raise TypeError("`env` should be of type {0}".format(Environment.__name__))

        # Check if we need to reinitialize spack.store.STORE and spack.repo.REPO due to
        # config changes.
        install_tree_before = spack.config.get("config:install_tree")
        upstreams_before = spack.config.get("upstreams")
        repos_before = spack.config.get("repos")
        env.manifest.prepare_config_scope()
        install_tree_after = spack.config.get("config:install_tree")
        upstreams_after = spack.config.get("upstreams")
        repos_after = spack.config.get("repos")

        if install_tree_before != install_tree_after or upstreams_before != upstreams_after:
            setattr(env, "store_token", spack.store.reinitialize())

        if repos_before != repos_after:
            setattr(env, "repo_token", spack.repo.PATH)
            spack.repo.PATH.disable()
            new_repo = spack.repo.RepoPath.from_config(spack.config.CONFIG)
            if use_env_repo:
                new_repo.put_first(env.repo)
            spack.repo.enable_repo(new_repo)

        tty.debug(f"Using environment '{env.name}'")
    except Exception:
        _active_environment = None
        raise


def deactivate():
    """Undo any configuration or repo settings modified by ``activate()``."""
    global _active_environment

    if not _active_environment:
        return

    # If any config changes affected spack.store.STORE or spack.repo.PATH, undo them.
    store = getattr(_active_environment, "store_token", None)
    if store is not None:
        spack.store.restore(store)
        delattr(_active_environment, "store_token")

    repo = getattr(_active_environment, "repo_token", None)

    if repo is not None:
        spack.repo.PATH.disable()
        spack.repo.enable_repo(repo)

    _active_environment.manifest.deactivate_config_scope()

    tty.debug(f"Deactivated environment '{_active_environment.name}'")

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
    return valid_env_name(name) and os.path.lexists(os.path.join(_root(name), manifest_name))


def active(name):
    """True if the named environment is active."""
    return _active_environment and name == _active_environment.name


def is_env_dir(path):
    """Whether a directory contains a spack environment."""
    path = substitute_path_variables(path)
    return os.path.isdir(path) and os.path.exists(os.path.join(path, manifest_name))


def as_env_dir(name_or_dir):
    """Translate an environment name or directory to the environment directory"""
    path = substitute_path_variables(name_or_dir)
    if is_env_dir(path):
        return path
    else:
        validate_env_name(name_or_dir)
        if not exists(name_or_dir):
            raise SpackEnvironmentError("no such environment '%s'" % name_or_dir)
        return _root(name_or_dir)


def environment_from_name_or_dir(name_or_dir):
    """Get an environment with the supplied name."""
    return Environment(as_env_dir(name_or_dir))


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
    include_concrete: Optional[List[str]] = None,
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
        include_concrete: concrete environment names/paths to be included
    """
    environment_dir = environment_dir_from_name(name, exists_ok=False)
    return create_in_dir(
        environment_dir,
        init_file=init_file,
        with_view=with_view,
        keep_relative=keep_relative,
        include_concrete=include_concrete,
    )


def create_in_dir(
    root: Union[str, pathlib.Path],
    init_file: Optional[Union[str, pathlib.Path]] = None,
    with_view: Optional[Union[str, pathlib.Path, bool]] = None,
    keep_relative: bool = False,
    include_concrete: Optional[List[str]] = None,
) -> "Environment":
    """Create an environment in the directory passed as input and returns it.

    Files with suffix ``.json`` or ``.lock`` are considered lockfiles. Files with any other name
    are considered manifest files.

    Args:
        root: directory where to create the environment.
        init_file: either a lockfile, a manifest file, an env directory, or None
        with_view: whether a view should be maintained for the environment. If the value is a
            string, it specifies the path to the view
        keep_relative: if True, develop paths are copied verbatim into the new environment file,
            otherwise they are made absolute
        include_concrete: concrete environment names/paths to be included
    """
    # If the initfile is a named environment, get its path
    if init_file and exists(str(init_file)):
        init_file = read(str(init_file)).path
    initialize_environment_dir(root, envfile=init_file)

    if with_view is None and keep_relative:
        return Environment(root)

    try:
        manifest = EnvironmentManifestFile(root)

        if with_view is not None:
            manifest.set_default_view(with_view)

        if include_concrete is not None:
            # Validate included concrete envs
            set_included_envs_to_env_paths(include_concrete)
            validate_included_envs_exists(include_concrete)
            validate_included_envs_concrete(include_concrete)

            # Add unmodified paths to the config
            manifest.set_include_concrete(include_concrete)

        manifest.flush()

    except (spack.config.ConfigFormatError, SpackEnvironmentConfigError) as e:
        shutil.rmtree(root)
        raise e

    env = Environment(root)

    if init_file:
        if os.path.isdir(init_file):
            init_file_dir = init_file
            copied = True
        else:
            init_file_dir = os.path.abspath(os.path.dirname(init_file))
            copied = False

        if not keep_relative:
            if env.path != init_file_dir:
                # If we are here, we are creating an environment based on an
                # spack.yaml file in another directory, and moreover we want
                # dev paths in this environment to refer to their original
                # locations.
                # If the full env was copied including internal files, only rewrite
                # relative paths outside of env
                _rewrite_relative_dev_paths_on_relocation(env, init_file_dir, copied_env=copied)
                _rewrite_relative_repos_paths_on_relocation(env, init_file_dir, copied_env=copied)

    return env


def _rewrite_relative_dev_paths_on_relocation(env, init_file_dir, copied_env=False):
    """When initializing the environment from a manifest file and we plan
    to store the environment in a different directory, we have to rewrite
    relative paths to absolute ones."""
    with env:
        dev_specs = spack.config.get("develop", default={}, scope=env.scope_name)
        if not dev_specs:
            return
        for name, entry in dev_specs.items():
            dev_path = substitute_path_variables(entry["path"])
            expanded_path = spack.config.canonicalize_path(dev_path, default_wd=init_file_dir)

            # Skip if the substituted and expanded path is the same (e.g. when absolute)
            if entry["path"] == expanded_path:
                continue

            # If copied and it's inside the env, we copied it and don't need to relativize
            if copied_env and expanded_path.startswith(init_file_dir):
                continue

            tty.debug("Expanding develop path for {0} to {1}".format(name, expanded_path))

            dev_specs[name]["path"] = expanded_path

        spack.config.set("develop", dev_specs, scope=env.scope_name)

        env._dev_specs = None
        # If we changed the environment's spack.yaml scope, that will not be reflected
        # in the manifest that we read
        env._re_read()


def _rewrite_relative_repos_paths_on_relocation(env, init_file_dir, copied_env=False):
    """When initializing the environment from a manifest file and we plan
    to store the environment in a different directory, we have to rewrite
    relative repo paths to absolute ones and expand environment variables."""
    with env:
        repos_specs = spack.config.get("repos", default={}, scope=env.scope_name)
        if not repos_specs:
            return
        for name, entry in list(repos_specs.items()):
            # only rewrite when we have a path-based repository
            if not isinstance(entry, str):
                continue
            repo_path = substitute_path_variables(entry)
            expanded_path = spack.config.canonicalize_path(repo_path, default_wd=init_file_dir)

            # Skip if the substituted and expanded path is the same (e.g. when absolute)
            if entry == expanded_path:
                continue

            # If copied and it's inside the env, we copied it and don't need to relativize
            if copied_env and expanded_path.startswith(init_file_dir):
                continue

            tty.debug("Expanding repo path for {0} to {1}".format(entry, expanded_path))

            repos_specs[name] = expanded_path

        spack.config.set("repos", repos_specs, scope=env.scope_name)

        env.repos_specs = None
        # If we changed the environment's spack.yaml scope, that will not be reflected
        # in the manifest that we read
        env._re_read()


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


def set_included_envs_to_env_paths(include_concrete: List[str]) -> None:
    """If the included environment(s) is the environment name
    it is replaced by the path to the environment

    Args:
        include_concrete: list of env name or path to env"""

    for i, env_name in enumerate(include_concrete):
        if is_env_dir(env_name):
            include_concrete[i] = env_name
        elif exists(env_name):
            include_concrete[i] = root(env_name)


def validate_included_envs_exists(include_concrete: List[str]) -> None:
    """Checks that all of the included environments exist

    Args:
       include_concrete: list of already existing concrete environments to include

    Raises:
        SpackEnvironmentError: if any of the included environments do not exist
    """

    missing_envs = set()

    for env_name in include_concrete:
        if not is_env_dir(env_name):
            missing_envs.add(env_name)

    if missing_envs:
        msg = "The following environment(s) are missing: {0}".format(", ".join(missing_envs))
        raise SpackEnvironmentError(msg)


def validate_included_envs_concrete(include_concrete: List[str]) -> None:
    """Checks that all of the included environments are concrete

    Args:
        include_concrete: list of already existing concrete environments to include

    Raises:
        SpackEnvironmentError: if any of the included environments are not concrete
    """

    non_concrete_envs = set()

    for env_path in include_concrete:
        if not os.path.exists(os.path.join(as_env_dir(env_path), lockfile_name)):
            non_concrete_envs.add(environment_name(env_path))

    if non_concrete_envs:
        msg = "The following environment(s) are not concrete: {0}\nPlease run:".format(
            ", ".join(non_concrete_envs)
        )
        for env in non_concrete_envs:
            msg += f"\n\t`spack -e {env} concretize`"

        raise SpackEnvironmentError(msg)


def all_environment_names():
    """List the names of environments that currently exist."""
    # just return empty if the env path does not exist.  A read-only
    # operation like list should not try to create a directory.
    if not os.path.exists(env_root_path()):
        return []

    env_root = pathlib.Path(env_root_path()).resolve()

    def yaml_paths():
        for root, dirs, files in os.walk(env_root, topdown=True, followlinks=True):
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".") and not env_root.samefile(os.path.join(root, d))
            ]
            if manifest_name in files:
                yield os.path.join(root, manifest_name)

    names = []
    for yaml_path in yaml_paths():
        candidate = str(pathlib.Path(yaml_path).relative_to(env_root).parent)
        if valid_env_name(candidate):
            names.append(candidate)
    return names


def all_environments():
    """Generator for all managed Environments."""
    for name in all_environment_names():
        yield read(name)


def _read_yaml(str_or_file):
    """Read YAML from a file for round-trip parsing."""
    try:
        data = syaml.load_config(str_or_file)
    except syaml.SpackYAMLError as e:
        raise SpackEnvironmentConfigError(
            f"Invalid environment configuration detected: {e.message}", e.filename
        )

    filename = getattr(str_or_file, "name", None)
    spack.config.validate(data, spack.schema.env.schema, filename)
    return data


def _write_yaml(data, str_or_file):
    """Write YAML to a file preserving comments and dict order."""
    filename = getattr(str_or_file, "name", None)
    spack.config.validate(data, spack.schema.env.schema, filename)
    syaml.dump_config(data, str_or_file, default_flow_style=False)


def _is_dev_spec_and_has_changed(spec):
    """Check if the passed spec is a dev build and whether it has changed since the
    last installation"""
    # First check if this is a dev build and in the process already try to get
    # the dev_path
    if not spec.variants.get("dev_path", None):
        return False

    # Now we can check whether the code changed since the last installation
    if not spec.installed:
        # Not installed -> nothing to compare against
        return False

    # hook so packages can use to write their own method for checking the dev_path
    # use package so attributes about concretization such as variant state can be
    # utilized
    return spec.package.detect_dev_src_change()


class ViewDescriptor:
    def __init__(
        self,
        base_path: str,
        root: str,
        *,
        projections: Optional[Dict[str, str]] = None,
        select: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None,
        link: str = default_view_link,
        link_type: fsv.LinkType = "symlink",
        link_dirs: bool = True,
        groups: Optional[Union[str, List[str]]] = None,
    ) -> None:
        self.base = base_path
        self.raw_root = root
        self.root = spack.config.canonicalize_path(root, default_wd=base_path)
        self.projections = projections or {}
        self.select = select or []
        self.exclude = exclude or []
        self.link_type: fsv.LinkType = fsv.canonicalize_link_type(link_type)
        self.link_dirs: bool = link_type == "symlink" and link_dirs
        self.link = link
        if isinstance(groups, str):
            groups = [groups]
        self.groups: Optional[List[str]] = groups

    def select_fn(self, spec: Spec) -> bool:
        return any(spec.satisfies(s) for s in self.select)

    def exclude_fn(self, spec: Spec) -> bool:
        return not any(spec.satisfies(e) for e in self.exclude)

    def update_root(self, new_path: str) -> None:
        self.raw_root = new_path
        self.root = spack.config.canonicalize_path(new_path, default_wd=self.base)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ViewDescriptor)
            and self.root == other.root
            and self.projections == other.projections
            and self.select == other.select
            and self.exclude == other.exclude
            and self.link == other.link
            and self.link_type == other.link_type
            and self.link_dirs == other.link_dirs
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
            ret["link_type"] = self.link_type
        if self.link_dirs:
            ret["link_dirs"] = self.link_dirs
        if self.link != default_view_link:
            ret["link"] = self.link
        return ret

    @staticmethod
    def from_dict(base_path: str, d) -> "ViewDescriptor":
        return ViewDescriptor(
            base_path,
            d["root"],
            projections=d.get("projections", {}),
            select=d.get("select", []),
            exclude=d.get("exclude", []),
            link=d.get("link", default_view_link),
            link_type=d.get("link_type", "symlink"),
            link_dirs=d.get("link_dirs", True),
            groups=d.get("group", None),
        )

    @property
    def _current_root(self) -> Optional[str]:
        if not islink(self.root):
            return None

        root = readlink(self.root)
        if os.path.isabs(root):
            return root

        root_dir = os.path.dirname(self.root)
        return os.path.join(root_dir, root)

    def _is_up_to_date(self, content_hash: str) -> bool:
        # Old format: self.root is a symlink to ._<basename>/<hash>/
        if os.path.islink(self.root):
            old_root = self._current_root
            if old_root and os.path.basename(old_root) == content_hash:
                return True
        # New format: check the marker file inside the view itself
        try:
            with open(self.marker_path, "r", encoding="utf-8") as f:
                return f.read().strip() == content_hash
        except OSError:
            return False

    @property
    def marker_path(self) -> str:
        return os.path.join(self.root, MARKER_FILE)

    def _ensure_safe_to_replace(self):
        """Prevents Spack from deleting non-Spack owned user directories like /usr/local if users
        accidentally map a view to an existing path."""
        try:
            lstat = os.lstat(self.root)
        except OSError:
            return  # non-existent path is fine to put a view

        if stat.S_ISLNK(lstat.st_mode):
            return  # symlinks are fine to replace
        if stat.S_ISDIR(lstat.st_mode) and (
            os.path.exists(self.marker_path) or not os.listdir(self.root)
        ):
            return  # Spack-owned and empty directories are fine to replace

        raise SpackEnvironmentViewError(
            f"The environment view at {self.root} cannot be updated because it is a non-empty "
            "directory or file not managed by Spack. Please remove it manually to update the view."
        )

    def content_hash(self, specs):
        d = syaml.syaml_dict(
            [
                ("descriptor", self.to_dict()),
                ("specs", [(spec.dag_hash(), spec.prefix) for spec in sorted(specs)]),
            ]
        )
        contents = sjson.dumps(d)
        return spack.util.hash.b32_hash(contents)

    def get_projection_for_spec(self, spec):
        """Get projection for spec. This function does not require the view
        to exist on the filesystem."""
        return self._view(self.root).get_projection_for_spec(spec)

    def view(self) -> fsv.SimpleFilesystemView:
        """
        Returns a view object for the *underlying* view directory. This means that the
        self.root symlink is followed, and that the view has to exist on the filesystem.
        This function is useful when writing to the view.

        Raise if there is no current view.
        """
        if os.path.islink(self.root):
            path: Optional[str] = self._current_root  # old format: follow symlink
        elif os.path.isdir(self.root):
            path = self.root  # new format: use directly
        else:
            path = None
        if not path:
            raise SpackEnvironmentViewError(
                f"Attempting to get nonexistent view from environment. View root is at {self.root}"
            )
        return self._view(path)

    def _view(self, root: str) -> fsv.SimpleFilesystemView:
        """Returns a view object for a given root dir."""
        return fsv.SimpleFilesystemView(
            root,
            spack.store.STORE.layout,
            ignore_conflicts=True,
            projections=self.projections,
            link_type=self.link_type,
            link_dirs=self.link_dirs,
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

    def specs_for_view(self, concrete_roots: List[Spec]) -> List[Spec]:
        """Flatten the DAGs of the concrete roots, keep only unique, selected, and installed specs
        in topological order from root to leaf."""
        if self.link == "all":
            deptype = dt.LINK | dt.RUN
        elif self.link == "run":
            deptype = dt.RUN
        else:
            deptype = dt.NONE

        specs = traverse.traverse_nodes(
            concrete_roots, order="topo", deptype=deptype, key=traverse.by_dag_hash
        )

        # Filter selected, installed specs
        with spack.store.STORE.db.read_transaction():
            result = [s for s in specs if s in self and s.installed]

        return self._exclude_duplicate_runtimes(result)

    def regenerate(self, env: "Environment") -> None:
        if self.groups is None:
            concrete_roots = env.concrete_roots()
        else:
            concrete_roots = [c for g in self.groups for _, c in env.concretized_specs_by(group=g)]

        specs = self.specs_for_view(concrete_roots)
        content_hash = self.content_hash(specs)

        if self._is_up_to_date(content_hash):
            tty.debug(f"View at {self.root} does not need regeneration.")
            return

        self._ensure_safe_to_replace()

        if specs:
            tty.msg(f"Updating view at {self.root}")

        root_parent = os.path.dirname(self.root)
        root_basename = os.path.basename(self.root)
        suffix = uuid.uuid4().hex[:8]
        # Temporary location for the old view in case we need to roll back
        old_root = os.path.join(root_parent, f"{root_basename}.old.{suffix}")

        # The view is built *in place* at self.root: packages bake the projection path
        # (e.g. shebangs, pyvenv.cfg) into file contents, and that path has to be the
        # final view location, not a temporary build directory that's renamed afterwards.
        # To stay able to roll back, move an existing view aside first.
        moved_old = os.path.lexists(self.root)
        if moved_old:
            os.rename(self.root, old_root)

        try:
            fs.mkdirp(self.root)
            self._view(self.root).add_specs(*specs)

            # Claim ownership of the view by dropping a marker file with the content hash.
            with open(self.marker_path, "x", encoding="utf-8") as f:
                f.write(content_hash)

        except Exception as e:
            # Roll back to the previous view (if any).
            shutil.rmtree(self.root, ignore_errors=True)
            if moved_old:
                try:
                    os.rename(old_root, self.root)
                except OSError:
                    pass

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

        if not moved_old:
            return

        # Clean up old view
        if os.path.islink(old_root):
            # Old format: only remove symlink target if it lives inside ._<name>/
            target = os.path.realpath(old_root)
            old_view_container = os.path.join(root_parent, "._%s" % root_basename)
            if target.startswith(old_view_container + os.sep):
                try:
                    shutil.rmtree(target)
                except OSError as exc:
                    tty.warn(f"Failed to remove old view at {target}\n{exc}")
            os.unlink(old_root)
        elif os.path.isdir(old_root):
            try:
                shutil.rmtree(old_root)
            except OSError as exc:
                tty.warn(f"Failed to remove old view at {old_root}\n{exc}")

    def _exclude_duplicate_runtimes(self, specs: List[Spec]) -> List[Spec]:
        """Stably filter out duplicates of "runtime" tagged packages, keeping only latest."""
        # Maps packages tagged "runtime" to the spec with latest version.
        latest: Dict[str, Spec] = {}
        for s in specs:
            if "runtime" not in getattr(s.package, "tags", ()):
                continue
            elif s.name not in latest or latest[s.name].version < s.version:
                latest[s.name] = s

        return [x for x in specs if x.name not in latest or latest[x.name] is x]


def env_subdir_path(manifest_dir: Union[str, pathlib.Path]) -> str:
    """Path to where the environment stores repos, logs, views, configs.

    Args:
        manifest_dir:  directory containing the environment manifest file

    Returns:  directory the environment uses to manage its files
    """
    return os.path.join(str(manifest_dir), env_subdir_name)


class ConcretizedRootInfo:
    """Data on root specs that have been concretized"""

    __slots__ = ("root", "hash", "new", "group")

    def __init__(
        self, *, root_spec: spack.spec.Spec, root_hash: str, new: bool = False, group: str
    ):
        self.root = root_spec
        self.hash = root_hash
        self.new = new
        self.group = group

    def __str__(self):
        return f"{self.root} -> {self.hash} [new={self.new}]"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ConcretizedRootInfo)
            and self.root == other.root
            and self.hash == other.hash
            and self.new == other.new
            and self.group == other.group
        )

    def __hash__(self) -> int:
        return hash((self.root, self.hash, self.new, self.group))

    @staticmethod
    def from_info_dict(info_dict: Dict[str, str]) -> "ConcretizedRootInfo":
        # Lockfile versions < 7 don't have the "group" attribute
        return ConcretizedRootInfo(
            root_spec=Spec(info_dict["spec"]),
            root_hash=info_dict["hash"],
            new=False,
            group=info_dict.get("group", DEFAULT_USER_SPEC_GROUP),
        )


class Environment:
    """A Spack environment, which bundles together configuration and a list of specs."""

    def __init__(self, manifest_dir: Union[str, pathlib.Path]) -> None:
        """An environment can be constructed from a directory containing a "spack.yaml" file, and
        optionally a consistent "spack.lock" file.

        Args:
            manifest_dir: directory with the "spack.yaml" associated with the environment
        """
        self.path = os.path.abspath(str(manifest_dir))
        self.name = environment_name(self.path)
        self.env_subdir_path = env_subdir_path(self.path)

        self.txlock = lk.Lock(self._transaction_lock_path)

        self._unify = None
        self.views: Dict[str, ViewDescriptor] = {}

        #: Parser for spec lists
        self._spec_lists_parser = SpecListParser()
        #: Specs from "spack.yaml"
        self.spec_lists: Dict[str, SpecList] = {}
        #: Information on concretized roots
        self.concretized_roots: List[ConcretizedRootInfo] = []
        #: Concretized specs by hash
        self.specs_by_hash: Dict[str, Spec] = {}
        #: Repository for this environment (memoized)
        self._repo = None

        #: Environment root dirs for concrete (lockfile) included environments
        self.included_concrete_env_root_dirs: List[str] = []
        #: First-level included concretized spec data from/to the lockfile.
        self.included_concrete_spec_data: Dict[str, Dict[str, List[str]]] = {}
        #: Roots from included environments from the last concretization, keyed by env path
        self.included_concretized_roots: Dict[str, List[ConcretizedRootInfo]] = {}
        #: Concretized specs by hash from the included environments
        self.included_specs_by_hash: Dict[str, Dict[str, Spec]] = {}

        #: Previously active environment
        self._previous_active = None
        self._dev_specs = None

        # Load the manifest file contents into memory
        self._load_manifest_file()

    def _load_manifest_file(self):
        """Instantiate and load the manifest file contents into memory."""
        with lk.ReadTransaction(self.txlock):
            self.manifest = EnvironmentManifestFile(self.path, self.name)
            with self.manifest.use_config():
                self._read()

    @contextlib.contextmanager
    def config_override_for_group(self, *, group: str):
        key = self.manifest._ensure_group_exists(group=group)
        internal_scope = self.manifest.config_override(group=key)
        if internal_scope is None:
            # No internal scope
            tty.debug(
                f"[{__name__}] No configuration override necessary for the '{group}' group "
                f"in the environment at {self.manifest_path}"
            )
            yield
            return

        try:
            tty.debug(
                f"[{__name__}] Overriding the configuration for the '{group}' group defined "
                f"in {self.manifest_path} before concretization"
            )
            spack.config.CONFIG.push_scope(
                internal_scope, priority=ConfigScopePriority.ENVIRONMENT_SPEC_GROUPS
            )
            yield
        finally:
            spack.config.CONFIG.remove_scope(internal_scope.name)

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("txlock", None)
        state.pop("_repo", None)
        state.pop("repo_token", None)
        state.pop("store_token", None)
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.txlock = lk.Lock(self._transaction_lock_path)
        self._repo = None

    def _re_read(self):
        """Reinitialize the environment object."""
        self.clear()
        self._load_manifest_file()

    def _read(self):
        self._construct_state_from_manifest()

        if os.path.exists(self.lock_path):
            with open(self.lock_path, encoding="utf-8") as f:
                read_lock_version = self._read_lockfile(f)["_meta"]["lockfile-version"]

            if read_lock_version == 1:
                tty.debug(f"Storing backup of {self.lock_path} at {self._lock_backup_v1_path}")
                shutil.copy(self.lock_path, self._lock_backup_v1_path)

    def write_transaction(self):
        """Get a write lock context manager for use in a ``with`` block."""
        return lk.WriteTransaction(self.txlock, acquire=self._re_read)

    def _process_view(self, env_view: Optional[Union[bool, str, Dict]]):
        """Process view option(s), which can be boolean, string, or None.

        A boolean environment view option takes precedence over any that may
        be included. So ``view: True`` results in the default view only. And
        ``view: False`` means the environment will have no view.

        Args:
            env_view: view option provided in the manifest or configuration
        """

        def add_view(name, values):
            """Add the view with the name and the string or dict values."""
            if isinstance(values, str):
                self.views[name] = ViewDescriptor(self.path, values)
            elif isinstance(values, dict):
                self.views[name] = ViewDescriptor.from_dict(self.path, values)
            else:
                tty.error(f"Cannot add view named {name} for {type(values)} values {values}")

        # If the configuration specifies 'view: False' then we are done
        # processing views. If this is called with the environment's view
        # view (versus an included view), then there are to be NO views.
        if env_view is False:
            return

        # If the configuration specifies 'view: True' then only the default
        # view will be created for the environment and we are done processing
        # views.
        if env_view is True:
            add_view(default_view_name, self.view_path_default)
            return

        # Otherwise, the configuration has a subdirectory or dictionary.
        if isinstance(env_view, str):
            add_view(default_view_name, env_view)
        elif env_view:
            for name, values in env_view.items():
                add_view(name, values)

        # If we reach this point without an explicit view option then we
        # provide the default view.
        if self.views == dict():
            self.views[default_view_name] = ViewDescriptor(self.path, self.view_path_default)

    def _load_concrete_include_data(self):
        """Load concrete include specs data from included concrete directories."""
        if self.included_concrete_env_root_dirs:
            if os.path.exists(self.lock_path):
                with open(self.lock_path, encoding="utf-8") as f:
                    data = self._read_lockfile(f)

                if lockfile_include_key in data:
                    self.included_concrete_spec_data = data[lockfile_include_key]
            else:
                self.include_concrete_envs()

    def _process_included_lockfiles(self):
        """Extract and load into memory included lock file data."""
        includes = self.manifest[TOP_LEVEL_KEY].get(lockfile_include_key, [])
        if includes:
            tty.warn(
                f"Use of '{lockfile_include_key}' in manifest files "
                f"is deprecated. The key should be '{manifest_include_name}' "
                f"and the path should end with '{lockfile_name}'. Run "
                f"'spack env update {self.name}' to update the manifest."
            )
            includes = [os.path.join(inc, lockfile_name) for inc in includes]
        includes += self.manifest[TOP_LEVEL_KEY].get(manifest_include_name, [])
        if not includes:
            return

        # Expand config and environment variables for concrete environments,
        # indicated by the inclusion of lock files.
        self.included_concrete_env_root_dirs = []

        for entry in includes:
            include = spack.config.included_path(entry)
            if isinstance(include, spack.config.GitIncludePaths):
                # Git includes must be cloned first; paths are relative to the
                # clone destination, not to the manifest directory.
                destination = include._clone(self.manifest.env_config_scope)
                if destination is None:
                    continue
                resolved = [os.path.join(destination, p) for p in include.paths]
            else:
                resolved = [
                    spack.config.canonicalize_path(p, default_wd=self.path) for p in include.paths
                ]

            for path in resolved:
                if os.path.basename(path) != lockfile_name:
                    continue

                tty.debug(f"Adding {path} to the concrete environment root directories")
                self.included_concrete_env_root_dirs.append(os.path.dirname(path))

        # Cache concrete environments for required lock files.
        self._load_concrete_include_data()

    def _construct_state_from_manifest(self):
        """Set up user specs and views from the manifest file."""
        self.views = {}
        self._sync_speclists()
        self._process_view(spack.config.get("view", True))
        self._process_included_lockfiles()

    def _sync_speclists(self):
        self._spec_lists_parser = SpecListParser(
            toolchains=spack.config.CONFIG.get("toolchains", {})
        )
        self.spec_lists = {}
        self.spec_lists.update(
            self._spec_lists_parser.parse_definitions(
                data=spack.config.CONFIG.get("definitions", [])
            )
        )
        for group in self.manifest.groups():
            tty.debug(f"[{__name__}]: Synchronizing user specs from the '{group}' group", level=2)
            key = self._user_specs_key(group=group)
            self.spec_lists[key] = self._spec_lists_parser.parse_user_specs(
                name=key, yaml_list=self.manifest.user_specs(group=group)
            )

    def _user_specs_key(self, *, group: Optional[str] = None) -> str:
        if group is None or group == DEFAULT_USER_SPEC_GROUP:
            return USER_SPECS_KEY
        return f"{USER_SPECS_KEY}:{group}"

    @property
    def user_specs(self) -> SpecList:
        return self.user_specs_by(group=DEFAULT_USER_SPEC_GROUP)

    def user_specs_by(self, *, group: Optional[str]) -> SpecList:
        """Returns a dictionary of user specs keyed by their group."""
        key = self._user_specs_key(group=group)
        return self.spec_lists[key]

    def explicit_roots(self):
        for x in self.concretized_roots:
            if self.manifest.is_explicit(group=x.group):
                yield x

    @property
    def dev_specs(self):
        dev_specs = {}
        dev_config = spack.config.get("develop", {})
        for name, entry in dev_config.items():
            local_entry = {"spec": str(entry["spec"])}
            # default path is the spec name
            if "path" not in entry:
                local_entry["path"] = name
            else:
                local_entry["path"] = entry["path"]
            dev_specs[name] = local_entry
        return dev_specs

    @property
    def included_user_specs(self) -> SpecList:
        """Included concrete user (or root) specs from last concretization."""
        spec_list = SpecList()

        if not self.included_concrete_env_root_dirs:
            return spec_list

        def add_root_specs(included_concrete_specs):
            # add specs from the include *and* any nested includes it may have
            for env, info in included_concrete_specs.items():
                for root_list in info["roots"]:
                    spec_list.add(root_list["spec"])

                if lockfile_include_key in info:
                    add_root_specs(info[lockfile_include_key])

        add_root_specs(self.included_concrete_spec_data)
        return spec_list

    def clear(self):
        """Clear the contents of the environment"""
        self.spec_lists = {}
        self._dev_specs = {}
        self.concretized_roots = []
        self.specs_by_hash = {}  # concretized specs by hash

        self.included_concrete_spec_data = {}  # concretized specs from lockfile of included envs
        self.included_concretized_roots = {}  # root specs of the included envs, keyed by env path
        self.included_specs_by_hash = {}  # concretized specs by hash from the included envs

        self.invalidate_repository_cache()
        self._previous_active = None  # previously active environment

        self.manifest.clear()

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
    def repos_path(self):
        return os.path.join(self.env_subdir_path, "repos")

    @property
    def view_path_default(self) -> str:
        # default path for environment views
        return os.path.join(self.env_subdir_path, "view")

    @property
    def repo(self):
        if self._repo is None:
            self._repo = make_repo_path(self.repos_path)
        return self._repo

    @property
    def scope_name(self):
        """Name of the config scope of this environment's manifest file."""
        return self.manifest.scope_name

    def include_concrete_envs(self):
        """Copy and save the included environments' specs internally."""

        root_hash_seen = set()
        concrete_hash_seen = set()
        self.included_concrete_spec_data = {}

        for env_path in self.included_concrete_env_root_dirs:
            # Check that the environment (lockfile) exists
            if not is_env_dir(env_path):
                raise SpackEnvironmentError(f"Unable to find env at {env_path}")

            env = Environment(env_path)
            self.included_concrete_spec_data[env_path] = {"roots": [], "concrete_specs": {}}

            # Copy unique root specs from env
            for root_dict in env._concrete_roots_dict():
                if root_dict["hash"] not in root_hash_seen:
                    self.included_concrete_spec_data[env_path]["roots"].append(root_dict)
                    root_hash_seen.add(root_dict["hash"])

            # Copy unique concrete specs from env
            for dag_hash, spec_details in env._concrete_specs_dict().items():
                if dag_hash not in concrete_hash_seen:
                    self.included_concrete_spec_data[env_path]["concrete_specs"].update(
                        {dag_hash: spec_details}
                    )
                    concrete_hash_seen.add(dag_hash)

            # Copy transitive include data
            transitive = env.included_concrete_spec_data
            if transitive:
                self.included_concrete_spec_data[env_path][lockfile_include_key] = transitive

        self.unify_specs()
        self.write()

    def destroy(self):
        """Remove this environment from Spack entirely."""
        shutil.rmtree(self.path)

    def add(self, user_spec, list_name=USER_SPECS_KEY) -> bool:
        """Add a single user_spec (non-concretized) to the Environment

        Returns:
            True if the spec was added, False if it was already present and did not need to be
            added

        """
        spec = Spec(user_spec)

        if list_name not in self.spec_lists:
            raise SpackEnvironmentError(f"No list {list_name} exists in environment {self.name}")

        if list_name == USER_SPECS_KEY:
            if spec.anonymous:
                raise SpackEnvironmentError("cannot add anonymous specs to an environment")
            elif not spack.repo.PATH.exists(spec.name) and not spec.abstract_hash:
                virtuals = spack.repo.PATH.provider_index.providers.keys()
                if spec.name not in virtuals:
                    raise SpackEnvironmentError(f"no such package: {spec.name}")

        list_to_change = self.spec_lists[list_name]
        existing = str(spec) in list_to_change.yaml_list
        if not existing:
            list_to_change.add(spec)
            if list_name == USER_SPECS_KEY:
                self.manifest.add_user_spec(str(user_spec))
            else:
                self.manifest.add_definition(str(user_spec), list_name=list_name)
            self._sync_speclists()

        return bool(not existing)

    def change_existing_spec(
        self,
        change_spec: Spec,
        list_name: str = USER_SPECS_KEY,
        match_spec: Optional[Spec] = None,
        allow_changing_multiple_specs=False,
    ):
        """
        Find the spec identified by ``match_spec`` and change it to ``change_spec``.

        Arguments:
            change_spec: defines the spec properties that
                need to be changed. This will not change attributes of the
                matched spec unless they conflict with ``change_spec``.
            list_name: identifies the spec list in the environment that
                should be modified
            match_spec: if set, this identifies the spec
                that should be changed. If not set, it is assumed we are
                looking for a spec with the same name as ``change_spec``.
        """
        if not (change_spec.name or match_spec):
            raise ValueError(
                "Must specify a spec name or match spec to identify a single spec"
                " in the environment that will be changed (or multiple with '--all')"
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
            raise ValueError(f"{str(match_spec)} matches multiple specs")

        for idx, spec in matches:
            override_spec = Spec.override(spec, change_spec)
            if list_name == USER_SPECS_KEY:
                self.manifest.override_user_spec(str(override_spec), idx=idx)
            else:
                self.manifest.override_definition(
                    str(spec), override=str(override_spec), list_name=list_name
                )
        self._sync_speclists()

    def remove(self, query_spec, list_name=USER_SPECS_KEY, force=False):
        """Remove specs from an environment that match a query_spec"""
        err_msg_header = (
            f"Cannot remove '{query_spec}' from '{list_name}' definition "
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
            # concrete specs match against concrete specs in the env by dag hash.
            matches = [x.root for x in self.concretized_roots if query_spec.dag_hash() == x.hash]

        if not matches:
            raise SpackEnvironmentError(f"{err_msg_header}, no spec matches")

        old_specs = set(self.user_specs)

        # Remove specs from the appropriate spec list
        for spec in matches:
            if spec not in list_to_change:
                continue
            try:
                list_to_change.remove(spec)
            except SpecListError as e:
                msg = str(e)
                if force:
                    msg += " It will be removed from the concrete specs."
                tty.warn(msg)
            else:
                if list_name == USER_SPECS_KEY:
                    self.manifest.remove_user_spec(str(spec))
                else:
                    self.manifest.remove_definition(str(spec), list_name=list_name)

        # Recompute "definitions" and user specs
        self._sync_speclists()
        new_specs = set(self.user_specs)

        # If 'force', update stale concretized specs
        if force:
            stale_specs = old_specs - new_specs
            self.concretized_roots, removed = stable_partition(
                self.concretized_roots, lambda x: x.root not in stale_specs
            )
            for x in removed:
                del self.specs_by_hash[x.hash]

    def is_develop(self, spec):
        """Returns true when the spec is built from local sources"""
        return spec.name in self.dev_specs

    def apply_develop(self, specs: List[spack.spec.Spec], paths: Optional[List[str]] = None):
        """Mutate concrete specs to include dev_path provenance pointing to path.

        This will fail if any existing concrete spec for the same package does not satisfy the

        given develop spec."""
        selectors = []
        mutators = []
        msgs = []

        assert not paths or len(specs) == len(paths)
        for spec, path in zip_longest(specs, paths or [], fillvalue=None):
            assert spec
            selector = spack.spec.Spec(spec.name)

            mutator = spack.spec.Spec()
            if path:
                variant = vt.SingleValuedVariant("dev_path", path)
            else:
                variant = vt.VariantValueRemoval("dev_path")
            mutator.variants["dev_path"] = variant

            msg = (
                f"Develop spec '{spec}' conflicts with concrete specs in environment."
                " Try again with 'spack develop --no-modify-concrete-specs'"
                " and run 'spack concretize --force' to apply your changes."
            )
            selectors.append(selector)
            mutators.append(mutator)
            msgs.append(msg)

        self.mutate(selectors, mutators, validators=specs, msgs=msgs)

    def mutate(
        self,
        selectors: List[spack.spec.Spec],
        mutators: List[spack.spec.Spec],
        validators: Optional[List[spack.spec.Spec]] = None,
        msgs: Optional[List[str]] = None,
    ):
        """Mutate concrete specs of an environment

        Mutate any spec that matches ``selector``. Invalidate caches on parents of mutated specs.
        If a validator spec is supplied, throw an error if a selected spec does not satisfy the
        validator.
        """
        # Find all specs that this mutation applies to
        modify_specs = []
        modified_specs = []
        if len(selectors) != len(mutators):
            raise ValueError(
                f"Length mismatch: selectors ({len(selectors)}) != mutators ({len(mutators)})"
            )

        if validators and len(validators) != len(selectors):
            raise ValueError(
                f"Length mismatch: validators ({len(validators)}) != selectors ({len(selectors)})"
            )

        if msgs and len(msgs) != len(selectors):
            raise ValueError(
                f"Length mismatch: msgs ({len(msgs)}) != selectors ({len(selectors)})"
            )

        for dep in self.all_specs_generator():
            for selector, mutator, validator, msg in zip_longest(
                selectors, mutators, validators or [], msgs or [], fillvalue=None
            ):
                assert selector
                assert mutator
                if dep.satisfies(selector):
                    if not dep.satisfies(validator or selector):
                        if not msg:
                            msg = f"spec {dep} satisfies selector {selector}"
                            msg += f" but not validator {validator}"
                        raise SpackEnvironmentDevelopError(msg)
                    modify_specs.append((dep, mutator))

        # Manipulate selected specs
        for s, mutator in modify_specs:
            modified = s.mutate(mutator, rehash=False)
            if modified:
                modified_specs.append(s)

        # Identify roots modified and invalidate all dependent hashes
        modified_roots = []
        for parent in traverse.traverse_nodes(modified_specs, direction="parents"):
            # record whether this parent is a root before we modify the hash
            if parent.dag_hash() in self.specs_by_hash:
                modified_roots.append((parent, parent.dag_hash()))
            # modify the parent to invalidate hashes
            parent._mark_root_concrete(False)
            parent.clear_caches()

        # Compute new hashes and update the env list of specs
        hash_mutations = {}
        for root, old_hash in modified_roots:
            # New hash must be computed after we finalize concretization
            root._finalize_concretization()
            new_hash = root.dag_hash()
            self.specs_by_hash.pop(old_hash)
            self.specs_by_hash[new_hash] = root
            hash_mutations[old_hash] = new_hash

        for x in self.concretized_roots:
            if x.hash in hash_mutations:
                x.hash = hash_mutations[x.hash]

        if modified_roots:
            self.write()

    def concretize(
        self, *, force: Optional[bool] = None, tests: Union[bool, Sequence[str]] = False
    ) -> Sequence[SpecPair]:
        """Concretize user_specs in this environment.

        Only concretizes specs that haven't been concretized yet unless force is ``True``.

        This only modifies the environment in memory. ``write()`` will write out a lockfile
        containing concretized specs.

        Arguments:
            force: re-concretize ALL specs, even those that were already concretized;
                defaults to ``spack.config.get("concretizer:force")``
            tests: False to run no tests, True to test all packages, or a list of
                package names to run tests for some

        Returns:
            List of specs that have been concretized. Each entry is a tuple of
            the user spec and the corresponding concretized spec.
        """
        old_concretized_roots = self.concretized_roots[:]
        old_specs_by_hash = self.specs_by_hash.copy()

        # This is slightly complicated to pass by value the correct portion of the way
        # down the stack
        old_concrete_data = {
            env_name: env_data.copy()
            for env_name, env_data in self.included_concrete_spec_data.items()
        }
        old_included_by_hash = {
            env_name: env_by_hash.copy()
            for env_name, env_by_hash in self.included_specs_by_hash.items()
        }

        try:
            return EnvironmentConcretizer(self).concretize(force=force, tests=tests)
        except BaseException:
            self.concretized_roots = old_concretized_roots
            self.specs_by_hash = old_specs_by_hash
            self.included_specs_by_hash = old_included_by_hash
            self.included_concrete_spec_data = old_concrete_data
            raise

    def sync_concretized_specs(self) -> None:
        """Removes concrete specs that no longer correlate to a user spec"""
        if not self.concretized_roots:
            return

        to_deconcretize, user_specs = [], self._all_user_specs_with_group()
        for x in self.concretized_roots:
            if (x.group, x.root) not in user_specs:
                to_deconcretize.append(x)
        for x in to_deconcretize:
            self.deconcretize_by_user_spec(x.root, group=x.group)

    def _all_user_specs_with_group(self) -> Set[Tuple[str, Spec]]:
        result = set()
        for group in self.manifest.groups():
            result.update([(group, x) for x in self.user_specs_by(group=group)])
        return result

    def clear_concretized_specs(self) -> None:
        """Clears the currently concretized specs"""
        self.concretized_roots = []
        self.specs_by_hash = {}

    def deconcretize_by_hash(self, dag_hash: str) -> None:
        """Removes a concrete spec from the environment concretization"""
        self.concretized_roots = [x for x in self.concretized_roots if x.hash != dag_hash]
        self._maybe_remove_dag_hash(dag_hash)

    def deconcretize_by_user_spec(
        self, spec: spack.spec.Spec, *, group: Optional[str] = None
    ) -> None:
        """Removes a user spec from the environment concretization

        Arguments:
            spec: user spec to deconcretize
            group: group of the spec to remove. If not specified, the spec is removed from
                the default group
        """
        group = group or DEFAULT_USER_SPEC_GROUP
        # spec has to be a root of the environment
        discarded, self.concretized_roots = stable_partition(
            self.concretized_roots, lambda x: x.group == group and x.root == spec
        )
        assert len({x.hash for x in discarded}) == 1, (
            "More than one hash associated with a single user spec"
        )
        dag_hash = discarded[0].hash
        self._maybe_remove_dag_hash(dag_hash)

    def _maybe_remove_dag_hash(self, dag_hash: str):
        # If this was the only user spec that concretized to this concrete spec, remove it
        if not self.user_spec_with_hash(dag_hash) and dag_hash in self.specs_by_hash:
            # if we deconcretized a dependency that doesn't correspond to a root, it won't be here.
            del self.specs_by_hash[dag_hash]

    def user_spec_with_hash(self, dag_hash: str) -> bool:
        """Returns True if any user spec is associated with a concrete spec with the given hash"""
        return any(x.hash == dag_hash for x in self.concretized_roots)

    def unify_specs(self) -> None:
        # Keep the information on new specs by copying the concretized roots
        old_concretized_roots = self.concretized_roots
        self._read_lockfile_dict(self._to_lockfile_dict())
        self.concretized_roots = old_concretized_roots

    @property
    def default_view(self):
        if not self.has_view(default_view_name):
            raise SpackEnvironmentError(f"{self.name} does not have a default view enabled")

        return self.views[default_view_name]

    def has_view(self, view_name: str) -> bool:
        return view_name in self.views

    def update_default_view(self, path_or_bool: Union[str, bool]) -> None:
        """Updates the path of the default view.

        If the argument passed as input is False the default view is deleted, if present. The
        manifest will have an entry ``view: false``.

        If the argument passed as input is True a default view is created, if not already present.
        The manifest will have an entry ``view: true``. If a default view is already declared, it
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
            assert isinstance(view_path, str), f"expected str for 'view_path', but got {view_path}"
            self.views[default_view_name] = ViewDescriptor(self.path, view_path)

        self.manifest.set_default_view(self._default_view_as_yaml())

    def delete_default_view(self) -> None:
        """Deletes the default view associated with this environment."""
        if default_view_name not in self.views:
            return

        view_path = pathlib.Path(self.default_view.root)
        try:
            if view_path.is_symlink():
                shutil.rmtree(view_path.resolve())  # old format: remove hash dir
                view_path.unlink()
            else:
                shutil.rmtree(view_path)  # new format: remove real dir
        except FileNotFoundError as e:
            tty.debug(f"[ENVIRONMENT] error trying to delete the default view: {e}")

    def regenerate_views(self):
        if not self.views:
            tty.debug("Skip view update, this environment does not maintain a view")
            return

        for view in self.views.values():
            view.regenerate(self)

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

    def _env_modifications_for_view(
        self, view: ViewDescriptor, reverse: bool = False
    ) -> spack.util.environment.EnvironmentModifications:
        try:
            with spack.store.STORE.db.read_transaction():
                installed_roots = [s for s in self.concrete_roots() if s.installed]
            mods = uenv.environment_modifications_for_specs(*installed_roots, view=view)
        except Exception as e:
            # Failing to setup spec-specific changes shouldn't be a hard error.
            tty.warn(
                f"could not {'unload' if reverse else 'load'} runtime environment due "
                f"to {e.__class__.__name__}: {e}"
            )
            return spack.util.environment.EnvironmentModifications()
        return mods.reversed() if reverse else mods

    def add_view_to_env(
        self, env_mod: spack.util.environment.EnvironmentModifications, view: str
    ) -> spack.util.environment.EnvironmentModifications:
        """Collect the environment modifications to activate an environment using the provided
        view. Removes duplicate paths.

        Args:
            env_mod: the environment modifications object that is modified.
            view: the name of the view to activate."""
        descriptor = self.views.get(view)
        if not descriptor:
            return env_mod

        env_mod.extend(uenv.unconditional_environment_modifications(descriptor))
        env_mod.extend(self._env_modifications_for_view(descriptor))

        # deduplicate paths from specs mapped to the same location
        for env_var in env_mod.group_by_name():
            env_mod.prune_duplicate_paths(env_var)

        return env_mod

    def rm_view_from_env(
        self, env_mod: spack.util.environment.EnvironmentModifications, view: str
    ) -> spack.util.environment.EnvironmentModifications:
        """Collect the environment modifications to deactivate an environment using the provided
        view. Reverses the action of ``add_view_to_env``.

        Args:
            env_mod: the environment modifications object that is modified.
            view: the name of the view to deactivate."""
        descriptor = self.views.get(view)
        if not descriptor:
            return env_mod

        env_mod.extend(uenv.unconditional_environment_modifications(descriptor).reversed())
        env_mod.extend(self._env_modifications_for_view(descriptor, reverse=True))

        return env_mod

    def add_concrete_spec(
        self,
        spec: spack.spec.Spec,
        concrete: spack.spec.Spec,
        *,
        new: bool = True,
        group: Optional[str] = None,
    ):
        """Called when a new concretized spec is added to the environment.

        This ensures that all internal data structures are kept in sync.

        Arguments:
            spec: user spec that resulted in the concrete spec
            concrete: spec concretized within this environment
            new: whether to write this spec's package to the env repo on write()
        """
        assert concrete.concrete
        h = concrete.dag_hash()
        group = group or DEFAULT_USER_SPEC_GROUP
        self.concretized_roots.append(
            ConcretizedRootInfo(root_spec=spec, root_hash=h, new=new, group=group)
        )
        self.specs_by_hash[h] = concrete

    def _dev_specs_that_need_overwrite(self):
        """Return the hashes of all specs that need to be reinstalled due to source code change."""
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

    def _partition_roots_by_install_status(self):
        """Partition root specs into those that do not have to be passed to the
        installer, and those that should be, taking into account development
        specs. This is done in a single read transaction per environment instead
        of per spec."""
        with spack.store.STORE.db.read_transaction():
            uninstalled, installed = stable_partition(self.concrete_roots(), _is_uninstalled)
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

    def install_specs(self, specs: Optional[List[Spec]] = None, **install_args):
        roots = self.concrete_roots()
        specs = specs if specs is not None else roots

        # Extract reporter arguments
        reporter = install_args.pop("reporter", None)
        report_file = install_args.pop("report_file", None)

        # Extend the set of specs to overwrite with modified dev specs and their parents
        install_args["overwrite"] = {
            *install_args.get("overwrite", ()),
            *self._dev_specs_that_need_overwrite(),
        }

        # Only environment roots in explicit groups are marked explicit
        install_args["explicit"] = {
            *install_args.get("explicit", ()),
            *(x.hash for x in self.explicit_roots()),
        }

        builder = spack.installer_dispatch.create_installer(
            [spec.package for spec in specs], create_reports=reporter is not None, **install_args
        )

        try:
            builder.install()
        finally:
            if reporter:
                if isinstance(builder.reports, dict):
                    reporter.build_report(report_file, list(builder.reports.values()))
                elif isinstance(builder.reports, list):
                    reporter.build_report(report_file, builder.reports)
                else:
                    raise TypeError("builder.reports must be either a dictionary or a list")

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
        ``spack.yaml``.
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
        for x in self.concretized_roots:
            yield x.root, self.specs_by_hash[x.hash]

        yield from self.concretized_specs_from_all_included_environments()

    def concretized_specs_from_all_included_environments(self):
        seen = {(x.root, x.hash) for x in self.concretized_roots}
        for included_env in self.included_concretized_roots:
            yield from self.concretized_specs_from_included_environment(included_env, _seen=seen)

    def concretized_specs_from_included_environment(
        self, included_env: str, *, _seen: Optional[Set[Tuple[spack.spec.Spec, str]]] = None
    ):
        _seen = set() if _seen is None else _seen
        for x in self.included_concretized_roots[included_env]:
            if (x.root, x.hash) in _seen:
                continue
            _seen.add((x.root, x.hash))
            yield x.root, self.included_specs_by_hash[included_env][x.hash]

    def concrete_roots(self):
        """Same as concretized_specs, except it returns the list of concrete
        roots *without* associated user spec"""
        return [root for _, root in self.concretized_specs()]

    def concretized_specs_by(self, *, group: str) -> Iterable[Tuple[Spec, Spec]]:
        """Generates all the (abstract, concrete) spec pairs for a given group"""
        for x in self.concretized_roots:
            if x.group != group:
                continue
            yield x.root, self.specs_by_hash[x.hash]

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
        but must be concrete (specs added with ``spack add`` without an
        intervening ``spack concretize`` will not be matched).

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
        removed on next concretize."""
        needed = set()
        for s, c in self.concretized_specs():
            if s in self.user_specs:
                for d in c.traverse():
                    needed.add(d)

        for s, c in self.concretized_specs():
            for d in c.traverse():
                if d not in needed:
                    yield d

    def _concrete_specs_dict(self):
        concrete_specs = {}
        for s in traverse.traverse_nodes(self.specs_by_hash.values(), key=traverse.by_dag_hash):
            spec_dict = s.node_dict_with_hashes(hash=ht.dag_hash)
            # Assumes no legacy formats, since this was just created.
            spec_dict[ht.dag_hash.name] = s.dag_hash()
            concrete_specs[s.dag_hash()] = spec_dict

            if s.build_spec is not s:
                for d in s.build_spec.traverse():
                    build_spec_dict = d.node_dict_with_hashes(hash=ht.dag_hash)
                    build_spec_dict[ht.dag_hash.name] = d.dag_hash()
                    concrete_specs[d.dag_hash()] = build_spec_dict

        return concrete_specs

    def _concrete_roots_dict(self):
        if not self.has_groups():
            return [{"hash": x.hash, "spec": str(x.root)} for x in self.concretized_roots]

        return [
            {"hash": x.hash, "spec": str(x.root), "group": x.group} for x in self.concretized_roots
        ]

    def has_groups(self) -> bool:
        groups = self.manifest.groups()
        # True if groups != {DEFAULT_USER_SPEC_GROUP}
        return len(groups) != 1 or DEFAULT_USER_SPEC_GROUP not in groups

    def _to_lockfile_dict(self):
        """Create a dictionary to store a lockfile for this environment."""
        lockfile_version = CURRENT_LOCKFILE_VERSION if self.has_groups() else 6
        concrete_specs = self._concrete_specs_dict()
        root_specs = self._concrete_roots_dict()

        spack_dict = {"version": spack.spack_version}
        spack_commit = spack.get_spack_commit()
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
                "lockfile-version": lockfile_version,
                "specfile-version": spack.spec.SPECFILE_FORMAT_VERSION,
            },
            # spack version information
            "spack": spack_dict,
            # users specs + hashes are the 'roots' of the environment
            "roots": root_specs,
            # Concrete specs by hash, including dependencies
            "concrete_specs": concrete_specs,
        }

        if self.included_concrete_env_root_dirs:
            data[lockfile_include_key] = self.included_concrete_spec_data

        return data

    def _read_lockfile(self, file_or_json):
        """Read a lockfile from a file or from a raw string."""
        lockfile_dict = sjson.load(file_or_json)
        self._read_lockfile_dict(lockfile_dict)
        return lockfile_dict

    def _set_included_env_roots(
        self,
        env_name: str,
        env_info: Dict[str, Dict[str, Any]],
        included_json_specs_by_hash: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Dict[str, Any]]:
        """Populates included_concretized_roots from included environment data,
        including any transitively nested included environments.

        Args:
           env_name: the path of the included environment
           env_info: included concrete environment data
           included_json_specs_by_hash: concrete spec data keyed by hash

        Returns: updated specs_by_hash
        """
        self.included_concretized_roots[env_name] = []

        def add_specs(name, info, specs_by_hash):
            # Add specs from the environment as well as any of its nested
            # environments.
            for root_info in info["roots"]:
                self.included_concretized_roots[name].append(
                    ConcretizedRootInfo.from_info_dict(root_info)
                )
            if "concrete_specs" in info:
                specs_by_hash.update(info["concrete_specs"])

            if lockfile_include_key in info:
                for included_name, included_info in info[lockfile_include_key].items():
                    if included_name not in self.included_concretized_roots:
                        self.included_concretized_roots[included_name] = []
                    add_specs(included_name, included_info, specs_by_hash)

        add_specs(env_name, env_info, included_json_specs_by_hash)
        return included_json_specs_by_hash

    def _read_lockfile_dict(self, d):
        """Read a lockfile dictionary into this environment."""
        self.specs_by_hash = {}
        self.included_specs_by_hash = {}
        self.included_concretized_roots = {}

        roots = d["roots"]
        self.concretized_roots = [ConcretizedRootInfo.from_info_dict(r) for r in roots]

        json_specs_by_hash = d["concrete_specs"]
        included_json_specs_by_hash = {}

        if lockfile_include_key in d:
            for env_name, env_info in d[lockfile_include_key].items():
                included_json_specs_by_hash.update(
                    self._set_included_env_roots(env_name, env_info, included_json_specs_by_hash)
                )

        current_lockfile_format = d["_meta"]["lockfile-version"]
        try:
            reader = READER_CLS[current_lockfile_format]
        except KeyError:
            msg = (
                f"Spack {spack.__version__} cannot read the lockfile '{self.lock_path}', using "
                f"the v{current_lockfile_format} format."
            )
            if CURRENT_LOCKFILE_VERSION < current_lockfile_format:
                msg += " You need to use a newer Spack version."
            raise SpackEnvironmentError(msg)

        concretized_order = [x.hash for x in self.concretized_roots]
        first_seen, concretized_order = self._filter_specs(
            reader, json_specs_by_hash, concretized_order
        )
        for idx, spec_dag_hash in enumerate(concretized_order):
            self.concretized_roots[idx].hash = spec_dag_hash
            self.specs_by_hash[spec_dag_hash] = first_seen[spec_dag_hash]

        if any(self.included_concretized_roots.values()):
            first_seen = {}

            for env_name, roots in self.included_concretized_roots.items():
                order = [x.hash for x in roots]
                filtered_spec, new_order = self._filter_specs(
                    reader, included_json_specs_by_hash, order
                )
                first_seen.update(filtered_spec)
                for idx, spec_dag_hash in enumerate(new_order):
                    roots[idx].hash = spec_dag_hash

            for env_path, roots in self.included_concretized_roots.items():
                self.included_specs_by_hash[env_path] = {x.hash: first_seen[x.hash] for x in roots}

    def _filter_specs(self, reader, json_specs_by_hash, order_concretized):
        # Track specs by their lockfile key.  Currently, spack uses the finest
        # grained hash as the lockfile key, while older formats used the build
        # hash or a previous incarnation of the DAG hash (one that did not
        # include build deps or package hash).
        specs_by_hash = {}

        # Track specs by their DAG hash, allows handling DAG hash collisions
        first_seen = {}

        # First pass: Put each spec in the map ignoring dependencies
        for lockfile_key, node_dict in json_specs_by_hash.items():
            spec = reader.from_node_dict(node_dict)
            if not spec._hash:
                # in v1 lockfiles, the hash only occurs as a key
                spec._hash = lockfile_key
            specs_by_hash[lockfile_key] = spec

        # Second pass: For each spec, get its dependencies from the node dict
        # and add them to the spec, including build specs
        for lockfile_key, node_dict in json_specs_by_hash.items():
            name, data = reader.name_and_data(node_dict)
            for _, dep_hash, deptypes, _, virtuals, direct in reader.dependencies_from_node_dict(
                data
            ):
                specs_by_hash[lockfile_key]._add_dependency(
                    specs_by_hash[dep_hash],
                    depflag=dt.canonicalize(deptypes),
                    virtuals=virtuals,
                    direct=direct,
                )

            if "build_spec" in node_dict:
                _, bhash, _ = reader.extract_build_spec_info_from_node_dict(node_dict)
                specs_by_hash[lockfile_key]._build_spec = specs_by_hash[bhash]

        # Traverse the root specs one at a time in the order they appear.
        # The first time we see each DAG hash, that's the one we want to
        # keep.  This is only required as long as we support older lockfile
        # formats where the mapping from DAG hash to lockfile key is possibly
        # one-to-many.

        for lockfile_key in order_concretized:
            for s in specs_by_hash[lockfile_key].traverse():
                if s.dag_hash() not in first_seen:
                    first_seen[s.dag_hash()] = s

        # Now make sure concretized_order and our internal specs dict
        # contains the keys used by modern spack (i.e. the dag_hash
        # that includes build deps and package hash).

        order_concretized = [specs_by_hash[h_key].dag_hash() for h_key in order_concretized]

        return first_seen, order_concretized

    def write(self, regenerate: bool = True) -> None:
        """Writes an in-memory environment to its location on disk.

        Write out package files for each newly concretized spec.  Also
        regenerate any views associated with the environment and run post-write
        hooks, if regenerate is True.

        Args:
            regenerate: regenerate views and run post-write hooks as well as writing if True.
        """
        self.manifest_uptodate_or_warn()
        if self.specs_by_hash or self.included_concrete_env_root_dirs:
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

        for x in self.concretized_roots:
            x.new = False

    def update_lockfile(self) -> None:
        with fs.write_tmp_and_move(self.lock_path, encoding="utf-8") as f:
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
        new_specs = [self.specs_by_hash[x.hash] for x in self.concretized_roots if x.new]
        for spec in traverse.traverse_nodes(new_specs):
            if not spec.concrete:
                raise ValueError("specs passed to environment.write() must be concrete!")

            self._add_to_environment_repository(spec)

    def _add_to_environment_repository(self, spec_node: Spec) -> None:
        """Add the root node of the spec to the environment repository"""
        namespace: str = spec_node.namespace
        repository = spack.repo.create_or_construct(
            root=os.path.join(self.repos_path, namespace),
            namespace=namespace,
            package_api=spack.repo.PATH.get_repo(namespace).package_api,
        )
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
        if self._previous_active:
            deactivate()
        activate(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        deactivate()
        if self._previous_active:
            activate(self._previous_active)


def _is_uninstalled(spec):
    return not spec.installed or (spec.satisfies("dev_path=*") or spec.satisfies("^dev_path=*"))


class ReusableSpecsFactory:
    """Creates a list of SpecFilters to generate the reusable specs for the environment"""

    def __init__(self, *, env: Environment, group: str):
        self.env = env
        self.group = group

    @staticmethod
    def _const(specs: List[Spec]) -> Callable[[], List[Spec]]:
        """Returns a zero-argument callable that always returns the given list."""
        return lambda: specs

    def __call__(
        self, is_usable: Callable[[Spec], bool], configuration: spack.config.Configuration
    ) -> List[SpecFilter]:
        result = []
        # Specs from group dependencies _must_ be reused, regardless of configuration
        dependencies = self.env.manifest.needs(group=self.group)
        necessary_specs = []
        for d in dependencies:
            necessary_specs.extend([x for _, x in self.env.concretized_specs_by(group=d)])

        # Specs from groups listed as dependencies
        if necessary_specs:
            necessary_specs = list(
                traverse.traverse_nodes(necessary_specs, deptype=("link", "run"))
            )
            result.append(
                SpecFilter(
                    self._const(necessary_specs), include=[], exclude=[], is_usable=is_usable
                )
            )

        # Included environments and _this_ group, instead, are subject to configuration
        concretizer_yaml = configuration.get_config("concretizer")
        reuse_yaml = concretizer_yaml.get("reuse", False)

        # With no reuse don't account for previously concretized specs in _this_ group
        if reuse_yaml is False:
            return result

        this_group_specs = [x for _, x in self.env.concretized_specs_by(group=self.group)]
        included_specs = [
            x for _, x in self.env.concretized_specs_from_all_included_environments()
        ]
        additional_specs = list(traverse.traverse_nodes(this_group_specs + included_specs))
        if not isinstance(reuse_yaml, Mapping):
            result.append(
                SpecFilter(
                    self._const(additional_specs), include=[], exclude=[], is_usable=is_usable
                )
            )
            return result

        # Here we know we have a complex reuse configuration
        default_include = reuse_yaml.get("include", [])
        default_exclude = reuse_yaml.get("exclude", [])
        for source in reuse_yaml.get("from", []):
            # We just need to take care of the environment-related parts
            if source["type"] != "environment":
                continue

            include = source.get("include", default_include)
            exclude = source.get("exclude", default_exclude)
            if "path" not in source:
                result.append(
                    SpecFilter(
                        self._const(additional_specs),
                        include=include,
                        exclude=exclude,
                        is_usable=is_usable,
                    )
                )
                continue

            env_dir = as_env_dir(source["path"])
            if env_dir in self.env.included_concrete_env_root_dirs:
                spec_pairs_from_included_envs = [
                    x for _, x in self.env.concretized_specs_from_included_environment(env_dir)
                ]
                included_specs = list(traverse.traverse_nodes(spec_pairs_from_included_envs))
                result.append(
                    SpecFilter(
                        self._const(included_specs),
                        include=include,
                        exclude=exclude,
                        is_usable=is_usable,
                    )
                )

        return result


class EnvironmentConcretizer:
    def __init__(self, env: Environment):
        self.env = env

    def concretize(
        self, *, force: Optional[bool] = None, tests: Union[bool, Sequence[str]] = False
    ) -> List[SpecPair]:
        if force is None:
            force = spack.config.get("concretizer:force")
        self._prepare_environment_for_concretization(force=force)

        result = []
        # Sort so that the ordering is deterministic, and "default" specs are first
        for current_group in self._order_groups():
            with self.env.config_override_for_group(group=current_group):
                partial_result = self._concretize_single_group(group=current_group, tests=tests)
                result.extend(partial_result)

        # Unify the specs objects, so we get correct references to all parents
        if result:
            self.env.unify_specs()
        return result

    def _concretize_single_group(
        self, *, group: str, tests: Union[bool, Sequence[str]]
    ) -> List[SpecPair]:
        # Exit early if the set of concretized specs is the set of user specs
        new_user_specs, kept_user_specs = self._partition_user_specs(group=group)
        if not new_user_specs:
            return []

        # Pick the right concretization strategy
        if group != DEFAULT_USER_SPEC_GROUP:
            tty.msg(f"Concretizing the '{group}' group of specs")
        unify = spack.config.CONFIG.get_config("concretizer").get("unify", False)
        factory = ReusableSpecsFactory(env=self.env, group=group)
        if unify == "when_possible":
            partial_result = self._concretize_together_where_possible(
                new_user_specs, kept_user_specs, tests=tests, group=group, factory=factory
            )

        elif unify is True:
            partial_result = self._concretize_together(
                new_user_specs, kept_user_specs, tests=tests, group=group, factory=factory
            )

        elif unify is False:
            partial_result = self._concretize_separately(
                new_user_specs, kept_user_specs, tests=tests, group=group, factory=factory
            )
        else:
            raise SpackEnvironmentError(f"concretization strategy not implemented [{unify}]")

        return partial_result

    def _prepare_environment_for_concretization(self, *, force: bool):
        """Reset the environment concrete state and ensure consistency with user specs."""
        if force:
            self.env.clear_concretized_specs()
        else:
            self.env.sync_concretized_specs()

        # If a combined env, check updated spec is in the linked envs
        if self.env.included_concrete_env_root_dirs:
            self.env.include_concrete_envs()

    def _partition_user_specs(
        self, *, group: str
    ) -> Tuple[List[spack.spec.Spec], List[spack.spec.Spec]]:
        """Splits the users specs in the list of the ones to be computed, and the list of
        the ones to retain.
        """
        concretized_user_specs = {x.root for x in self.env.concretized_roots if x.group == group}
        kept_user_specs, new_user_specs = stable_partition(
            self.env.user_specs_by(group=group), lambda x: x in concretized_user_specs
        )
        kept_user_specs += self.env.included_user_specs
        return new_user_specs, kept_user_specs

    def _order_groups(self) -> List[str]:
        done, result = {DEFAULT_USER_SPEC_GROUP}, [DEFAULT_USER_SPEC_GROUP]
        all_groups = self.env.manifest.groups()
        remaining = all_groups - {DEFAULT_USER_SPEC_GROUP}

        # Validate upfront that all 'needs' references point to defined groups
        for group in remaining:
            for dep in self.env.manifest.needs(group=group):
                if dep not in all_groups:
                    raise SpackEnvironmentConfigError(
                        f"group '{group}' needs '{dep}', but '{dep}' is not a defined group",
                        self.env.manifest.manifest_file,
                    )

        while remaining:
            # Check we have groups that are "ready"
            ready = []
            for current in remaining:
                deps = self.env.manifest.needs(group=current)
                if all(d in done for d in deps):
                    ready.append(current)

            # Check we can progress - if nothing is ready, there is a cycle
            if not ready:
                raise SpackEnvironmentConfigError(
                    f"cyclic dependency detected among groups: {', '.join(sorted(remaining))}",
                    self.env.manifest.manifest_file,
                )

            result.extend(ready)
            done.update(ready)
            remaining.difference_update(ready)
        return result

    def _user_spec_pairs(
        self, user_specs_to_compute: List[Spec], user_specs_to_keep: List[Spec]
    ) -> List[SpecPair]:
        specs_to_concretize = [(s, None) for s in user_specs_to_compute] + [
            (abstract, concrete)
            for abstract, concrete in self.env.concretized_specs()
            if abstract in user_specs_to_keep
        ]
        return specs_to_concretize

    def _concretize_together_where_possible(
        self,
        to_compute: List[Spec],
        to_keep: List[Spec],
        *,
        group: Optional[str] = None,
        tests: Union[bool, Sequence] = False,
        factory: ReusableSpecsFactory,
    ) -> List[SpecPair]:
        import spack.concretize

        specs_to_concretize = self._user_spec_pairs(to_compute, to_keep)
        result = spack.concretize.concretize_together_when_possible(
            specs_to_concretize, tests=tests, factory=factory
        )
        result = [x for x in result if x[0] in to_compute]
        for abstract, concrete in result:
            self.env.add_concrete_spec(abstract, concrete, new=True, group=group)

        return result

    def _concretize_together(
        self,
        to_compute: List[Spec],
        to_keep: List[Spec],
        *,
        group: Optional[str] = None,
        tests: Union[bool, Sequence] = False,
        factory: ReusableSpecsFactory,
    ) -> List[SpecPair]:
        import spack.concretize

        to_concretize = self._user_spec_pairs(to_compute, to_keep)
        try:
            concrete_pairs = spack.concretize.concretize_together(
                to_concretize, tests=tests, factory=factory
            )
        except spack.error.UnsatisfiableSpecError as e:
            # "Enhance" the error message for multiple root specs, suggest a less strict
            # form of concretization.
            if len(self.env.user_specs_by(group=group)) > 1:
                e.message += ". "
                if to_keep:
                    e.message += (
                        "Couldn't concretize without changing the existing environment. "
                        "If you are ok with changing it, try `spack concretize --force`. "
                    )
                e.message += (
                    "You could consider setting `concretizer:unify` to `when_possible` "
                    "or `false` to allow multiple versions of some packages."
                )
            raise

        # Return the portion of the return value that is new
        result = concrete_pairs[: len(to_compute)]
        for abstract, concrete in result:
            self.env.add_concrete_spec(abstract, concrete, new=True, group=group)
        return result

    def _concretize_separately(
        self,
        to_compute: List[Spec],
        to_keep: List[Spec],
        *,
        group: Optional[str] = None,
        tests: Union[bool, Sequence] = False,
        factory: ReusableSpecsFactory,
    ) -> List[SpecPair]:
        """Concretization strategy that concretizes separately one user spec after the other"""
        import spack.concretize

        to_concretize = [(x, None) for x in to_compute]
        concrete_pairs = spack.concretize.concretize_separately(
            to_concretize, tests=tests, factory=factory
        )

        for abstract, concrete in concrete_pairs:
            self.env.add_concrete_spec(abstract, concrete, new=True, group=group)

        return concrete_pairs


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


def display_specs(
    specs: List[spack.spec.Spec],
    *,
    highlight_non_defaults: bool = False,
    status_fn: Optional[Callable[["spack.spec.Spec"], "spack.spec.InstallStatus"]] = None,
) -> None:
    """Displays a list of specs traversed breadth-first, covering nodes, with install status.

    Args:
        specs: list of specs to be displayed
        highlight_non_defaults: if True, highlights non-default versions and variants in the specs
            being displayed
        status_fn: callable mapping a spec to its InstallStatus; defaults to
            ``spack.spec.Spec.install_status``
    """
    tree_string = spack.spec.tree(
        specs,
        format=spack.spec.DISPLAY_FORMAT,
        hashes=True,
        hashlen=7,
        status_fn=status_fn if status_fn is not None else spack.spec.Spec.install_status,
        highlight_version_fn=(
            spack.package_base.non_preferred_version if highlight_non_defaults else None
        ),
        highlight_variant_fn=(
            spack.package_base.non_default_variant if highlight_non_defaults else None
        ),
        key=traverse.by_dag_hash,
    )
    print(tree_string)


def make_repo_path(root):
    """Make a RepoPath from the repo subdirectories in an environment."""
    repos = (
        spack.repo.from_path(os.path.dirname(p))
        for p in glob.glob(os.path.join(root, "**", "repo.yaml"), recursive=True)
    )
    return spack.repo.RepoPath(*repos)


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
    with open(manifest, encoding="utf-8") as f:
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
    with open(manifest, "w", encoding="utf-8") as f:
        syaml.dump_config(data, f)
    return True


def _top_level_key(data):
    """Return the top level key used in this environment

    Args:
        data (dict): raw yaml data of the environment

    Returns:
        Either 'spack' or 'env'
    """
    msg = 'cannot find top level attribute "spack" or "env" in the environment'
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
        with open(manifest, encoding="utf-8") as f:
            data = syaml.load(f)
    except OSError:
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
    if not envfile.exists():
        msg = f"cannot initialize environment, {envfile} is not a valid file"
        raise SpackEnvironmentError(msg)

    if envfile.is_dir():
        # initialization file is an entire env directory
        if not (envfile / "spack.yaml").is_file():
            msg = f"cannot initialize environment, {envfile} is not a valid environment"
            raise SpackEnvironmentError(msg)
        copy_tree(str(envfile), str(environment_dir))
        return

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

    # Copy relative path includes that live inside the environment dir
    try:
        manifest = EnvironmentManifestFile(environment_dir)
    except Exception:
        # error handling for bad manifests is handled on other code paths
        return

    # TODO: make this recursive
    includes = manifest[TOP_LEVEL_KEY].get(manifest_include_name, [])
    paths = spack.config.paths_from_includes(includes)
    for path in paths:
        if os.path.isabs(path):
            continue

        abspath = pathlib.Path(os.path.normpath(environment_dir / path))
        common_path = pathlib.Path(os.path.commonpath([environment_dir, abspath]))
        if common_path != environment_dir:
            tty.debug(f"Will not copy relative include file from outside environment: {path}")
            continue

        orig_abspath = os.path.normpath(envfile.parent / path)
        if os.path.isfile(orig_abspath):
            fs.touchp(abspath)
            shutil.copy(orig_abspath, abspath)
            continue

        if not os.path.exists(orig_abspath):
            tty.warn(f"Skipping copy of non-existent include path: '{path}'")
            continue

        if os.path.exists(abspath):
            tty.warn(f"Skipping copy of directory over existing path: {path}")
            continue

        shutil.copytree(orig_abspath, abspath, symlinks=True)


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
             manifest_dir: directory containing the manifest and lockfile
        """
        # TBD: Should this be the abspath?
        manifest_dir = pathlib.Path(manifest_dir)
        lockfile = manifest_dir / lockfile_name
        with lockfile.open("r", encoding="utf-8") as f:
            data = sjson.load(f)
        roots = data["roots"]

        user_specs_by_group: Dict[str, List[str]] = {}
        for item in roots:
            # "group" is not there for Lockfile v6 and lower
            group = item.get("group", DEFAULT_USER_SPEC_GROUP)
            user_specs_by_group.setdefault(group, []).append(item["spec"])

        default_content = manifest_dir / manifest_name
        default_content.write_text(default_manifest_yaml())
        manifest = EnvironmentManifestFile(manifest_dir)

        for group, specs in user_specs_by_group.items():
            for spec in specs:
                manifest.add_user_spec(spec, group=group)

        manifest.flush()
        return manifest

    def __init__(self, manifest_dir: Union[pathlib.Path, str], name: Optional[str] = None) -> None:
        self.manifest_dir = pathlib.Path(manifest_dir)
        self.name = name or str(manifest_dir)
        self.manifest_file = self.manifest_dir / manifest_name
        self.scope_name = f"env:{self.name}"
        self.config_stage_dir = os.path.join(env_subdir_path(manifest_dir), "config")

        #: Configuration scope associated with this environment. Note that this is not
        #: invalidated by a re-read of the manifest file.
        self._env_config_scope: Optional[spack.config.ConfigScope] = None

        if not self.manifest_file.exists():
            msg = f"cannot find '{manifest_name}' in {self.manifest_dir}"
            raise SpackEnvironmentError(msg)

        with self.manifest_file.open(encoding="utf-8") as f:
            self.yaml_content = _read_yaml(f)

        # Maps groups to their dependencies
        self._groups: Dict[str, Tuple[str, ...]] = {DEFAULT_USER_SPEC_GROUP: tuple()}
        # Raw YAML definitions of the user specs for each group
        self._user_specs: Dict[str, List] = {DEFAULT_USER_SPEC_GROUP: []}
        # Configuration overrides for each group
        self._config_override: Dict[str, Any] = {DEFAULT_USER_SPEC_GROUP: None}
        # Whether specs in each group are marked explicit
        self._explicit: Dict[str, bool] = {DEFAULT_USER_SPEC_GROUP: True}
        self._init_user_specs()

        self.changed = False

    def _init_user_specs(self):
        specs_yaml = self.configuration.get(USER_SPECS_KEY, [])
        for item in specs_yaml:
            if isinstance(item, str):
                self._user_specs[DEFAULT_USER_SPEC_GROUP].append(item)
            elif isinstance(item, dict):
                group = item.get("group", DEFAULT_USER_SPEC_GROUP)

                # Error if a group is defined more than once
                if group != DEFAULT_USER_SPEC_GROUP and group in self._groups:
                    raise SpackEnvironmentConfigError(
                        f"group '{group}' defined more than once", self.manifest_file
                    )

                # Add an entry for the user specs and store group dependencies
                if group not in self._user_specs:
                    self._user_specs[group] = []
                    self._groups[group] = tuple(item.get("needs", ()))
                    self._config_override[group] = item.get("override", None)
                    self._explicit[group] = item.get("explicit", True)

                if "matrix" in item:
                    # Short form if the group is composed of only one matrix
                    self._user_specs[group].append(
                        {
                            key: item[key]
                            for key in spack.schema.spec_list.spec_list_properties
                            if key in item
                        }
                    )
                elif "specs" in item:
                    self._user_specs[group].extend(item["specs"])

    def _clear_user_specs(self) -> None:
        self._user_specs = {DEFAULT_USER_SPEC_GROUP: []}
        self._groups = {DEFAULT_USER_SPEC_GROUP: tuple()}
        self._config_override = {DEFAULT_USER_SPEC_GROUP: None}
        self._explicit = {DEFAULT_USER_SPEC_GROUP: True}

    def _all_matches(self, user_spec: str) -> List[str]:
        """Maps the input string to the first equivalent user spec in the manifest,
        and returns it.

        Args:
            user_spec: user spec to be found

        Raises:
            ValueError: if no equivalent match is found
        """
        result = []
        for yaml_spec_str in self.configuration["specs"]:
            if Spec(yaml_spec_str) == Spec(user_spec):
                result.append(yaml_spec_str)

        if not result:
            raise ValueError(f"cannot find a spec equivalent to {user_spec}")

        return result

    def user_specs(self, *, group: Optional[str] = None) -> List:
        group = self._ensure_group_exists(group)
        return self._user_specs[group]

    def config_override(
        self, *, group: Optional[str] = None
    ) -> Optional[spack.config.InternalConfigScope]:
        group = self._ensure_group_exists(group)
        data = self._config_override[group]
        if data is None:
            return None
        return spack.config.InternalConfigScope(f"env:groups:{group}", data)

    def groups(self) -> KeysView:
        """Returns the list of groups defined in the manifest"""
        return self._groups.keys()

    def needs(self, *, group: Optional[str] = None) -> Tuple[str, ...]:
        """Returns the dependencies of a group of user specs."""
        group = self._ensure_group_exists(group)
        return self._groups[group]

    def is_explicit(self, *, group: Optional[str] = None) -> bool:
        """Returns whether specs in a group are marked explicit.

        When False, specs in the group are installed as implicit dependencies
        and are eligible for garbage collection once no other spec depends on them.
        """
        group = self._ensure_group_exists(group)
        return self._explicit[group]

    def _ensure_group_exists(self, group: Optional[str]) -> str:
        group = DEFAULT_USER_SPEC_GROUP if group is None else group
        if group not in self._groups:
            raise ValueError(f"user specs group '{group}' not found in {self.manifest_file}")
        return group

    def add_user_spec(self, user_spec: str, *, group: Optional[str] = None) -> None:
        """Appends the user spec passed as input to the list of root specs for the given group.

        Args:
            user_spec: user spec to be appended
            group: group where the spec should be added. If None, the default group is used.
        """
        group = group or DEFAULT_USER_SPEC_GROUP

        if group == DEFAULT_USER_SPEC_GROUP:
            # Append to top-most specs: attribute
            specs_yaml = self.configuration.setdefault("specs", [])
            specs_yaml.append(user_spec)
        else:
            # Append to specs: attribute within a group
            group_in_yaml = self._get_group(group)
            group_in_yaml.setdefault("specs", []).append(user_spec)

        self._user_specs[group].append(user_spec)
        self.changed = True

    def _get_group(self, group: str) -> Dict:
        """Find or create the group entry in the manifest"""
        specs_yaml = self.configuration.setdefault("specs", [])
        group_entry = None
        for item in specs_yaml:
            if isinstance(item, dict) and item.get("group") == group:
                group_entry = item
                break

        if group_entry is None:
            group_entry = {"group": group, "specs": []}
            specs_yaml.append(group_entry)
            self._groups[group] = tuple()
            self._config_override[group] = None
            self._user_specs[group] = []
            self._explicit[group] = True

        return group_entry

    def remove_user_spec(self, user_spec: str) -> None:
        """Removes the user spec passed as input from the default list of root specs

        Args:
            user_spec: user spec to be removed

        Raises:
            SpackEnvironmentError: when the user spec is not in the list
        """
        try:
            for key in self._all_matches(user_spec):
                self.configuration["specs"].remove(key)
                self._user_specs[DEFAULT_USER_SPEC_GROUP].remove(key)
        except ValueError as e:
            msg = f"cannot remove {user_spec} from {self}, no such spec exists"
            raise SpackEnvironmentError(msg) from e
        self.changed = True

    def clear(self) -> None:
        """Clear all user specs from the list of root specs"""
        self.configuration["specs"] = []
        self._clear_user_specs()
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
            self.configuration["specs"][idx] = user_spec
            self._clear_user_specs()
            self._init_user_specs()
        except ValueError as e:
            msg = f"cannot override {user_spec} from {self}"
            raise SpackEnvironmentError(msg) from e
        self.changed = True

    def set_include_concrete(self, include_concrete: List[str]) -> None:
        """Sets the included concrete environments in the manifest to the value(s) passed as input.

        Args:
            include_concrete: list of already existing concrete environments to include
        """
        self.configuration[lockfile_include_key] = list(include_concrete)
        self.changed = True

    def add_definition(self, user_spec: str, list_name: str) -> None:
        """Appends a user spec to the first active definition matching the name passed as argument.

        Args:
            user_spec: user spec to be appended
            list_name: name of the definition where to append

        Raises:
            SpackEnvironmentError: is no valid definition exists already
        """
        defs = self.configuration.get("definitions", [])
        msg = f"cannot add {user_spec} to the '{list_name}' definition, no valid list exists"

        for idx, item in self._iterate_on_definitions(defs, list_name=list_name, err_msg=msg):
            item[list_name].append(user_spec)
            break

        # "definitions" can be remote, so we need to update the global config too
        spack.config.CONFIG.set("definitions", defs, scope=self.scope_name)
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
        defs = self.configuration.get("definitions", [])
        msg = f"cannot remove {user_spec} from the '{list_name}' definition, no valid list exists"

        for idx, item in self._iterate_on_definitions(defs, list_name=list_name, err_msg=msg):
            try:
                item[list_name].remove(user_spec)
                break
            except ValueError:
                pass

        # "definitions" can be remote, so we need to update the global config too
        spack.config.CONFIG.set("definitions", defs, scope=self.scope_name)
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
        defs = self.configuration.get("definitions", [])
        msg = f"cannot override {user_spec} with {override} in the '{list_name}' definition"

        for idx, item in self._iterate_on_definitions(defs, list_name=list_name, err_msg=msg):
            try:
                sub_index = item[list_name].index(user_spec)
                item[list_name][sub_index] = override
                break
            except ValueError:
                pass

        # "definitions" can be remote, so we need to update the global config too
        spack.config.CONFIG.set("definitions", defs, scope=self.scope_name)
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
            if not spack.spec.eval_conditional(condition_str):
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
            self.configuration["view"][default_view_name].update(view)
            self.changed = True
            return

        if not isinstance(view, bool):
            view = str(view)

        self.configuration["view"] = view
        self.changed = True

    def remove_default_view(self) -> None:
        """Removes the default view from the manifest file"""
        view_data = self.configuration.get("view")
        if isinstance(view_data, collections.abc.Mapping):
            self.configuration["view"].pop(default_view_name)
            self.changed = True
            return

        self.set_default_view(view=False)

    def flush(self) -> None:
        """Synchronizes the object with the manifest file on disk."""
        if not self.changed:
            return

        with fs.write_tmp_and_move(os.path.realpath(self.manifest_file)) as f:
            _write_yaml(self.yaml_content, f)
        self.changed = False

    @property
    def configuration(self):
        """Return the dictionaries in the pristine YAML, without the top level attribute"""
        return self.yaml_content[TOP_LEVEL_KEY]

    def __len__(self):
        return len(self.yaml_content)

    def __getitem__(self, key):
        return self.yaml_content[key]

    def __iter__(self):
        return iter(self.yaml_content)

    def __str__(self):
        return str(self.manifest_file)

    @property
    def env_config_scope(self) -> spack.config.ConfigScope:
        """The configuration scope for the environment manifest"""
        if self._env_config_scope is None:
            self._env_config_scope = spack.config.SingleFileScope(
                self.scope_name,
                str(self.manifest_file),
                spack.schema.env.schema,
                yaml_path=[TOP_LEVEL_KEY],
            )
            ensure_no_disallowed_env_config_mods(self._env_config_scope)
        return self._env_config_scope

    def prepare_config_scope(self) -> None:
        """Add the manifest's scope to the global configuration search path."""
        spack.config.CONFIG.push_scope(
            self.env_config_scope, priority=ConfigScopePriority.ENVIRONMENT
        )

    def deactivate_config_scope(self) -> None:
        """Remove the manifest's scope from the global config path."""
        spack.config.CONFIG.remove_scope(self.env_config_scope.name)

    @contextlib.contextmanager
    def use_config(self):
        """Ensure only the manifest's configuration scopes are global."""
        with no_active_environment():
            self.prepare_config_scope()
            yield
            self.deactivate_config_scope()


def environment_path_scope(name: str, path: str) -> Optional[spack.config.ConfigScope]:
    """Retrieve the suitably named environment path scope

    Arguments:
        name: configuration scope name
        path: path to configuration file(s)

    Returns: list of environment scopes, if any, or None
    """
    if exists(path):  # managed environment
        manifest = EnvironmentManifestFile(root(path))
    elif is_env_dir(path):  # anonymous environment
        manifest = EnvironmentManifestFile(path)
    else:
        return None

    manifest.env_config_scope.name = f"{name}:{manifest.env_config_scope.name}"
    manifest.env_config_scope.writable = False
    return manifest.env_config_scope


class SpackEnvironmentError(spack.error.SpackError):
    """Superclass for all errors to do with Spack environments."""


class SpackEnvironmentViewError(SpackEnvironmentError):
    """Class for errors regarding view generation."""


class SpackEnvironmentConfigError(SpackEnvironmentError):
    """Class for Spack environment-specific configuration errors."""

    def __init__(self, msg, filename):
        super().__init__(f"{msg} in {filename}")


class SpackEnvironmentDevelopError(SpackEnvironmentError):
    """Class for errors in applying develop information to an environment."""
