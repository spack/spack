# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Find the packages that may own a library or an executable, from the patterns in their
recipes.
"""

import os
import re
from typing import TYPE_CHECKING, Dict, Iterable, List, NamedTuple, Optional, Pattern, Tuple, Type

import spack.package_base
import spack.util.tty

from .path import ExecutablesFinder

if TYPE_CHECKING:
    import spack.repo


def library_patterns(pkg: Type["spack.package_base.PackageBase"]) -> List[str]:
    """Returns the regexes matching the names of the libraries a package owns: its ``sonames``
    when the recipe sets them, otherwise its ``libraries``.
    """
    sonames = getattr(pkg, "sonames", None)
    if sonames is not None:
        return list(sonames)
    return list(getattr(pkg, "libraries", []))


class LibraryOwner(NamedTuple):
    """A package that owns a library or an executable."""

    name: str
    #: version that the recipe detects for the file, when the ownership is confirmed by the
    #: recipe's ``determine_version``
    version: Optional[str]


class OwnershipIndex:
    """Maps the names of libraries and executables to the packages whose patterns match them.

    Names are matched with ``re.search``, as detection matches file names.
    """

    def __init__(self, pkgs: Iterable[Type["spack.package_base.PackageBase"]]) -> None:
        self._libraries: List[Tuple[str, List[Pattern]]] = []
        self._executables: List[Tuple[str, List[Pattern]]] = []
        #: Packages that own libraries through their ``libraries`` attribute. These patterns
        #: select candidate files for detection, and are often prefixes such as ``libz``.
        self._detected_by_libraries: Dict[str, Type["spack.package_base.PackageBase"]] = {}
        #: Packages that own executables, by name
        self._detected_by_executables: Dict[str, Type["spack.package_base.PackageBase"]] = {}
        finder = ExecutablesFinder()
        for pkg in pkgs:
            if getattr(pkg, "sonames", None) is None and hasattr(pkg, "libraries"):
                self._detected_by_libraries[pkg.name] = pkg
            libraries = [re.compile(x) for x in library_patterns(pkg)]
            if libraries:
                self._libraries.append((pkg.name, libraries))
            executables = [re.compile(x) for x in finder.search_patterns(pkg=pkg)]
            if executables:
                self._executables.append((pkg.name, executables))
                self._detected_by_executables[pkg.name] = pkg
        self._library_owners: Dict[str, List[str]] = {}
        self._confirmed_library_owners: Dict[str, List[LibraryOwner]] = {}
        self._executable_owners: Dict[str, List[str]] = {}
        self._confirmed_executable_owners: Dict[str, List[LibraryOwner]] = {}

    def library_owners(self, name: str) -> List[str]:
        """Returns the packages that may own a library loaded under ``name``, sorted by name."""
        if name not in self._library_owners:
            self._library_owners[name] = _owners(name, self._libraries)
        return self._library_owners[name]

    def confirmed_library_owners(self, path: str, real_path: str) -> List[LibraryOwner]:
        """Returns the packages that own the library found at ``path``, sorted by name.

        A package that owns libraries through its ``libraries`` attribute owns the library only
        if its ``determine_version`` returns a version for it, as detection requires.

        Arguments:
            path: path the library was found at, whose base name is the name it was loaded under
            real_path: path of the library with symlinks resolved
        """
        if real_path not in self._confirmed_library_owners:
            result = []
            for name in self.library_owners(os.path.basename(path)):
                if name not in self._detected_by_libraries:
                    result.append(LibraryOwner(name=name, version=None))
                    continue
                version = _detected_version(self._detected_by_libraries[name], real_path, path)
                if version:
                    result.append(LibraryOwner(name=name, version=version))
            self._confirmed_library_owners[real_path] = result
        return self._confirmed_library_owners[real_path]

    def executable_owners(self, name: str) -> List[str]:
        """Returns the packages that may own an executable named ``name``, sorted by name."""
        if name not in self._executable_owners:
            self._executable_owners[name] = _owners(name, self._executables)
        return self._executable_owners[name]

    def confirmed_executable_owners(self, path: str) -> List[LibraryOwner]:
        """Returns the packages that own the executable at ``path``, sorted by name.

        A package owns the executable if its ``executables`` patterns match the name of the file,
        and its ``determine_version`` returns a version for it. Packages without
        ``determine_version`` own it on the patterns alone.
        """
        if path not in self._confirmed_executable_owners:
            result = []
            for name in self.executable_owners(os.path.basename(path)):
                pkg = self._detected_by_executables[name]
                if not hasattr(pkg, "determine_version"):
                    result.append(LibraryOwner(name=name, version=None))
                    continue
                version = _detected_version(pkg, path)
                if version:
                    result.append(LibraryOwner(name=name, version=version))
            self._confirmed_executable_owners[path] = result
        return self._confirmed_executable_owners[path]


def _detected_version(pkg: Type["spack.package_base.PackageBase"], *paths: str) -> Optional[str]:
    """Returns the version ``determine_version`` returns for the first path it accepts."""
    for path in paths:
        try:
            version = getattr(pkg, "determine_version")(path)
        except Exception as e:
            spack.util.tty.debug(f"Cannot detect the version of '{path}' [{e}]")
            continue
        if version:
            return version
    return None


def _owners(name: str, patterns: List[Tuple[str, List[Pattern]]]) -> List[str]:
    return sorted(pkg for pkg, regexes in patterns if any(x.search(name) for x in regexes))


def ownership_index(repo: "spack.repo.RepoPath") -> OwnershipIndex:
    """Returns the ownership index of the detectable packages in ``repo``. Packages that cannot
    be detected own nothing, even when they set ``sonames``.
    """
    names = sorted(repo.packages_with_tags(spack.package_base.DetectablePackageMeta.TAG))
    return OwnershipIndex(repo.get_pkg_class(name) for name in names)
