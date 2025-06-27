# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import abc
import contextlib
import difflib
import errno
import functools
import importlib
import importlib.machinery
import importlib.util
import inspect
import itertools
import os
import random
import re
import shutil
import stat
import string
import sys
import traceback
import types
import uuid
import warnings
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterator,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)

import llnl.path
import llnl.util.filesystem as fs
import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.filesystem import working_dir

import spack
import spack.caches
import spack.config
import spack.error
import spack.patch
import spack.paths
import spack.provider_index
import spack.spec
import spack.tag
import spack.tengine
import spack.util.executable
import spack.util.file_cache
import spack.util.git
import spack.util.hash
import spack.util.lock
import spack.util.naming as nm
import spack.util.path
import spack.util.spack_yaml as syaml

PKG_MODULE_PREFIX_V1 = "spack.pkg."
PKG_MODULE_PREFIX_V2 = "spack_repo."

_API_REGEX = re.compile(r"^v(\d+)\.(\d+)$")

SPACK_REPO_INDEX_FILE_NAME = "spack-repo-index.yaml"


def package_repository_lock() -> spack.util.lock.Lock:
    """Lock for process safety when cloning remote package repositories"""
    return spack.util.lock.Lock(
        os.path.join(spack.paths.user_cache_path, "package-repository.lock")
    )


def is_package_module(fullname: str) -> bool:
    """Check if the given module is a package module."""
    return fullname.startswith(PKG_MODULE_PREFIX_V1) or (
        fullname.startswith(PKG_MODULE_PREFIX_V2) and fullname.endswith(".package")
    )


def namespace_from_fullname(fullname: str) -> str:
    """Return the repository namespace only for the full module name.

    For instance:

        namespace_from_fullname("spack.pkg.builtin.hdf5") == "builtin"
        namespace_from_fullname("spack_repo.x.y.z.packages.pkg_name.package") == "x.y.z"

    Args:
        fullname: full name for the Python module
    """
    if fullname.startswith(PKG_MODULE_PREFIX_V1):
        namespace, _, _ = fullname.rpartition(".")
        return namespace[len(PKG_MODULE_PREFIX_V1) :]
    elif fullname.startswith(PKG_MODULE_PREFIX_V2) and fullname.endswith(".package"):
        return ".".join(fullname.split(".")[1:-3])
    return fullname


class _PrependFileLoader(importlib.machinery.SourceFileLoader):
    def __init__(self, fullname: str, repo: "Repo", package_name: str) -> None:
        self.repo = repo
        self.package_name = package_name
        path = repo.filename_for_package_name(package_name)
        self.fullname = fullname
        self.prepend = b"from spack_repo.builtin.build_systems._package_api_v1 import *\n"
        super().__init__(self.fullname, path)

    def path_stats(self, path):
        stats = dict(super().path_stats(path))
        stats["size"] += len(self.prepend)
        return stats

    def get_data(self, path):
        data = super().get_data(path)
        return self.prepend + data if path == self.path else data


class SpackNamespaceLoader:
    def create_module(self, spec):
        return SpackNamespace(spec.name)

    def exec_module(self, module):
        module.__loader__ = self


class ReposFinder:
    """MetaPathFinder class that loads a Python module corresponding to an API v1 Spack package.

    Returns a loader based on the inspection of the current repository list.
    """

    #: The current list of repositories.
    repo_path: "RepoPath"

    def find_spec(self, fullname, python_path, target=None):
        # "target" is not None only when calling importlib.reload()
        if target is not None:
            raise RuntimeError('cannot reload module "{0}"'.format(fullname))

        # Preferred API from https://peps.python.org/pep-0451/
        if not fullname.startswith(PKG_MODULE_PREFIX_V1) and fullname != "spack.pkg":
            return None

        loader = self.compute_loader(fullname)
        if loader is None:
            return None
        return importlib.util.spec_from_loader(fullname, loader)

    def compute_loader(self, fullname: str):
        # namespaces are added to repo, and package modules are leaves.
        namespace, dot, module_name = fullname.rpartition(".")

        # If it's a module in some repo, or if it is the repo's namespace, let the repo handle it.

        if not hasattr(self, "repo_path"):
            return None

        for repo in self.repo_path.repos:
            # We are using the namespace of the repo and the repo contains the package
            if namespace == repo.full_namespace:
                # With 2 nested conditionals we can call "repo.real_name" only once
                package_name = repo.real_name(module_name)
                if package_name:
                    return _PrependFileLoader(fullname, repo, package_name)

            # We are importing a full namespace like 'spack.pkg.builtin'
            if fullname == repo.full_namespace:
                return SpackNamespaceLoader()

        # No repo provides the namespace, but it is a valid prefix of
        # something in the RepoPath.
        if self.repo_path.by_namespace.is_prefix(fullname[len(PKG_MODULE_PREFIX_V1) :]):
            return SpackNamespaceLoader()

        return None


#
# These names describe how repos should be laid out in the filesystem.
#
repo_config_name = "repo.yaml"  # Top-level filename for repo config.
repo_index_name = "index.yaml"  # Top-level filename for repository index.
packages_dir_name = "packages"  # Top-level repo directory containing pkgs.
package_file_name = "package.py"  # Filename for packages in a repository.

#: Guaranteed unused default value for some functions.
NOT_PROVIDED = object()


def builtin_repo() -> "Repo":
    """Get the test repo if it is active, otherwise the builtin repo."""
    try:
        return PATH.get_repo("builtin_mock")
    except UnknownNamespaceError:
        return PATH.get_repo("builtin")


class GitExe:
    # Wrapper around Executable for git to set working directory for all
    # invocations.
    #
    # Not using -C as that is not supported for git < 1.8.5.
    def __init__(self, packages_path: str):
        self._git_cmd = spack.util.git.git(required=True)
        self.packages_dir = packages_path

    def __call__(self, *args, **kwargs) -> str:
        with working_dir(self.packages_dir):
            return self._git_cmd(*args, **kwargs, output=str)


def list_packages(rev: str, repo: "Repo") -> List[str]:
    """List all packages associated with the given revision"""
    git = GitExe(repo.packages_path)

    # git ls-tree does not support ... merge-base syntax, so do it manually
    if rev.endswith("..."):
        ref = rev.replace("...", "")
        rev = git("merge-base", ref, "HEAD").strip()

    output = git("ls-tree", "-r", "--name-only", rev)

    # recursively list the packages directory
    package_paths = [
        line.split(os.sep) for line in output.split("\n") if line.endswith("package.py")
    ]

    # take the directory names with one-level-deep package files
    package_names = [
        nm.pkg_dir_to_pkg_name(line[0], repo.package_api)
        for line in package_paths
        if len(line) == 2
    ]

    return sorted(set(package_names))


def diff_packages(rev1: str, rev2: str, repo: "Repo") -> Tuple[Set[str], Set[str]]:
    """Compute packages lists for the two revisions and return a tuple
    containing all the packages in rev1 but not in rev2 and all the
    packages in rev2 but not in rev1."""
    p1 = set(list_packages(rev1, repo))
    p2 = set(list_packages(rev2, repo))
    return p1.difference(p2), p2.difference(p1)


def get_all_package_diffs(type: str, repo: "Repo", rev1="HEAD^1", rev2="HEAD") -> Set[str]:
    """Get packages changed, added, or removed (or any combination of those) since a commit.

    Arguments:

        type: String containing one or more of 'A', 'R', 'C'
        rev1: Revision to compare against, default is 'HEAD^'
        rev2: Revision to compare to rev1, default is 'HEAD'
    """
    lower_type = type.lower()
    if not re.match("^[arc]*$", lower_type):
        tty.die(
            f"Invalid change type: '{type}'. "
            "Can contain only A (added), R (removed), or C (changed)"
        )

    removed, added = diff_packages(rev1, rev2, repo)

    git = GitExe(repo.packages_path)
    out = git("diff", "--relative", "--name-only", rev1, rev2).strip()

    lines = [] if not out else re.split(r"\s+", out)
    changed: Set[str] = set()
    for path in lines:
        dir_name, _, _ = path.partition("/")
        if not nm.valid_module_name(dir_name, repo.package_api):
            continue
        pkg_name = nm.pkg_dir_to_pkg_name(dir_name, repo.package_api)
        if pkg_name not in added and pkg_name not in removed:
            changed.add(pkg_name)

    packages: Set[str] = set()
    if "a" in lower_type:
        packages |= added
    if "r" in lower_type:
        packages |= removed
    if "c" in lower_type:
        packages |= changed

    return packages


def add_package_to_git_stage(packages: List[str], repo: "Repo") -> None:
    """add a package to the git stage with `git add`"""
    git = GitExe(repo.packages_path)

    for pkg_name in packages:
        filename = PATH.filename_for_package_name(pkg_name)
        if not os.path.isfile(filename):
            tty.die(f"No such package: {pkg_name}.  Path does not exist:", filename)

        git("add", filename)


