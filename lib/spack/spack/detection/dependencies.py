# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Detect the dependencies between externals from the libraries their files load."""

import collections
import os
import re
import warnings
from typing import Dict, Iterable, List, NamedTuple, Tuple

import spack.deptypes as dt
import spack.externals
import spack.repo
import spack.spec

from .common import library_prefix
from .elf_closure import DynamicLoader, LoadedObject
from .ownership import LibraryOwner, OwnershipIndex
from .path import DetectedExternal

#: Libraries of libc and of compiler runtimes. The solver models these without edges between
#: externals, so they neither produce an edge nor are searched for other libraries.
SYSTEM_LIBRARIES = re.compile(
    r"^(ld-linux.*|ld64\.so|ld-musl-.*|libc\.musl-.*"
    r"|lib(c|m|mvec|pthread|dl|rt|util|resolv|anl|nsl|BrokenLocale|thread_db)\.so"
    r"|lib(gcc_s|stdc\+\+|gfortran|quadmath|gomp|atomic|itm|ssp|c\+\+|c\+\+abi)\.so)"
)


class ExternalEdge(NamedTuple):
    """A dependency of a detected external on another external."""

    parent: spack.spec.Spec
    child: spack.spec.Spec
    depflag: dt.DepFlag
    virtuals: Tuple[str, ...]
    #: real path of the library of the child that a file of the parent loads
    library: str


class MissingExternal(NamedTuple):
    """A library that a detected external loads, owned by packages with no matching external."""

    parent: spack.spec.Spec
    #: real path of the library
    library: str
    #: packages whose patterns match the library
    owners: List[str]


class DetectedDependencies(NamedTuple):
    edges: List[ExternalEdge]
    missing: List[MissingExternal]


def _libraries_of_other_packages(
    loaded: Dict[str, LoadedObject], root: str, name: str, index: OwnershipIndex
) -> Dict[str, List[LibraryOwner]]:
    """Returns the libraries loaded for ``root`` that are owned by packages other than ``name``,
    mapped to their owners.

    The search passes through libraries owned by ``name`` or by no package, and stops at system
    libraries and at libraries of other packages.
    """
    result: Dict[str, List[LibraryOwner]] = {}
    root_key = os.path.realpath(root)
    if root_key not in loaded:
        return result

    visited = {root_key}
    queue = collections.deque([root_key])
    while queue:
        for key in loaded[queue.popleft()].needed:
            if key in visited:
                continue
            visited.add(key)
            if SYSTEM_LIBRARIES.match(os.path.basename(loaded[key].path)):
                continue
            owners = index.confirmed_library_owners(loaded[key].path, key)
            if owners and all(x.name != name for x in owners):
                result[key] = owners
                continue
            queue.append(key)
    return result


def _is_in_prefix(library: LoadedObject, key: str, spec: spack.spec.Spec) -> bool:
    """Returns whether a library is under the prefix of an external, before or after resolving
    symlinks in the path the library was found at.
    """
    if not spec.external_path:
        return False
    prefixes = {
        os.path.realpath(library_prefix(os.path.dirname(library.path))),
        library_prefix(os.path.dirname(key)),
    }
    return os.path.realpath(spec.external_path) in prefixes


def detect_dependencies(
    detected: Iterable[DetectedExternal],
    *,
    externals: Iterable[spack.spec.Spec],
    index: OwnershipIndex,
    loader: DynamicLoader,
    repo: spack.repo.RepoPath,
) -> DetectedDependencies:
    """Returns the link dependencies of detected externals on other externals.

    A library loaded by the files of a detected external is attributed to the externals of its
    owners, among ``externals``, whose prefix contains it and whose version matches the one the
    owner detects for it, if any. An edge is recorded when exactly one such external exists, and
    the recipe of the parent has a link dependency on it that applies to the parent. Libraries
    whose owners have no such external are returned as missing.

    Arguments:
        detected: detected externals, with the files they were detected from
        externals: candidate dependencies, from this detection and from configuration
        index: owners of libraries
        loader: resolves the libraries that a file loads
        repo: repository of the recipes
    """
    externals_by_name: Dict[str, List[spack.spec.Spec]] = collections.defaultdict(list)
    for spec in externals:
        externals_by_name[spec.name].append(spec)

    edges: List[ExternalEdge] = []
    missing: List[MissingExternal] = []
    for parent, files in detected:
        libraries: Dict[str, List[LibraryOwner]] = {}
        loaded: Dict[str, LoadedObject] = {}
        for root in files:
            loaded_by_root = loader.load(root)
            for key, owners in _libraries_of_other_packages(
                loaded_by_root, root, parent.name, index
            ).items():
                libraries.setdefault(key, owners)
                loaded.setdefault(key, loaded_by_root[key])

        # The parser completes an external read from configuration in the same way
        completed = parent.copy()
        spack.externals.complete_variants_and_architecture(completed, repo)
        types_by_name = spack.externals.dependency_types(completed, repo)

        children: List[spack.spec.Spec] = []
        for key, owners in libraries.items():
            candidates = [
                spec
                for owner in owners
                for spec in externals_by_name.get(owner.name, [])
                if _is_in_prefix(loaded[key], key, spec)
                and (owner.version is None or spec.intersects(f"@={owner.version}"))
            ]
            if not candidates:
                owner_names = [x.name for x in owners]
                missing.append(MissingExternal(parent=parent, library=key, owners=owner_names))
                continue

            if len(candidates) > 1:
                candidates_str = ", ".join(str(x) for x in candidates)
                warnings.warn(
                    f"{parent} loads {key}, which may belong to any of {candidates_str}. "
                    f"No dependency is recorded for it."
                )
                continue

            child = candidates[0]
            if any(child is x for x in children):
                continue

            depflag, virtuals = spack.externals.infer_dependency(child, types_by_name, repo)
            depflag &= dt.LINK
            if not depflag:
                warnings.warn(
                    f"{parent} loads {key} from {child}, but the recipe of {parent.name} has no "
                    f"link dependency on {child.name} that applies to it. No dependency is "
                    f"recorded for it."
                )
                continue

            children.append(child)
            edges.append(
                ExternalEdge(
                    parent=parent, child=child, depflag=depflag, virtuals=virtuals, library=key
                )
            )

    return DetectedDependencies(edges=edges, missing=missing)
