# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Data structures that represent Spack's dependency relationships."""

from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

import spack.deptypes as dt
import spack.spec

if TYPE_CHECKING:
    import spack.patch


#: Recipes declare the same requirement over and over: a trilinos solve holds 24.7k Dependency
#: objects with 11.4k distinct (spec, depflag) pairs.
_DEPENDENCY_CACHE: Dict[Tuple[str, dt.DepFlag], "Dependency"] = {}


def intern_dependency(dependency: "Dependency") -> "Dependency":
    """Return the shared Dependency equal to ``dependency``. Only unpatched dependencies are
    shared, since patches are attached per dependent package."""
    key = (str(dependency.spec), dependency.depflag)
    cached = _DEPENDENCY_CACHE.get(key)
    if cached is not None:
        return cached
    _DEPENDENCY_CACHE[key] = dependency
    return dependency


class Dependency:
    """Class representing metadata for a dependency on a package.

    This class differs from ``spack.spec.DependencySpec`` because it
    represents metadata at the ``Package`` level.
    ``spack.spec.DependencySpec`` is a descriptor for an actual package
    configuration, while ``Dependency`` is a descriptor for a package's
    dependency *requirements*.

    A dependency is a requirement for a configuration of another package
    that satisfies a particular spec.  The dependency can have *types*,
    which determine *how* that package configuration is required,
    e.g. whether it is required for building the package, whether it
    needs to be linked to, or whether it is needed at runtime so that
    Spack can call commands from it.

    A package can also depend on another package with *patches*. This is
    for cases where the maintainers of one package also maintain special
    patches for their dependencies.  If one package depends on another
    with patches, a special version of that dependency with patches
    applied will be built for use by the dependent package.  The patches
    are included in the new version's spec hash to differentiate it from
    unpatched versions of the same package, so that unpatched versions of
    the dependency package can coexist with the patched version.

    """

    __slots__ = "spec", "patches", "depflag"

    def __init__(self, spec: spack.spec.Spec, depflag: dt.DepFlag = dt.DEFAULT):
        """Create a new Dependency.

        Args:
            spec: Spec indicating dependency requirements
            depflag: flags describing the dependency relationship
        """
        self.spec = spec

        # Maps condition specs to lists of Patch objects, as the patches dict on packages
        # does. None until a patch is actually attached: only a handful of packages patch
        # their dependencies, and an empty dict per Dependency is a large share of the heap.
        self.patches: Optional[Dict[spack.spec.Spec, List["spack.patch.Patch"]]] = None
        self.depflag = depflag

    @property
    def name(self) -> str:
        """Get the name of the dependency package."""
        return self.spec.name

    def __repr__(self) -> str:
        types = dt.flag_to_chars(self.depflag)
        if self.patches:
            return f"<Dependency: {self.spec} [{types}, {self.patches}]>"
        else:
            return f"<Dependency: {self.spec} [{types}]>"