def autospec(function):
    """Decorator that automatically converts the first argument of a
    function to a Spec.
    """

    @functools.wraps(function)
    def converter(self, spec_like, *args, **kwargs):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like, *args, **kwargs)

    return converter


def is_package_file(filename):
    """Determine whether we are in a package file from a repo."""
    # Package files are named `package.py` and are not in lib/spack/spack
    # We have to remove the file extension because it can be .py and can be
    # .pyc depending on context, and can differ between the files
    import spack.package_base  # break cycle

    filename_noext = os.path.splitext(filename)[0]
    packagebase_filename_noext = os.path.splitext(inspect.getfile(spack.package_base.PackageBase))[
        0
    ]
    return (
        filename_noext != packagebase_filename_noext
        and os.path.basename(filename_noext) == "package"
    )


class SpackNamespace(types.ModuleType):
    """Allow lazy loading of modules."""

    def __init__(self, namespace):
        super().__init__(namespace)
        self.__file__ = "(spack namespace)"
        self.__path__ = []
        self.__name__ = namespace
        self.__package__ = namespace
        self.__modules = {}

    def __getattr__(self, name):
        """Getattr lazily loads modules if they're not already loaded."""
        submodule = f"{self.__package__}.{name}"
        try:
            setattr(self, name, importlib.import_module(submodule))
        except ImportError:
            msg = "'{0}' object has no attribute {1}"
            raise AttributeError(msg.format(type(self), name))
        return getattr(self, name)


class FastPackageChecker(Mapping[str, os.stat_result]):
    """Cache that maps package names to the stats obtained on the
    'package.py' files associated with them.

    For each repository a cache is maintained at class level, and shared among
    all instances referring to it. Update of the global cache is done lazily
    during instance initialization.
    """

    #: Global cache, reused by every instance
    _paths_cache: Dict[str, Dict[str, os.stat_result]] = {}

    def __init__(self, packages_path: str, package_api: Tuple[int, int]) -> None:
        # The path of the repository managed by this instance
        self.packages_path = packages_path
        self.package_api = package_api

        # If the cache we need is not there yet, then build it appropriately
        if packages_path not in self._paths_cache:
            self._paths_cache[packages_path] = self._create_new_cache()

        #: Reference to the appropriate entry in the global cache
        self._packages_to_stats = self._paths_cache[packages_path]

    def invalidate(self) -> None:
        """Regenerate cache for this checker."""
        self._paths_cache[self.packages_path] = self._create_new_cache()
        self._packages_to_stats = self._paths_cache[self.packages_path]

    def _create_new_cache(self) -> Dict[str, os.stat_result]:
        """Create a new cache for packages in a repo.

        The implementation here should try to minimize filesystem
        calls.  At the moment, it is O(number of packages) and makes
        about one stat call per package.  This is reasonably fast, and
        avoids actually importing packages in Spack, which is slow.
        """
        # Create a dictionary that will store the mapping between a
        # package name and its stat info
        cache: Dict[str, os.stat_result] = {}
        with os.scandir(self.packages_path) as entries:
            for entry in entries:
                # Construct the file name from the directory
                pkg_file = os.path.join(entry.path, package_file_name)

                try:
                    sinfo = os.stat(pkg_file)
                except OSError as e:
                    if e.errno in (errno.ENOENT, errno.ENOTDIR):
                        # No package.py file here.
                        continue
                    elif e.errno == errno.EACCES:
                        tty.warn(f"Can't read package file {pkg_file}.")
                        continue
                    raise e

                # If it's not a file, skip it.
                if not stat.S_ISREG(sinfo.st_mode):
                    continue

                # Only consider package.py files in directories that are valid module names under
                # the current package API
                if not nm.valid_module_name(entry.name, self.package_api):
                    x, y = self.package_api
                    tty.warn(
                        f"Package {pkg_file} cannot be used because `{entry.name}` is not a valid "
                        f"Spack package module name for Package API v{x}.{y}."
                    )
                    continue

                # Store the stat info by package name.
                cache[nm.pkg_dir_to_pkg_name(entry.name, self.package_api)] = sinfo

        return cache

    def last_mtime(self) -> float:
        return max(sinfo.st_mtime for sinfo in self._packages_to_stats.values())

    def modified_since(self, since: float) -> List[str]:
        return [name for name, sinfo in self._packages_to_stats.items() if sinfo.st_mtime > since]

    def __getitem__(self, item: str) -> os.stat_result:
        return self._packages_to_stats[item]

    def __iter__(self) -> Iterator[str]:
        return iter(self._packages_to_stats)

    def __len__(self) -> int:
        return len(self._packages_to_stats)


class Indexer(metaclass=abc.ABCMeta):
    """Adaptor for indexes that need to be generated when repos are updated."""

    def __init__(self, repository):
        self.repository = repository
        self.index = None

    def create(self):
        self.index = self._create()

    @abc.abstractmethod
    def _create(self):
        """Create an empty index and return it."""

    def needs_update(self, pkg):
        """Whether an update is needed when the package file hasn't changed.

        Returns:
            (bool): ``True`` if this package needs its index
                updated, ``False`` otherwise.

        We already automatically update indexes when package files
        change, but other files (like patches) may change underneath the
        package file. This method can be used to check additional
        package-specific files whenever they're loaded, to tell the
        RepoIndex to update the index *just* for that package.

        """
        return False

    @abc.abstractmethod
    def read(self, stream):
        """Read this index from a provided file object."""

    @abc.abstractmethod
    def update(self, pkg_fullname):
        """Update the index in memory with information about a package."""

    @abc.abstractmethod
    def write(self, stream):
        """Write the index to a file object."""


class TagIndexer(Indexer):
    """Lifecycle methods for a TagIndex on a Repo."""

    def _create(self):
        return spack.tag.TagIndex(self.repository)

    def read(self, stream):
        self.index = spack.tag.TagIndex.from_json(stream, self.repository)

    def update(self, pkg_fullname):
        self.index.update_package(pkg_fullname.split(".")[-1])

    def write(self, stream):
        self.index.to_json(stream)


class ProviderIndexer(Indexer):
    """Lifecycle methods for virtual package providers."""

    def _create(self):
        return spack.provider_index.ProviderIndex(repository=self.repository)

    def read(self, stream):
        self.index = spack.provider_index.ProviderIndex.from_json(stream, self.repository)

    def update(self, pkg_fullname):
        name = pkg_fullname.split(".")[-1]
        is_virtual = (
            not self.repository.exists(name) or self.repository.get_pkg_class(name).virtual
        )
        if is_virtual:
            return
        self.index.remove_provider(pkg_fullname)
        self.index.update(pkg_fullname)

    def write(self, stream):
        self.index.to_json(stream)


class PatchIndexer(Indexer):
    """Lifecycle methods for patch cache."""

    def _create(self):
        return spack.patch.PatchCache(repository=self.repository)

    def needs_update(self):
        # TODO: patches can change under a package and we should handle
        # TODO: it, but we currently punt. This should be refactored to
        # TODO: check whether patches changed each time a package loads,
        # TODO: tell the RepoIndex to reindex them.
        return False

    def read(self, stream):
        self.index = spack.patch.PatchCache.from_json(stream, repository=self.repository)

    def write(self, stream):
        self.index.to_json(stream)

    def update(self, pkg_fullname):
        self.index.update_package(pkg_fullname)


