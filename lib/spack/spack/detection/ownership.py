# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Find the packages that may own a library or an executable, from the patterns in their
recipes.
"""

import re
from typing import TYPE_CHECKING, Dict, Iterable, List, Pattern, Tuple, Type

import spack.package_base

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


class OwnershipIndex:
    """Maps the names of libraries and executables to the packages whose patterns match them.

    Names are matched with ``re.search``, as detection matches file names.
    """

    def __init__(self, pkgs: Iterable[Type["spack.package_base.PackageBase"]]) -> None:
        self._libraries: List[Tuple[str, List[Pattern]]] = []
        self._executables: List[Tuple[str, List[Pattern]]] = []
        finder = ExecutablesFinder()
        for pkg in pkgs:
            libraries = [re.compile(x) for x in library_patterns(pkg)]
            if libraries:
                self._libraries.append((pkg.name, libraries))
            executables = [re.compile(x) for x in finder.search_patterns(pkg=pkg)]
            if executables:
                self._executables.append((pkg.name, executables))
        self._library_owners: Dict[str, List[str]] = {}
        self._executable_owners: Dict[str, List[str]] = {}

    def library_owners(self, name: str) -> List[str]:
        """Returns the packages that may own a library loaded under ``name``, sorted by name."""
        if name not in self._library_owners:
            self._library_owners[name] = _owners(name, self._libraries)
        return self._library_owners[name]

    def executable_owners(self, name: str) -> List[str]:
        """Returns the packages that may own an executable named ``name``, sorted by name."""
        if name not in self._executable_owners:
            self._executable_owners[name] = _owners(name, self._executables)
        return self._executable_owners[name]


def _owners(name: str, patterns: List[Tuple[str, List[Pattern]]]) -> List[str]:
    return sorted(pkg for pkg, regexes in patterns if any(x.search(name) for x in regexes))


def ownership_index(repo: "spack.repo.RepoPath") -> OwnershipIndex:
    """Returns the ownership index of the detectable packages in ``repo``. Packages that cannot
    be detected own nothing, even when they set ``sonames``.
    """
    names = sorted(repo.packages_with_tags(spack.package_base.DetectablePackageMeta.TAG))
    return OwnershipIndex(repo.get_pkg_class(name) for name in names)
