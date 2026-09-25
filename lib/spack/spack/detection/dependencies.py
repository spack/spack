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

from .common import executable_prefix, library_prefix
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
    #: real path of a library of the child that the parent loads, or of an executable of the
    #: child that the parent runs
    library: str


class MissingExternal(NamedTuple):
    """A file that a detected external uses, owned by packages with no matching external."""

    parent: spack.spec.Spec
    #: real path of the file
    library: str
    #: packages that own the file
    owners: List[str]
    #: prefix of the installation the file belongs to, guessed from its directory
    prefix: str


class _Evidence(NamedTuple):
    """A file of another package that a detected external uses."""

    #: real path of the file
    key: str
    #: path the file was found at
    path: str
    owners: List[LibraryOwner]
    #: ``LINK`` for a library the external loads, ``RUN`` for an executable it runs
    depflag: dt.DepFlag

    def prefix_of(self, directory: str) -> str:
        if self.depflag == dt.LINK:
            return library_prefix(directory)
        return executable_prefix(directory)


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


def _is_in_prefix(evidence: _Evidence, spec: spack.spec.Spec) -> bool:
    """Returns whether a file is under the prefix of an external, before or after resolving
    symlinks in the path the file was found at.
    """
    if not spec.external_path:
        return False
    prefixes = {
        os.path.realpath(evidence.prefix_of(os.path.dirname(evidence.path))),
        evidence.prefix_of(os.path.dirname(evidence.key)),
    }
    return os.path.realpath(spec.external_path) in prefixes


def _files_of_other_packages(
    dependency_files: List[str], name: str, index: OwnershipIndex
) -> List[_Evidence]:
    """Returns the files among ``dependency_files`` that are owned by packages other than
    ``name``, as libraries or as executables.
    """
    result = []
    for path in dependency_files:
        key = os.path.realpath(path)
        for owners, depflag in (
            (index.confirmed_library_owners(path, key), dt.LINK),
            (index.confirmed_executable_owners(path), dt.RUN),
        ):
            if owners and all(x.name != name for x in owners):
                result.append(_Evidence(key=key, path=path, owners=owners, depflag=depflag))
    return result


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
    """Returns the link and run dependencies of detected externals on other externals.

    The evidence of a dependency is a library loaded by the files of a detected external, or by
    its dependency files, and a dependency file itself when another package owns it as a library
    (link) or as an executable (run). Each file is attributed to the externals of its owners,
    among ``externals``, whose prefix contains it and whose version matches the one the owner
    detects for it, if any. An edge is recorded when exactly one such external exists, with the
    types of the recipe's dependency on it that are shown by the evidence. Files whose owners have
    no such external are returned as missing.

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
    for parent, files, dependency_files in detected:
        libraries: Dict[str, List[LibraryOwner]] = {}
        default_libraries: Dict[str, List[LibraryOwner]] = {}
        loaded: Dict[str, LoadedObject] = {}
        for root in [*files, *dependency_files]:
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

        evidence = [
            _Evidence(key=key, path=loaded[key].path, owners=owners, depflag=dt.LINK)
            for key, owners in libraries.items()
        ]
        evidence.extend(_files_of_other_packages(dependency_files, parent.name, index))

        # Children, with the types of evidence found for them and the first file found
        children: List[Tuple[spack.spec.Spec, dt.DepFlag, str]] = []
        for item in evidence:
            candidates = [
                spec
                for owner in item.owners
                for spec in externals_by_name.get(owner.name, [])
                if _is_in_prefix(item, spec)
                and (owner.version is None or spec.intersects(f"@={owner.version}"))
            ]
            if not candidates:
                missing.append(
                    MissingExternal(
                        parent=parent,
                        library=item.key,
                        owners=[x.name for x in item.owners],
                        prefix=item.prefix_of(os.path.dirname(item.key)),
                    )
                )
                continue

            if len(candidates) > 1:
                candidates_str = ", ".join(str(x) for x in candidates)
                warnings.warn(
                    f"{parent} uses {item.key}, which may belong to any of {candidates_str}. "
                    f"No dependency is recorded for it."
                )
                continue

            child = candidates[0]
            for i, (other, flag, key) in enumerate(children):
                if other is child:
                    children[i] = (other, flag | item.depflag, key)
                    break
            else:
                children.append((child, item.depflag, item.key))

        for child, evidence_flag, key in children:
            depflag, virtuals = spack.externals.infer_dependency(child, types_by_name, repo)
            depflag &= evidence_flag
            if not depflag:
                types_str = " or ".join(dt.flag_to_tuple(evidence_flag))
                warnings.warn(
                    f"{parent} uses {key} from {child}, but the recipe of {parent.name} has no "
                    f"{types_str} dependency on {child.name} that applies to it. No dependency "
                    f"is recorded for it."
                )
                continue

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
    files they use when those have no external.

    The ``determine_dependency_files`` method of the recipe of each external, if defined, is
    called once with its spec, and the files it returns are used as evidence of dependencies.
    An owner is searched for in the prefix of the file and in its directory, once per prefix.
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
            entry = entry._replace(dependency_files=_dependency_files(entry.spec, repo))
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
            prefix = item.prefix
            for owner in item.owners:
                if owner in excluded or (owner, prefix) in searched:
                    continue
                searched.add((owner, prefix))
                owners_by_prefix[prefix].add(owner)
                hints_by_prefix[prefix].add(os.path.dirname(item.library))

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


def _dependency_files(spec: spack.spec.Spec, repo: spack.repo.RepoPath) -> List[str]:
    """Returns the absolute paths that ``determine_dependency_files`` returns for a spec, or an
    empty list if the recipe does not define it. Errors in the method are turned into warnings.
    """
    method = getattr(repo.get_pkg_class(spec.name), "determine_dependency_files", None)
    if method is None:
        return []

    try:
        paths = list(method(spec) or [])
    except Exception as e:
        warnings.warn(f"Cannot get the dependency files of {spec} [{type(e).__name__}: {e}]")
        return []

    result = [x for x in paths if isinstance(x, str) and os.path.isabs(x)]
    if len(result) != len(paths):
        warnings.warn(
            f"The dependency files of {spec} must be absolute paths, the other values are "
            f"ignored [{', '.join(repr(x) for x in paths if x not in result)}]"
        )
    return result