class RepoIndex:
    """Container class that manages a set of Indexers for a Repo.

    This class is responsible for checking packages in a repository for
    updates (using ``FastPackageChecker``) and for regenerating indexes
    when they're needed.

    ``Indexers`` should be added to the ``RepoIndex`` using
    ``add_indexer(name, indexer)``, and they should support the interface
    defined by ``Indexer``, so that the ``RepoIndex`` can read, generate,
    and update stored indices.

    Generated indexes are accessed by name via ``__getitem__()``."""

    def __init__(
        self,
        package_checker: FastPackageChecker,
        namespace: str,
        cache: spack.util.file_cache.FileCache,
    ):
        self.checker = package_checker
        self.packages_path = self.checker.packages_path
        if sys.platform == "win32":
            self.packages_path = llnl.path.convert_to_posix_path(self.packages_path)
        self.namespace = namespace

        self.indexers: Dict[str, Indexer] = {}
        self.indexes: Dict[str, Any] = {}
        self.cache = cache

    def add_indexer(self, name: str, indexer: Indexer):
        """Add an indexer to the repo index.

        Arguments:
            name: name of this indexer
            indexer: object implementing the ``Indexer`` interface"""
        self.indexers[name] = indexer

    def __getitem__(self, name):
        """Get the index with the specified name, reindexing if needed."""
        indexer = self.indexers.get(name)
        if not indexer:
            raise KeyError("no such index: %s" % name)

        if name not in self.indexes:
            self._build_all_indexes()

        return self.indexes[name]

    def _build_all_indexes(self):
        """Build all the indexes at once.

        We regenerate *all* indexes whenever *any* index needs an update,
        because the main bottleneck here is loading all the packages.  It
        can take tens of seconds to regenerate sequentially, and we'd
        rather only pay that cost once rather than on several
        invocations."""
        for name, indexer in self.indexers.items():
            self.indexes[name] = self._build_index(name, indexer)

    def _build_index(self, name: str, indexer: Indexer):
        """Determine which packages need an update, and update indexes."""

        # Filename of the provider index cache (we assume they're all json)
        cache_filename = (
            f"{name}/{self.namespace}-specfile_v{spack.spec.SPECFILE_FORMAT_VERSION}-index.json"
        )

        # Compute which packages needs to be updated in the cache
        index_mtime = self.cache.mtime(cache_filename)
        needs_update = self.checker.modified_since(index_mtime)

        index_existed = self.cache.init_entry(cache_filename)
        if index_existed and not needs_update:
            # If the index exists and doesn't need an update, read it
            with self.cache.read_transaction(cache_filename) as f:
                indexer.read(f)

        else:
            # Otherwise update it and rewrite the cache file
            with self.cache.write_transaction(cache_filename) as (old, new):
                indexer.read(old) if old else indexer.create()

                # Compute which packages needs to be updated **again** in case someone updated them
                # while we waited for the lock
                new_index_mtime = self.cache.mtime(cache_filename)
                if new_index_mtime != index_mtime:
                    needs_update = self.checker.modified_since(new_index_mtime)

                for pkg_name in needs_update:
                    indexer.update(f"{self.namespace}.{pkg_name}")

                indexer.write(new)

        return indexer.index


class RepoPath:
    """A RepoPath is a list of Repo instances that function as one.

    It functions exactly like a Repo, but it operates on the combined
    results of the Repos in its list instead of on a single package
    repository.
    """

    def __init__(self, *repos: "Repo") -> None:
        self.repos: List[Repo] = []
        self.by_namespace = nm.NamespaceTrie()
        self._provider_index: Optional[spack.provider_index.ProviderIndex] = None
        self._patch_index: Optional[spack.patch.PatchCache] = None
        self._tag_index: Optional[spack.tag.TagIndex] = None

        for repo in repos:
            self.put_last(repo)

    @staticmethod
    def from_descriptors(
        descriptors: "RepoDescriptors",
        cache: spack.util.file_cache.FileCache,
        overrides: Optional[Dict[str, Any]] = None,
    ) -> "RepoPath":
        repo_path, errors = descriptors.construct(cache=cache, fetch=True, overrides=overrides)

        # Merely warn if package repositories from config could not be constructed.
        if errors:
            for path, error in errors.items():
                tty.warn(f"Error constructing repository '{path}': {error}")

        return repo_path

    @staticmethod
    def from_config(config: spack.config.Configuration) -> "RepoPath":
        """Create a RepoPath from a configuration object."""
        overrides = {
            pkg_name: data["package_attributes"]
            for pkg_name, data in config.get("packages").items()
            if pkg_name != "all" and "package_attributes" in data
        }

        return RepoPath.from_descriptors(
            descriptors=RepoDescriptors.from_config(lock=package_repository_lock(), config=config),
            cache=spack.caches.MISC_CACHE,
            overrides=overrides,
        )

    def enable(self) -> None:
        """Set the relevant search paths for package module loading"""
        REPOS_FINDER.repo_path = self
        for p in reversed(self.python_paths()):
            if p not in sys.path:
                sys.path.insert(0, p)

    def disable(self) -> None:
        """Disable the search paths for package module loading"""
        if hasattr(REPOS_FINDER, "repo_path"):
            del REPOS_FINDER.repo_path
        for p in self.python_paths():
            if p in sys.path:
                sys.path.remove(p)

    def ensure_unwrapped(self) -> "RepoPath":
        """Ensure we unwrap this object from any dynamic wrapper (like Singleton)"""
        return self

    def put_first(self, repo: Union["Repo", "RepoPath"]) -> None:
        """Add repo first in the search path."""
        if isinstance(repo, RepoPath):
            for r in reversed(repo.repos):
                self.put_first(r)
            return

        self.repos.insert(0, repo)
        self.by_namespace[repo.namespace] = repo

    def put_last(self, repo):
        """Add repo last in the search path."""
        if isinstance(repo, RepoPath):
            for r in repo.repos:
                self.put_last(r)
            return

        self.repos.append(repo)

        # don't mask any higher-precedence repos with same namespace
        if repo.namespace not in self.by_namespace:
            self.by_namespace[repo.namespace] = repo

    def remove(self, repo):
        """Remove a repo from the search path."""
        if repo in self.repos:
            self.repos.remove(repo)

    def get_repo(self, namespace: str) -> "Repo":
        """Get a repository by namespace."""
        if namespace not in self.by_namespace:
            raise UnknownNamespaceError(namespace)
        return self.by_namespace[namespace]

    def first_repo(self) -> Optional["Repo"]:
        """Get the first repo in precedence order."""
        return self.repos[0] if self.repos else None

    @llnl.util.lang.memoized
    def _all_package_names_set(self, include_virtuals) -> Set[str]:
        return {name for repo in self.repos for name in repo.all_package_names(include_virtuals)}

    @llnl.util.lang.memoized
    def _all_package_names(self, include_virtuals: bool) -> List[str]:
        """Return all unique package names in all repositories."""
        return sorted(self._all_package_names_set(include_virtuals), key=lambda n: n.lower())

    def all_package_names(self, include_virtuals: bool = False) -> List[str]:
        return self._all_package_names(include_virtuals)

    def package_path(self, name: str) -> str:
        """Get path to package.py file for this repo."""
        return self.repo_for_pkg(name).package_path(name)

    def all_package_paths(self) -> Generator[str, None, None]:
        for name in self.all_package_names():
            yield self.package_path(name)

    def packages_with_tags(self, *tags: str, full: bool = False) -> Set[str]:
        """Returns a set of packages matching any of the tags in input.

        Args:
            full: if True the package names in the output are fully-qualified
        """
        return {
            f"{repo.namespace}.{pkg}" if full else pkg
            for repo in self.repos
            for pkg in repo.packages_with_tags(*tags)
        }

    def all_package_classes(self) -> Generator[Type["spack.package_base.PackageBase"], None, None]:
        for name in self.all_package_names():
            yield self.get_pkg_class(name)

    @property
    def provider_index(self) -> spack.provider_index.ProviderIndex:
        """Merged ProviderIndex from all Repos in the RepoPath."""
        if self._provider_index is None:
            self._provider_index = spack.provider_index.ProviderIndex(repository=self)
            for repo in reversed(self.repos):
                self._provider_index.merge(repo.provider_index)
        return self._provider_index

    @property
    def tag_index(self) -> spack.tag.TagIndex:
        """Merged TagIndex from all Repos in the RepoPath."""
        if self._tag_index is None:
            self._tag_index = spack.tag.TagIndex(repository=self)
            for repo in reversed(self.repos):
                self._tag_index.merge(repo.tag_index)
        return self._tag_index

    @property
    def patch_index(self) -> spack.patch.PatchCache:
        """Merged PatchIndex from all Repos in the RepoPath."""
        if self._patch_index is None:
            self._patch_index = spack.patch.PatchCache(repository=self)
            for repo in reversed(self.repos):
                self._patch_index.update(repo.patch_index)
        return self._patch_index

    @autospec
    def providers_for(self, virtual_spec: "spack.spec.Spec") -> List["spack.spec.Spec"]:
        providers = [
            spec
            for spec in self.provider_index.providers_for(virtual_spec)
            if spec.name in self._all_package_names_set(include_virtuals=False)
        ]
        if not providers:
            raise UnknownPackageError(virtual_spec.fullname)
        return providers

    @autospec
    def extensions_for(
        self, extendee_spec: "spack.spec.Spec"
    ) -> List["spack.package_base.PackageBase"]:
        return [
            pkg_cls(spack.spec.Spec(pkg_cls.name))
            for pkg_cls in self.all_package_classes()
            if pkg_cls(spack.spec.Spec(pkg_cls.name)).extends(extendee_spec)
        ]

    def last_mtime(self):
        """Time a package file in this repo was last updated."""
        return max(repo.last_mtime() for repo in self.repos)

    def repo_for_pkg(self, spec: Union[str, "spack.spec.Spec"]) -> "Repo":
        """Given a spec, get the repository for its package."""
        # We don't @_autospec this function b/c it's called very frequently
        # and we want to avoid parsing str's into Specs unnecessarily.
        if isinstance(spec, spack.spec.Spec):
            namespace = spec.namespace
            name = spec.name
        else:
            # handle strings directly for speed instead of @_autospec'ing
            namespace, _, name = spec.rpartition(".")

        # If the spec already has a namespace, then return the
        # corresponding repo if we know about it.
        if namespace:
            if namespace not in self.by_namespace:
                raise UnknownNamespaceError(namespace, name=name)
            return self.by_namespace[namespace]

        # If there's no namespace, search in the RepoPath.
        for repo in self.repos:
            if name in repo:
                return repo

        # If the package isn't in any repo, return the one with
        # highest precedence. This is for commands like `spack edit`
        # that can operate on packages that don't exist yet.
        selected = self.first_repo()
        if selected is None:
            raise UnknownPackageError(name)
        return selected

    def get(self, spec: "spack.spec.Spec") -> "spack.package_base.PackageBase":
        """Returns the package associated with the supplied spec."""
        msg = "RepoPath.get can only be called on concrete specs"
        assert isinstance(spec, spack.spec.Spec) and spec.concrete, msg
        return self.repo_for_pkg(spec).get(spec)

    def python_paths(self) -> List[str]:
        """Return a list of all the Python paths in the repos."""
        return [repo.python_path for repo in self.repos if repo.python_path]

    def get_pkg_class(self, pkg_name: str) -> Type["spack.package_base.PackageBase"]:
        """Find a class for the spec's package and return the class object."""
        return self.repo_for_pkg(pkg_name).get_pkg_class(pkg_name)

    @autospec
    def dump_provenance(self, spec, path):
        """Dump provenance information for a spec to a particular path.

        This dumps the package file and any associated patch files.
        Raises UnknownPackageError if not found.
        """
        return self.repo_for_pkg(spec).dump_provenance(spec, path)

    def dirname_for_package_name(self, pkg_name: str) -> str:
        return self.repo_for_pkg(pkg_name).dirname_for_package_name(pkg_name)

    def filename_for_package_name(self, pkg_name: str) -> str:
        return self.repo_for_pkg(pkg_name).filename_for_package_name(pkg_name)

    def exists(self, pkg_name: str) -> bool:
        """Whether package with the give name exists in the path's repos.

        Note that virtual packages do not "exist".
        """
        return any(repo.exists(pkg_name) for repo in self.repos)

    def _have_name(self, pkg_name: str) -> bool:
        have_name = pkg_name is not None
        if have_name and not isinstance(pkg_name, str):
            raise ValueError(f"is_virtual(): expected package name, got {type(pkg_name)}")
        return have_name

    def is_virtual(self, pkg_name: str) -> bool:
        """Return True if the package with this name is virtual, False otherwise.

        This function use the provider index. If calling from a code block that
        is used to construct the provider index use the ``is_virtual_safe`` function.

        Args:
            pkg_name (str): name of the package we want to check
        """
        have_name = self._have_name(pkg_name)
        return have_name and pkg_name in self.provider_index

    def is_virtual_safe(self, pkg_name: str) -> bool:
        """Return True if the package with this name is virtual, False otherwise.

        This function doesn't use the provider index.

        Args:
            pkg_name (str): name of the package we want to check
        """
        have_name = self._have_name(pkg_name)
        return have_name and (not self.exists(pkg_name) or self.get_pkg_class(pkg_name).virtual)

    def __contains__(self, pkg_name):
        return self.exists(pkg_name)

    def marshal(self):
        return (self.repos,)

    @staticmethod
    def unmarshal(repos):
        return RepoPath(*repos)

    def __reduce__(self):
        return RepoPath.unmarshal, self.marshal()


