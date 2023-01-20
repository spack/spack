# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Data structures that represent Spack's dependency relationships."""
from typing import Dict, List, Optional, Set, Tuple, Union

import spack.spec

#: The types of dependency relationships that Spack understands.
all_deptypes = ("build", "link", "run", "test")

#: Default dependency type if none is specified
default_deptype = ("build", "link")

#: Type hint for the arguments accepting a dependency type
DependencyArgument = Union[str, List[str], Tuple[str, ...]]


def deptype_chars(*type_tuples: str) -> str:
    """Create a string representing deptypes for many dependencies.

    The string will be some subset of 'blrt', like 'bl ', 'b t', or
    ' lr ' where each letter in 'blrt' stands for 'build', 'link',
    'run', and 'test' (the dependency types).

    For a single dependency, this just indicates that the dependency has
    the indicated deptypes. For a list of dependnecies, this shows
    whether ANY dpeendency in the list has the deptypes (so the deptypes
    are merged).
    """
    types: Set[str] = set()
    for t in type_tuples:
        if t:
            types.update(t)

    return "".join(t[0] if t in types else " " for t in all_deptypes)


def canonical_deptype(deptype: DependencyArgument) -> Tuple[str, ...]:
    """Convert deptype to a canonical sorted tuple, or raise ValueError.

    Args:
        deptype: string representing dependency type, or a list/tuple of such strings.
            Can also be the builtin function ``all`` or the string 'all', which result in
            a tuple of all dependency types known to Spack.
    """
    if deptype in ("all", all):
        return all_deptypes

    elif isinstance(deptype, str):
        if deptype not in all_deptypes:
            raise ValueError("Invalid dependency type: %s" % deptype)
        return (deptype,)

    elif isinstance(deptype, (tuple, list, set)):
        bad = [d for d in deptype if d not in all_deptypes]
        if bad:
            raise ValueError("Invalid dependency types: %s" % ",".join(str(t) for t in bad))
        return tuple(sorted(set(deptype)))

    raise ValueError("Invalid dependency type: %s" % repr(deptype))


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

    def __init__(
        self,
        pkg: "spack.package_base.PackageBase",
        spec: "spack.spec.Spec",
        type: Optional[Tuple[str, ...]] = default_deptype,
    ):
        """Create a new Dependency.

        Args:
            pkg: Package that has this dependency
            spec: Spec indicating dependency requirements
            type: strings describing dependency relationship
        """
        assert isinstance(spec, spack.spec.Spec)

        self.pkg = pkg
        self.spec = spec.copy()

        # This dict maps condition specs to lists of Patch objects, just
        # as the patches dict on packages does.
        self.patches: Dict[spack.spec.Spec, "List[spack.patch.Patch]"] = {}

        if type is None:
            self.type = set(default_deptype)
        else:
            self.type = set(type)

    @property
    def name(self) -> str:
        """Get the name of the dependency package."""
        return self.spec.name

    def merge(self, other: "Dependency"):
        """Merge constraints, deptypes, and patches of other into self."""
        self.spec.constrain(other.spec)
        self.type |= other.type

        # concatenate patch lists, or just copy them in
        for cond, p in other.patches.items():
            if cond in self.patches:
                current_list = self.patches[cond]
                current_list.extend(p for p in other.patches[cond] if p not in current_list)
            else:
                self.patches[cond] = other.patches[cond]

    def __repr__(self) -> str:
        types = deptype_chars(*self.type)
        return f"<Dependency: {self.pkg.name} -> {self.spec} [{types}]>"
