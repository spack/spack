# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Detect the dependencies between externals from the libraries their files load."""

import collections
import os
import re
import warnings
from typing import Callable, Dict, Iterable, List, NamedTuple, Optional, Set, Tuple

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


def _libraries_by_owners(
    libraries: Dict[str, List[LibraryOwner]],
) -> Dict[Tuple[str, ...], Set[str]]:
    result: Dict[Tuple[str, ...], Set[str]] = collections.defaultdict(set)
    for key, owners in libraries.items():
        result[tuple(x.name for x in owners)].add(key)
    return result


def _warn_on_environment_differences(
    parent: spack.spec.Spec,
    with_environment: Dict[str, List[LibraryOwner]],
    without_environment: Dict[str, List[LibraryOwner]],
) -> None:
    """Warns when libraries of the same owners are found at other paths without
    ``LD_LIBRARY_PATH``.
    """
    default = _libraries_by_owners(without_environment)
    for owners, keys in _libraries_by_owners(with_environment).items():
        other = default.get(owners)
        if other and other != keys:
            warnings.warn(
                f"{parent} loads {', '.join(sorted(keys))} through LD_LIBRARY_PATH, and "
                f"{', '.join(sorted(other))} without it. Dependencies are detected from the "
                f"libraries found through LD_LIBRARY_PATH."
            )


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

    When ``loader`` searches ``LD_LIBRARY_PATH``, libraries are also resolved without it, and a
    warning is emitted if that finds libraries of the same owners at other paths.

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

    without_environment = None
    if loader.ld_library_path:
        without_environment = DynamicLoader(ld_library_path=[], default_dirs=loader.default_dirs)

    edges: List[ExternalEdge] = []
    missing: List[MissingExternal] = []
    for parent, files in detected:
        libraries: Dict[str, List[LibraryOwner]] = {}
        default_libraries: Dict[str, List[LibraryOwner]] = {}
        loaded: Dict[str, LoadedObject] = {}
        for root in files:
            loaded_by_root = loader.load(root)
            for key, owners in _libraries_of_other_packages(
                loaded_by_root, root, parent.name, index
            ).items():
                libraries.setdefault(key, owners)
                loaded.setdefault(key, loaded_by_root[key])
            if without_environment is not None:
                default_libraries.update(
                    _libraries_of_other_packages(
                        without_environment.load(root), root, parent.name, index
                    )
                )

        if without_environment is not None:
            _warn_on_environment_differences(parent, libraries, default_libraries)

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


#: Detects externals of the packages in the first argument, searching the ``path_hints`` keyword
#: argument, as ``spack.detection.path.by_path_detailed`` does
DetectFn = Callable[..., Dict[str, List[DetectedExternal]]]


class DetectedWithDependencies(NamedTuple):
    #: detected externals by package name, including the packages detected as dependencies
    detected: Dict[str, List[DetectedExternal]]
    edges: List[ExternalEdge]
    missing: List[MissingExternal]


def detect_with_dependencies(
    detected: Dict[str, List[DetectedExternal]],
    *,
    detect: DetectFn,
    configured: Iterable[spack.spec.Spec],
    index: OwnershipIndex,
    loader: DynamicLoader,
    repo: spack.repo.RepoPath,
    exclude: Iterable[str] = (),
) -> DetectedWithDependencies:
    """Detects the dependencies of detected externals, detecting the packages that own the
    libraries they load when those have no external.

    An owner is searched for in the prefix of the library and in its directory, once per prefix.
    Externals detected this way are searched for dependencies in turn, until no new external is
    found. Packages in ``exclude`` are never searched for.

    Arguments:
        detected: detected externals by package name
        detect: function detecting the externals of a list of packages
        configured: externals in configuration, which are candidate dependencies
        index: owners of libraries
        loader: resolves the libraries that a file loads
        repo: repository of the recipes
        exclude: names of packages that are not searched for
    """
    excluded = set(exclude)
    configured = list(configured)
    result: Dict[str, List[DetectedExternal]] = collections.defaultdict(list)
    all_detected: List[DetectedExternal] = []
    known: Set[Tuple[str, Optional[str]]] = set()

    def add(name: str, entries: List[DetectedExternal]) -> List[DetectedExternal]:
        added = []
        for entry in entries:
            key = (str(entry.spec), entry.spec.external_path)
            if key in known:
                continue
            known.add(key)
            result[name].append(entry)
            all_detected.append(entry)
            added.append(entry)
        return added

    pending: List[DetectedExternal] = []
    for name, entries in detected.items():
        pending.extend(add(name, entries))

    searched: Set[Tuple[str, str]] = set()
    while pending:
        # Warnings are emitted once, by the final pass below
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            partial = detect_dependencies(
                pending,
                externals=[x.spec for x in all_detected] + configured,
                index=index,
                loader=loader,
                repo=repo,
            )

        owners_by_prefix: Dict[str, Set[str]] = collections.defaultdict(set)
        hints_by_prefix: Dict[str, Set[str]] = collections.defaultdict(set)
        for item in partial.missing:
            library_dir = os.path.dirname(item.library)
            prefix = library_prefix(library_dir)
            for owner in item.owners:
                if owner in excluded or (owner, prefix) in searched:
                    continue
                searched.add((owner, prefix))
                owners_by_prefix[prefix].add(owner)
                hints_by_prefix[prefix].add(library_dir)

        pending = []
        for prefix in sorted(owners_by_prefix):
            hints = [prefix, *sorted(hints_by_prefix[prefix])]
            found = detect(sorted(owners_by_prefix[prefix]), path_hints=hints)
            for name, entries in found.items():
                pending.extend(add(name, entries))

    final = detect_dependencies(
        all_detected,
        externals=[x.spec for x in all_detected] + configured,
        index=index,
        loader=loader,
        repo=repo,
    )
    return DetectedWithDependencies(detected=result, edges=final.edges, missing=final.missing)