def _parse_package_api_version(
    config: Dict[str, Any],
    min_api: Tuple[int, int] = spack.min_package_api_version,
    max_api: Tuple[int, int] = spack.package_api_version,
) -> Tuple[int, int]:
    api = config.get("api")
    if api is None:
        package_api = (1, 0)
    else:
        if not isinstance(api, str):
            raise BadRepoError(f"Invalid Package API version '{api}'. Must be of the form vX.Y")
        api_match = _API_REGEX.match(api)
        if api_match is None:
            raise BadRepoError(f"Invalid Package API version '{api}'. Must be of the form vX.Y")
        package_api = (int(api_match.group(1)), int(api_match.group(2)))

    if min_api <= package_api <= max_api:
        return package_api

    min_str = ".".join(str(i) for i in min_api)
    max_str = ".".join(str(i) for i in max_api)
    curr_str = ".".join(str(i) for i in package_api)
    raise BadRepoError(
        f"Package API v{curr_str} is not supported by this version of Spack ("
        f"must be between v{min_str} and v{max_str})"
    )


def _validate_and_normalize_subdir(subdir: Any, root: str, package_api: Tuple[int, int]) -> str:
    if not isinstance(subdir, str):
        raise BadRepoError(f"Invalid subdirectory '{subdir}' in '{root}'. Must be a string")

    if package_api < (2, 0):
        return subdir  # In v1.x we did not validate subdir names

    if subdir in (".", ""):
        raise BadRepoError(
            f"Invalid subdirectory '{subdir}' in '{root}'. Use a symlink packages -> . instead"
        )

    # Otherwise we expect a directory name (not path) that can be used as a Python module.
    if os.sep in subdir:
        raise BadRepoError(
            f"Invalid subdirectory '{subdir}' in '{root}'. Expected a directory name, not a path"
        )
    if not nm.valid_module_name(subdir, package_api):
        raise BadRepoError(
            f"Invalid subdirectory '{subdir}' in '{root}'. Must be a valid Python module name"
        )
    return subdir


class Repo:
    """Class representing a package repository in the filesystem.

    Each package repository must have a top-level configuration file called `repo.yaml`.

    It contains the following keys:

    `namespace`:
        A Python namespace where the repository's packages should live.

    `subdirectory`:
        An optional subdirectory name where packages are placed

    `api`:
        A string of the form vX.Y that indicates the Package API version. The default is "v1.0".
        For the repo to be compatible with the current version of Spack, the version must be
        greater than or equal to :py:data:`spack.min_package_api_version` and less than or equal to
        :py:data:`spack.package_api_version`.
    """

    namespace: str

    def __init__(
        self,
        root: str,
        *,
        cache: spack.util.file_cache.FileCache,
        overrides: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Instantiate a package repository from a filesystem path.

        Args:
            root: the root directory of the repository
            cache: file cache associated with this repository
            overrides: dict mapping package name to class attribute overrides for that package
        """
        # Root directory, containing _repo.yaml and package dirs
        # Allow roots to by spack-relative by starting with '$spack'
        self.root = spack.util.path.canonicalize_path(root)

        # check and raise BadRepoError on fail.
        def check(condition, msg):
            if not condition:
                raise BadRepoError(msg)

        # Validate repository layout.
        self.config_file = os.path.join(self.root, repo_config_name)
        check(os.path.isfile(self.config_file), f"No {repo_config_name} found in '{root}'")

        # Read configuration and validate namespace
        config = self._read_config()

        self.package_api = _parse_package_api_version(config)
        self.subdirectory = _validate_and_normalize_subdir(
            config.get("subdirectory", packages_dir_name), root, self.package_api
        )
        self.packages_path = os.path.join(self.root, self.subdirectory)

        check(
            os.path.isdir(self.packages_path),
            f"No directory '{self.subdirectory}' found in '{root}'",
        )

        # The parent dir of spack_repo/ which should be added to sys.path for api v2.x
        self.python_path: Optional[str] = None

        if self.package_api < (2, 0):
            check(
                "namespace" in config,
                f"{os.path.join(root, repo_config_name)} must define a namespace.",
            )
            self.namespace = config["namespace"]
            # Note: for Package API v1.x the namespace validation always had bugs, which won't be
            # fixed for compatibility reasons. The regex is missing "$" at the end, and it claims
            # to test for valid identifiers, but fails to split on `.` first.
            check(
                isinstance(self.namespace, str)
                and re.match(r"[a-zA-Z][a-zA-Z0-9_.]+", self.namespace),
                f"Invalid namespace '{self.namespace}' in repo '{self.root}'. "
                "Namespaces must be valid python identifiers separated by '.'",
            )
        else:
            # From Package API v2.0 the namespace follows from the directory structure.
            check(
                f"{os.sep}spack_repo{os.sep}" in self.root,
                f"Invalid repository path '{self.root}'. Path must contain 'spack_repo{os.sep}'",
            )
            derived_namespace = self.root.rpartition(f"spack_repo{os.sep}")[2].replace(os.sep, ".")
            if "namespace" in config:
                self.namespace = config["namespace"]

                check(
                    isinstance(self.namespace, str) and self.namespace == derived_namespace,
                    f"Namespace '{self.namespace}' should be {derived_namespace} or omitted in "
                    f"{os.path.join(root, repo_config_name)}",
                )
            else:
                self.namespace = derived_namespace

            # strip the namespace directories from the root path to get the python path
            # e.g. /my/pythonpath/spack_repo/x/y/z -> /my/pythonpath
            python_path = self.root
            for _ in self.namespace.split("."):
                python_path = os.path.dirname(python_path)
            self.python_path = os.path.dirname(python_path)

            # check that all subdirectories are valid module names
            check(
                all(nm.valid_module_name(x, self.package_api) for x in self.namespace.split(".")),
                f"Invalid namespace '{self.namespace}' in repo '{self.root}'",
            )

        # Set up 'full_namespace' to include the super-namespace
        if self.package_api < (2, 0):
            self.full_namespace = f"{PKG_MODULE_PREFIX_V1}{self.namespace}"
        elif self.subdirectory == ".":
            self.full_namespace = f"{PKG_MODULE_PREFIX_V2}{self.namespace}"
        else:
            self.full_namespace = f"{PKG_MODULE_PREFIX_V2}{self.namespace}.{self.subdirectory}"

        # Keep name components around for checking prefixes.
        self._names = self.full_namespace.split(".")

        # Class attribute overrides by package name
        self.overrides = overrides or {}

        # Maps that goes from package name to corresponding file stat
        self._fast_package_checker: Optional[FastPackageChecker] = None

        # Indexes for this repository, computed lazily
        self._repo_index: Optional[RepoIndex] = None
        self._cache = cache

    @property
    def package_api_str(self) -> str:
        return f"v{self.package_api[0]}.{self.package_api[1]}"

    def real_name(self, import_name: str) -> Optional[str]:
        """Allow users to import Spack packages using Python identifiers.

        In Package API v1.x, there was no canonical module name for a package, and package's dir
        was not necessarily a valid Python module name. For that case we have to guess the actual
        package directory. From Package API v2.0 there is a one-to-one mapping between Spack
        package names and Python module names, so there is no guessing.

        For Packge API v1.x we support the following one-to-many mappings:
            num3proxy -> 3proxy
            foo_bar -> foo_bar, foo-bar
            foo_bar_baz -> foo_bar_baz, foo-bar-baz, foo_bar-baz, foo-bar_baz
        """
        if self.package_api >= (2, 0):
            if nm.pkg_dir_to_pkg_name(import_name, package_api=self.package_api) in self:
                return import_name
            return None

        if import_name in self:
            return import_name

        # For v1 generate the possible package names from a module name, and return the first
        # package name that exists in this repo.
        options = nm.possible_spack_module_names(import_name)
        try:
            options.remove(import_name)
        except ValueError:
            pass
        for name in options:
            if name in self:
                return name
        return None

    def is_prefix(self, fullname: str) -> bool:
        """True if fullname is a prefix of this Repo's namespace."""
        parts = fullname.split(".")
        return self._names[: len(parts)] == parts

    def _read_config(self) -> Dict[str, Any]:
        """Check for a YAML config file in this db's root directory."""
        try:
            with open(self.config_file, encoding="utf-8") as reponame_file:
                yaml_data = syaml.load(reponame_file)

                if (
                    not yaml_data
                    or "repo" not in yaml_data
                    or not isinstance(yaml_data["repo"], dict)
                ):
                    tty.die(f"Invalid {repo_config_name} in repository {self.root}")

                return yaml_data["repo"]

        except OSError:
            tty.die(f"Error reading {self.config_file} when opening {self.root}")

    def get(self, spec: "spack.spec.Spec") -> "spack.package_base.PackageBase":
        """Returns the package associated with the supplied spec."""
        msg = "Repo.get can only be called on concrete specs"
        assert isinstance(spec, spack.spec.Spec) and spec.concrete, msg
        # NOTE: we only check whether the package is None here, not whether it
        # actually exists, because we have to load it anyway, and that ends up
        # checking for existence. We avoid constructing FastPackageChecker,
        # which will stat all packages.
        if spec.name is None:
            raise UnknownPackageError(None, self)

        if spec.namespace and spec.namespace != self.namespace:
            raise UnknownPackageError(spec.name, self.namespace)

        package_class = self.get_pkg_class(spec.name)
        try:
            return package_class(spec)
        except spack.error.SpackError:
            # pass these through as their error messages will be fine.
            raise
        except Exception as e:
            # Make sure other errors in constructors hit the error
            # handler by wrapping them
            tty.debug(e)
            raise FailedConstructorError(spec.fullname, *sys.exc_info()) from e

    @autospec
    def dump_provenance(self, spec: "spack.spec.Spec", path: str) -> None:
        """Dump provenance information for a spec to a particular path.

        This dumps the package file and any associated patch files.
        Raises UnknownPackageError if not found.
        """
        if spec.namespace and spec.namespace != self.namespace:
            raise UnknownPackageError(
                f"Repository {self.namespace} does not contain package {spec.fullname}."
            )

        package_path = self.filename_for_package_name(spec.name)
        if not os.path.exists(package_path):
            # Spec has no files (e.g., package, patches) to copy
            tty.debug(f"{spec.name} does not have a package to dump")
            return

        # Install patch files needed by the (concrete) package.
        fs.mkdirp(path)
        if spec.concrete:
            for patch in itertools.chain.from_iterable(spec.package.patches.values()):
                if patch.path:
                    if os.path.exists(patch.path):
                        fs.install(patch.path, path)
                    else:
                        warnings.warn(f"Patch file did not exist: {patch.path}")

        # Install the package.py file itself.
        fs.install(self.filename_for_package_name(spec.name), path)

    @property
    def index(self) -> RepoIndex:
        """Construct the index for this repo lazily."""
        if self._repo_index is None:
            self._repo_index = RepoIndex(self._pkg_checker, self.namespace, cache=self._cache)
            self._repo_index.add_indexer("providers", ProviderIndexer(self))
            self._repo_index.add_indexer("tags", TagIndexer(self))
            self._repo_index.add_indexer("patches", PatchIndexer(self))
        return self._repo_index

    @property
    def provider_index(self) -> spack.provider_index.ProviderIndex:
        """A provider index with names *specific* to this repo."""
        return self.index["providers"]

    @property
    def tag_index(self) -> spack.tag.TagIndex:
        """Index of tags and which packages they're defined on."""
        return self.index["tags"]

    @property
    def patch_index(self) -> spack.patch.PatchCache:
        """Index of patches and packages they're defined on."""
        return self.index["patches"]

    @autospec
    def providers_for(self, vpkg_spec: "spack.spec.Spec") -> List["spack.spec.Spec"]:
        providers = self.provider_index.providers_for(vpkg_spec)
        if not providers:
            raise UnknownPackageError(vpkg_spec.fullname)
        return providers

    @autospec
    def extensions_for(
        self, extendee_spec: "spack.spec.Spec"
    ) -> List["spack.package_base.PackageBase"]:
        result = [pkg_cls(spack.spec.Spec(pkg_cls.name)) for pkg_cls in self.all_package_classes()]
        return [x for x in result if x.extends(extendee_spec)]

    def dirname_for_package_name(self, pkg_name: str) -> str:
        """Given a package name, get the directory containing its package.py file."""
        _, unqualified_name = self.partition_package_name(pkg_name)
        return os.path.join(
            self.packages_path, nm.pkg_name_to_pkg_dir(unqualified_name, self.package_api)
        )

    def filename_for_package_name(self, pkg_name: str) -> str:
        """Get the filename for the module we should load for a particular
        package.  Packages for a Repo live in
        ``$root/<package_name>/package.py``

        This will return a proper package.py path even if the
        package doesn't exist yet, so callers will need to ensure
        the package exists before importing.
        """
        pkg_dir = self.dirname_for_package_name(pkg_name)
        return os.path.join(pkg_dir, package_file_name)

    @property
    def _pkg_checker(self) -> FastPackageChecker:
        if self._fast_package_checker is None:
            self._fast_package_checker = FastPackageChecker(self.packages_path, self.package_api)
        return self._fast_package_checker

    def all_package_names(self, include_virtuals: bool = False) -> List[str]:
        """Returns a sorted list of all package names in the Repo."""
        names = sorted(self._pkg_checker.keys())
        if include_virtuals:
            return names
        return [x for x in names if not self.is_virtual(x)]

    def package_path(self, name: str) -> str:
        """Get path to package.py file for this repo."""
        return os.path.join(
            self.packages_path, nm.pkg_name_to_pkg_dir(name, self.package_api), package_file_name
        )

    def all_package_paths(self) -> Generator[str, None, None]:
        for name in self.all_package_names():
            yield self.package_path(name)

    def packages_with_tags(self, *tags: str) -> Set[str]:
        v = set(self.all_package_names())
        v.intersection_update(*(self.tag_index[tag.lower()] for tag in tags))
        return v

    def all_package_classes(self) -> Generator[Type["spack.package_base.PackageBase"], None, None]:
        """Iterator over all package *classes* in the repository.

        Use this with care, because loading packages is slow.
        """
        for name in self.all_package_names():
            yield self.get_pkg_class(name)

    def exists(self, pkg_name: str) -> bool:
        """Whether a package with the supplied name exists."""
        if pkg_name is None:
            return False

        # if the FastPackageChecker is already constructed, use it
        if self._fast_package_checker:
            return pkg_name in self._pkg_checker

        # if not, check for the package.py file
        path = self.filename_for_package_name(pkg_name)
        return os.path.exists(path)

    def last_mtime(self):
        """Time a package file in this repo was last updated."""
        return self._pkg_checker.last_mtime()

    def is_virtual(self, pkg_name: str) -> bool:
        """Return True if the package with this name is virtual, False otherwise.

        This function use the provider index. If calling from a code block that
        is used to construct the provider index use the ``is_virtual_safe`` function.
        """
        return pkg_name in self.provider_index

    def is_virtual_safe(self, pkg_name: str) -> bool:
        """Return True if the package with this name is virtual, False otherwise.

        This function doesn't use the provider index.
        """
        return not self.exists(pkg_name) or self.get_pkg_class(pkg_name).virtual

    def get_pkg_class(self, pkg_name: str) -> Type["spack.package_base.PackageBase"]:
        """Get the class for the package out of its module.

        First loads (or fetches from cache) a module for the
        package. Then extracts the package class from the module
        according to Spack's naming convention.
        """
        _, pkg_name = self.partition_package_name(pkg_name)
        fullname = f"{self.full_namespace}.{nm.pkg_name_to_pkg_dir(pkg_name, self.package_api)}"
        if self.package_api >= (2, 0):
            fullname += ".package"

        class_name = nm.pkg_name_to_class_name(pkg_name)

        try:
            module = importlib.import_module(fullname)
        except ImportError as e:
            raise UnknownPackageError(fullname) from e
        except Exception as e:
            msg = f"cannot load package '{pkg_name}' from the '{self.namespace}' repository: {e}"
            raise RepoError(msg) from e

        cls = getattr(module, class_name)
        if not isinstance(cls, type):
            tty.die(f"{pkg_name}.{class_name} is not a class")

        # Clear any prior changes to class attributes in case the class was loaded from the
        # same repo, but with different overrides
        overridden_attrs = getattr(cls, "overridden_attrs", {})
        attrs_exclusively_from_config = getattr(cls, "attrs_exclusively_from_config", [])
        for key, val in overridden_attrs.items():
            setattr(cls, key, val)
        for key in attrs_exclusively_from_config:
            delattr(cls, key)

        # Keep track of every class attribute that is overridden: if different overrides
        # dictionaries are used on the same physical repo, we make sure to restore the original
        # config values
        new_overridden_attrs = {}
        new_attrs_exclusively_from_config = set()
        for key, val in self.overrides.get(pkg_name, {}).items():
            if hasattr(cls, key):
                new_overridden_attrs[key] = getattr(cls, key)
            else:
                new_attrs_exclusively_from_config.add(key)

            setattr(cls, key, val)
        if new_overridden_attrs:
            setattr(cls, "overridden_attrs", dict(new_overridden_attrs))
        elif hasattr(cls, "overridden_attrs"):
            delattr(cls, "overridden_attrs")
        if new_attrs_exclusively_from_config:
            setattr(cls, "attrs_exclusively_from_config", new_attrs_exclusively_from_config)
        elif hasattr(cls, "attrs_exclusively_from_config"):
            delattr(cls, "attrs_exclusively_from_config")

        return cls

    def partition_package_name(self, pkg_name: str) -> Tuple[str, str]:
        namespace, pkg_name = partition_package_name(pkg_name)
        if namespace and (namespace != self.namespace):
            raise InvalidNamespaceError(
                f"Invalid namespace for the '{self.namespace}' repo: {namespace}"
            )

        return namespace, pkg_name

    def __str__(self) -> str:
        return f"Repo '{self.namespace}' at {self.root}"

    def __repr__(self) -> str:
        return self.__str__()

    def __contains__(self, pkg_name: str) -> bool:
        return self.exists(pkg_name)

    @staticmethod
    def unmarshal(root, cache, overrides):
        """Helper method to unmarshal keyword arguments"""
        return Repo(root, cache=cache, overrides=overrides)

    def marshal(self):
        cache = self._cache
        if isinstance(cache, llnl.util.lang.Singleton):
            cache = cache.instance
        return self.root, cache, self.overrides

    def __reduce__(self):
        return Repo.unmarshal, self.marshal()


RepoType = Union[Repo, RepoPath]


def partition_package_name(pkg_name: str) -> Tuple[str, str]:
    """Given a package name that might be fully-qualified, returns the namespace part,
    if present and the unqualified package name.

    If the package name is unqualified, the namespace is an empty string.

    Args:
        pkg_name: a package name, either unqualified like "llvl", or
            fully-qualified, like "builtin.llvm"
    """
    namespace, _, pkg_name = pkg_name.rpartition(".")
    return namespace, pkg_name


def get_repo_yaml_dir(
    root: str, namespace: Optional[str], package_api: Tuple[int, int]
) -> Tuple[str, str]:
    """Returns the directory where repo.yaml is located and the effective namespace."""
    if package_api < (2, 0):
        namespace = namespace or os.path.basename(root)
        # This ad-hoc regex is left for historical reasons, and should not have a breaking change.
        if not re.match(r"\w[\.\w-]*", namespace):
            raise InvalidNamespaceError(f"'{namespace}' is not a valid namespace.")
        return root, namespace

    # Package API v2 has <root>/spack_repo/<namespace>/<subdir> structure and requires a namespace
    if namespace is None:
        raise InvalidNamespaceError("Namespace must be provided.")

    # if namespace has dots those translate to subdirs of further namespace packages.
    namespace_components = namespace.split(".")

    if not all(nm.valid_module_name(n, package_api=package_api) for n in namespace_components):
        raise InvalidNamespaceError(f"'{namespace}' is not a valid namespace." % namespace)

    return os.path.join(root, "spack_repo", *namespace_components), namespace


def create_repo(
    root,
    namespace: Optional[str] = None,
    subdir: str = packages_dir_name,
    package_api: Tuple[int, int] = spack.package_api_version,
) -> Tuple[str, str]:
    """Create a new repository in root with the specified namespace.

    If the namespace is not provided, use basename of root.
    Return the canonicalized path and namespace of the created repository.
    """
    root = spack.util.path.canonicalize_path(root)
    repo_yaml_dir, namespace = get_repo_yaml_dir(os.path.abspath(root), namespace, package_api)

    existed = True
    try:
        dir_entry = next(os.scandir(repo_yaml_dir), None)
    except OSError as e:
        if e.errno == errno.ENOENT:
            existed = False
            dir_entry = None
        else:
            raise BadRepoError(f"Cannot create new repo in {root}: {e}")

    if dir_entry is not None:
        raise BadRepoError(f"Cannot create new repo in {root}: directory is not empty.")

    config_path = os.path.join(repo_yaml_dir, repo_config_name)

    subdir = _validate_and_normalize_subdir(subdir, root, package_api)

    packages_path = os.path.join(repo_yaml_dir, subdir)

    try:
        fs.mkdirp(packages_path)
        with open(config_path, "w", encoding="utf-8") as config:
            config.write("repo:\n")
            config.write(f"  namespace: '{namespace}'\n")
            if subdir != packages_dir_name:
                config.write(f"  subdirectory: '{subdir}'\n")
            x, y = package_api
            config.write(f"  api: v{x}.{y}\n")

    except OSError as e:
        # try to clean up.
        if existed:
            shutil.rmtree(config_path, ignore_errors=True)
            shutil.rmtree(packages_path, ignore_errors=True)
        else:
            shutil.rmtree(root, ignore_errors=True)

        raise BadRepoError(
            "Failed to create new repository in %s." % root, "Caused by %s: %s" % (type(e), e)
        ) from e

    return repo_yaml_dir, namespace


def from_path(path: str) -> Repo:
    """Constructs a Repo using global misc cache."""
    return Repo(path, cache=spack.caches.MISC_CACHE)


MaybeExecutable = Optional[spack.util.executable.Executable]


class RepoDescriptor:
    """Abstract base class for repository data."""

    def __init__(self, name: Optional[str]) -> None:
        self.name = name

    @property
    def _maybe_name(self) -> str:
        """Return the name if it exists, otherwise an empty string."""
        return f"{self.name}: " if self.name else ""

    def initialize(self, fetch: bool = True, git: MaybeExecutable = None) -> None:
        return None

    def update(self, git: MaybeExecutable = None, remote: str = "origin") -> None:
        return None

    def construct(
        self, cache: spack.util.file_cache.FileCache, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Union[Repo, Exception]]:
        """Construct Repo instances from the descriptor."""
        raise RuntimeError("construct() must be implemented in subclasses")


class LocalRepoDescriptor(RepoDescriptor):
    def __init__(self, name: Optional[str], path: str) -> None:
        super().__init__(name)
        self.path = path

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, path={self.path!r})"

    def construct(
        self, cache: spack.util.file_cache.FileCache, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Union[Repo, Exception]]:
        try:
            return {self.path: Repo(self.path, cache=cache, overrides=overrides)}
        except RepoError as e:
            return {self.path: e}


class RemoteRepoDescriptor(RepoDescriptor):
    def __init__(
        self,
        *,
        name: Optional[str],
        repository: str,
        branch: Optional[str],
        commit: Optional[str],
        tag: Optional[str],
        destination: str,
        relative_paths: Optional[List[str]],
        lock: spack.util.lock.Lock,
    ) -> None:
        super().__init__(name)
        self.repository = repository
        self.branch = branch
        self.commit = commit
        self.tag = tag
        self.destination = destination
        self.relative_paths = relative_paths
        self.error: Optional[str] = None
        self.write_transaction = spack.util.lock.WriteTransaction(lock)
        self.read_transaction = spack.util.lock.ReadTransaction(lock)

    def _fetched(self) -> bool:
        """Check if the repository has been fetched by looking for the .git
        directory or file (when a submodule)."""
        return os.path.exists(os.path.join(self.destination, ".git"))

    def fetched(self) -> bool:
        with self.read_transaction:
            return self._fetched()
        return False

    def _clone_or_pull(
        self,
        git: spack.util.executable.Executable,
        update: bool = False,
        remote: str = "origin",
        depth: int = 20,
    ) -> None:
        with self.write_transaction:
            try:
                with fs.working_dir(self.destination, create=True):
                    # do not fetch if the package repository was fetched by another
                    # process while we were waiting for the lock
                    fetched = self._fetched()
                    if fetched and not update:
                        self.read_index_file()
                        return

                    # setup the repository if it does not exist
                    if not fetched:
                        spack.util.git.init_git_repo(self.repository, remote=remote, git_exe=git)

                        # determine the default branch from ls-remote
                        refs = git("ls-remote", "--symref", remote, "HEAD", output=str)
                        ref_match = re.search(r"refs/heads/(\S+)", refs)
                        if not ref_match:
                            self.error = f"Unable to locate a default branch for {self.repository}"
                            return
                        self.branch = ref_match.group(1)

                    # determine the branch and remote if no config values exist
                    elif not (self.commit or self.tag or self.branch):
                        self.branch = git("rev-parse", "--abbrev-ref", "HEAD", output=str).strip()
                        remote = git("config", f"branch.{self.branch}.remote", output=str).strip()

                    if self.commit:
                        spack.util.git.pull_checkout_commit(self.commit, git_exe=git)

                    elif self.tag:
                        spack.util.git.pull_checkout_tag(self.tag, remote, depth, git_exe=git)

                    elif self.branch:
                        # if the branch already exists we should use the
                        # previously configured remote
                        try:
                            output = git("config", f"branch.{self.branch}.remote", output=str)
                            remote = output.strip()
                        except spack.util.executable.ProcessError:
                            pass
                        spack.util.git.pull_checkout_branch(
                            self.branch, remote=remote, depth=depth, git_exe=git
                        )

            except spack.util.executable.ProcessError:
                self.error = f"Failed to {'update' if update else 'clone'} repository {self.name}"
                return

            self.read_index_file()

    def update(self, git: MaybeExecutable = None, remote: str = "origin") -> None:
        if git is None:
            raise RepoError("Git executable not found")

        self._clone_or_pull(git, update=True, remote=remote)

        if self.error:
            raise RepoError(self.error)

    def initialize(self, fetch: bool = True, git: MaybeExecutable = None) -> None:
        """Clone the remote repository if it has not been fetched yet and read the index file
        if necessary."""
        if self.fetched():
            self.read_index_file()
            return

        if not fetch:
            return

        if not git:
            self.error = "Git executable not found"
            return

        self._clone_or_pull(git)

    def read_index_file(self) -> None:
        if self.relative_paths is not None:
            return

        repo_index_file = os.path.join(self.destination, SPACK_REPO_INDEX_FILE_NAME)
        try:
            with open(repo_index_file, encoding="utf-8") as f:
                index_data = syaml.load(f)
            assert "repo_index" in index_data, "missing 'repo_index' key"
            repo_index = index_data["repo_index"]
            assert isinstance(repo_index, dict), "'repo_index' must be a dictionary"
            assert "paths" in repo_index, "missing 'paths' key in 'repo_index'"
            sub_paths = repo_index["paths"]
            assert isinstance(sub_paths, list), "'paths' under 'repo_index' must be a list"
        except (OSError, syaml.SpackYAMLError, AssertionError) as e:
            self.error = f"failed to read {repo_index_file}: {e}"
            return

        # validate that this is a list of relative paths.
        if not isinstance(sub_paths, list) or not all(isinstance(p, str) for p in sub_paths):
            self.error = "invalid repo index file format: expected a list of relative paths."
            return

        self.relative_paths = sub_paths

    def __repr__(self):
        return (
            f"RemoteRepoDescriptor(name={self.name!r}, "
            f"repository={self.repository!r}, "
            f"destination={self.destination!r}, "
            f"relative_paths={self.relative_paths!r})"
        )

    def construct(
        self, cache: spack.util.file_cache.FileCache, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Union[Repo, Exception]]:
        if self.error:
            return {self.destination: Exception(self.error)}

        repos: Dict[str, Union[Repo, Exception]] = {}
        for subpath in self.relative_paths or []:
            if os.path.isabs(subpath):
                repos[self.destination] = Exception(
                    f"Repository subpath '{subpath}' must be relative"
                )
                continue
            path = os.path.join(self.destination, subpath)
            try:
                repos[path] = Repo(path, cache=cache, overrides=overrides)
            except RepoError as e:
                repos[path] = e
        return repos


class BrokenRepoDescriptor(RepoDescriptor):
    """A descriptor for a broken repository, used to indicate errors in the configuration that
    aren't fatal untill the repository is used."""

    def __init__(self, name: Optional[str], error: str) -> None:
        super().__init__(name)
        self.error = error

    def initialize(
        self, fetch: bool = True, git: Optional[spack.util.executable.Executable] = None
    ) -> None:
        pass

    def construct(
        self, cache: spack.util.file_cache.FileCache, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Union[Repo, Exception]]:
        return {self.name or "<unknown>": Exception(self.error)}


class RepoDescriptors(Mapping[str, RepoDescriptor]):
    """A collection of repository descriptors."""

    def __init__(self, descriptors: Dict[str, RepoDescriptor]) -> None:
        self.descriptors = descriptors

    def __getitem__(self, name: str) -> RepoDescriptor:
        return self.descriptors[name]

    def __iter__(self):
        return iter(self.descriptors.keys())

    def __len__(self):
        return len(self.descriptors)

    def __contains__(self, name) -> bool:
        return name in self.descriptors

    def __repr__(self):
        return f"RepoDescriptors({self.descriptors!r})"

    @staticmethod
    def from_config(
        lock: spack.util.lock.Lock, config: spack.config.Configuration, scope=None
    ) -> "RepoDescriptors":
        return RepoDescriptors(
            {
                name: parse_config_descriptor(name, cfg, lock)
                for name, cfg in config.get("repos", scope=scope).items()
            }
        )

    def construct(
        self,
        cache: spack.util.file_cache.FileCache,
        fetch: bool = True,
        find_git: Callable[[], MaybeExecutable] = lambda: spack.util.git.git(required=True),
        overrides: Optional[Dict[str, Any]] = None,
    ) -> Tuple[RepoPath, Dict[str, Exception]]:
        """Construct a RepoPath from the descriptors.

        If init is True, initialize all remote repositories that have not been fetched yet.

        Returns:
            A tuple containing a RepoPath instance with all constructed Repos and a dictionary
            mapping paths to exceptions that occurred during construction.
        """
        repos: List[Repo] = []
        errors: Dict[str, Exception] = {}
        git: MaybeExecutable = None

        for descriptor in self.descriptors.values():
            if fetch and isinstance(descriptor, RemoteRepoDescriptor):
                git = git or find_git()
                descriptor.initialize(fetch=True, git=git)
            else:
                descriptor.initialize(fetch=False)

            for path, result in descriptor.construct(cache=cache, overrides=overrides).items():
                if isinstance(result, Repo):
                    repos.append(result)
                else:
                    errors[path] = result

        return RepoPath(*repos), errors


def parse_config_descriptor(
    name: Optional[str], descriptor: Any, lock: spack.util.lock.Lock
) -> RepoDescriptor:
    """Parse a repository descriptor from validated configuration. This does not instantiate Repo
    objects, but merely turns the config into a more useful RepoDescriptor instance.

    Args:
        name: the name of the repository, used for error messages
        descriptor: the configuration for the repository, which can be a string (local path),
            or a dictionary with 'git' key containing git URL and other options.

    Returns:
        A RepoDescriptor instance, either LocalRepoDescriptor or RemoteRepoDescriptor.

    Raises:
        BadRepoError: if the descriptor is invalid or cannot be parsed.
        RuntimeError: if the descriptor is of an unexpected type.

    """
    if isinstance(descriptor, str):
        return LocalRepoDescriptor(name, spack.util.path.canonicalize_path(descriptor))

    # Should be the case due to config validation.
    assert isinstance(descriptor, dict), "Repository descriptor must be a string or a dictionary"

    # Configuration validation works per scope, and we want to allow overriding e.g. destination
    # in user config without the user having to repeat the `git` key and value again. This is a
    # hard error, since config validation is a hard error.
    if "git" not in descriptor:
        raise RuntimeError(
            f"Invalid configuration for repository '{name}': {descriptor!r}. A `git` attribute is "
            "required for remote repositories."
        )

    repository = descriptor["git"]
    assert isinstance(repository, str), "Package repository git URL must be a string"

    destination = descriptor.get("destination", None)

    if destination is None:  # use a default destination
        dir_name = spack.util.hash.b32_hash(repository)[-7:]
        destination = os.path.join(spack.paths.package_repos_path, dir_name)
    else:
        destination = spack.util.path.canonicalize_path(destination)

    return RemoteRepoDescriptor(
        name=name,
        repository=repository,
        branch=descriptor.get("branch"),
        commit=descriptor.get("commit"),
        tag=descriptor.get("tag"),
        destination=destination,
        relative_paths=descriptor.get("paths"),
        lock=lock,
    )


def create_or_construct(
    root: str,
    namespace: Optional[str] = None,
    package_api: Tuple[int, int] = spack.package_api_version,
) -> Repo:
    """Create a repository, or just return a Repo if it already exists."""
    repo_yaml_dir, _ = get_repo_yaml_dir(root, namespace, package_api)
    if not os.path.exists(repo_yaml_dir):
        fs.mkdirp(root)
        create_repo(root, namespace=namespace, package_api=package_api)
    return from_path(repo_yaml_dir)


def create_and_enable(config: spack.config.Configuration) -> RepoPath:
    """Immediately call enable() on the created RepoPath instance."""
    repo_path = RepoPath.from_config(config)
    repo_path.enable()
    return repo_path


#: Global package repository instance.
PATH: RepoPath = llnl.util.lang.Singleton(
    lambda: create_and_enable(spack.config.CONFIG)
)  # type: ignore[assignment]


# Add the finder to sys.meta_path
REPOS_FINDER = ReposFinder()
sys.meta_path.append(REPOS_FINDER)


def all_package_names(include_virtuals=False):
    """Convenience wrapper around ``spack.repo.all_package_names()``."""
    return PATH.all_package_names(include_virtuals)


@contextlib.contextmanager
def use_repositories(
    *paths_and_repos: Union[str, Repo], override: bool = True
) -> Generator[RepoPath, None, None]:
    """Use the repositories passed as arguments within the context manager.

    Args:
        *paths_and_repos: paths to the repositories to be used, or
            already constructed Repo objects
        override: if True use only the repositories passed as input,
            if False add them to the top of the list of current repositories.
    Returns:
        Corresponding RepoPath object
    """
    paths = {getattr(x, "root", x): getattr(x, "root", x) for x in paths_and_repos}
    scope_name = f"use-repo-{uuid.uuid4()}"
    repos_key = "repos:" if override else "repos"
    spack.config.CONFIG.push_scope(
        spack.config.InternalConfigScope(name=scope_name, data={repos_key: paths})
    )
    old_repo, new_repo = PATH, RepoPath.from_config(spack.config.CONFIG)
    old_repo.disable()
    enable_repo(new_repo)
    try:
        yield new_repo
    finally:
        spack.config.CONFIG.remove_scope(scope_name=scope_name)
        enable_repo(old_repo)


def enable_repo(repo_path: RepoPath) -> None:
    """Set the global package repository and make them available in module search paths."""
    global PATH
    PATH = repo_path
    PATH.enable()


class MockRepositoryBuilder:
    """Build a mock repository in a directory"""

    def __init__(self, root_directory, namespace=None):
        namespace = namespace or "".join(random.choice(string.ascii_lowercase) for _ in range(10))
        repo_root = os.path.join(root_directory, namespace)
        os.mkdir(repo_root)
        self.root, self.namespace = create_repo(repo_root, namespace)

    def add_package(self, name, dependencies=None):
        """Create a mock package in the repository, using a Jinja2 template.

        Args:
            name (str): name of the new package
            dependencies (list): list of ("dep_spec", "dep_type", "condition") tuples.
                Both "dep_type" and "condition" can default to ``None`` in which case
                ``spack.dependency.default_deptype`` and ``spack.spec.Spec()`` are used.
        """
        dependencies = dependencies or []
        context = {"cls_name": nm.pkg_name_to_class_name(name), "dependencies": dependencies}
        template = spack.tengine.make_environment().get_template("mock-repository/package.pyt")
        text = template.render(context)
        package_py = self.recipe_filename(name)
        fs.mkdirp(os.path.dirname(package_py))
        with open(package_py, "w", encoding="utf-8") as f:
            f.write(text)

    def remove(self, name):
        package_py = self.recipe_filename(name)
        shutil.rmtree(os.path.dirname(package_py))

    def recipe_filename(self, name: str):
        return os.path.join(
            self.root, "packages", nm.pkg_name_to_pkg_dir(name, package_api=(2, 0)), "package.py"
        )


class RepoError(spack.error.SpackError):
    """Superclass for repository-related errors."""


class NoRepoConfiguredError(RepoError):
    """Raised when there are no repositories configured."""


class InvalidNamespaceError(RepoError):
    """Raised when an invalid namespace is encountered."""


class BadRepoError(RepoError):
    """Raised when repo layout is invalid."""


class UnknownEntityError(RepoError):
    """Raised when we encounter a package spack doesn't have."""


class UnknownPackageError(UnknownEntityError):
    """Raised when we encounter a package spack doesn't have."""

    def __init__(self, name, repo=None):
        msg = "Attempting to retrieve anonymous package."
        long_msg = None
        if name:
            if repo:
                msg = "Package '{0}' not found in repository '{1.root}'"
                msg = msg.format(name, repo)
            else:
                msg = "Package '{0}' not found.".format(name)

            # Special handling for specs that may have been intended as
            # filenames: prompt the user to ask whether they intended to write
            # './<name>'.
            if name.endswith(".yaml"):
                long_msg = "Did you mean to specify a filename with './{0}'?"
                long_msg = long_msg.format(name)
            else:
                long_msg = "Use 'spack create' to create a new package."

                if not repo:
                    repo = PATH

                # We need to compare the base package name
                pkg_name = name.rsplit(".", 1)[-1]
                try:
                    similar = difflib.get_close_matches(pkg_name, repo.all_package_names())
                except Exception:
                    similar = []

                if 1 <= len(similar) <= 5:
                    long_msg += "\n\nDid you mean one of the following packages?\n  "
                    long_msg += "\n  ".join(similar)

        super().__init__(msg, long_msg)
        self.name = name


class UnknownNamespaceError(UnknownEntityError):
    """Raised when we encounter an unknown namespace"""

    def __init__(self, namespace, name=None):
        msg, long_msg = f"Unknown namespace: {namespace}", None
        if name == "yaml":
            long_msg = f"Did you mean to specify a filename with './{namespace}.{name}'?"
        super().__init__(msg, long_msg)


class FailedConstructorError(RepoError):
    """Raised when a package's class constructor fails."""

    def __init__(self, name, exc_type, exc_obj, exc_tb):
        super().__init__(
            "Class constructor failed for package '%s'." % name,
            "\nCaused by:\n"
            + ("%s: %s\n" % (exc_type.__name__, exc_obj))
            + "".join(traceback.format_tb(exc_tb)),
        )
        self.name = name
