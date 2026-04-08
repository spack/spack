# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Detection of software installed in the system, based on paths inspections
and running executables.
"""
import collections
import concurrent.futures
import os
import pathlib
import re
import sys
import traceback
import warnings
from typing import Dict, Iterable, List, Optional, Set, Tuple, Type

import spack.error
import spack.llnl.util.filesystem
import spack.llnl.util.lang
import spack.llnl.util.tty
import spack.spec
import spack.util.elf as elf_utils
import spack.util.environment
import spack.util.environment as environment
import spack.util.ld_so_conf
import spack.util.parallel

from .common import (
    DetectedDependency,
    WindowsCompilerExternalPaths,
    WindowsKitExternalPaths,
    _convert_to_iterable,
    _normalize_dependency,
    compute_windows_program_path_for_package,
    compute_windows_user_path_for_package,
    determine_external_dependencies,
    executable_prefix,
    find_win32_additional_install_paths,
    library_prefix,
    path_to_dict,
)

#: Timeout used for package detection (seconds)
DETECTION_TIMEOUT = 60
if sys.platform == "win32":
    DETECTION_TIMEOUT = 120


#: Maps a package name to a list of detected specs.
PkgToSpecsDict = Dict[str, List["spack.spec.Spec"]]
#: Maps a detected spec to a list of its dependencies.
SpecToDepsDict = Dict["spack.spec.Spec", List[DetectedDependency]]


def common_windows_package_paths(pkg_cls=None) -> List[str]:
    """Get the paths for common package installation location on Windows
    that are outside the PATH
    Returns [] on unix
    """
    if sys.platform != "win32":
        return []
    paths = WindowsCompilerExternalPaths.find_windows_compiler_bundled_packages()
    paths.extend(find_win32_additional_install_paths())
    paths.extend(WindowsKitExternalPaths.find_windows_kit_bin_paths())
    paths.extend(WindowsKitExternalPaths.find_windows_kit_reg_installed_roots_paths())
    paths.extend(WindowsKitExternalPaths.find_windows_kit_reg_sdk_paths())
    if pkg_cls:
        paths.extend(compute_windows_user_path_for_package(pkg_cls))
        paths.extend(compute_windows_program_path_for_package(pkg_cls))
    return paths


def file_identifier(path):
    s = os.stat(path)
    return s.st_dev, s.st_ino


def dedupe_paths(paths: List[str]) -> List[str]:
    """Deduplicate paths based on inode and device number. In case the list contains first a
    symlink and then the directory it points to, the symlink is replaced with the directory path.
    This ensures that we pick for example ``/usr/bin`` over ``/bin`` if the latter is a symlink to
    the former."""
    seen: Dict[Tuple[int, int], str] = {}

    linked_parent_check = lambda x: any(
        [spack.llnl.util.filesystem.islink(str(y)) for y in pathlib.Path(x).parents]
    )

    for path in paths:
        identifier = file_identifier(path)
        if identifier not in seen:
            seen[identifier] = path
        # we also want to deprioritize paths if they contain a symlink in any parent
        # (not just the basedir): e.g. oneapi has "latest/bin",
        # where "latest" is a symlink to 2025.0"
        elif not (spack.llnl.util.filesystem.islink(path) or linked_parent_check(path)):
            seen[identifier] = path
    return list(seen.values())


def executables_in_path(path_hints: List[str]) -> Dict[str, str]:
    """Get the paths of all executables available from the current PATH.

    For convenience, this is constructed as a dictionary where the keys are
    the executable paths and the values are the names of the executables
    (i.e. the basename of the executable path).

    There may be multiple paths with the same basename. In this case it is
    assumed there are two different instances of the executable.

    Args:
        path_hints: list of paths to be searched. If None the list will be
            constructed based on the PATH environment variable.
    """
    search_paths = spack.llnl.util.filesystem.search_paths_for_executables(*path_hints)
    # Make use we don't doubly list /usr/lib and /lib etc
    return path_to_dict(dedupe_paths(search_paths))


def accept_elf(path, host_compat):
    """Accept an ELF file if the header matches the given compat triplet. In case it's not an ELF
    (e.g. static library, or some arbitrary file, fall back to is_readable_file)."""
    # Fast path: assume libraries at least have .so in their basename.
    # Note: don't replace with splitext, because of libsmth.so.1.2.3 file names.
    if ".so" not in os.path.basename(path):
        return spack.llnl.util.filesystem.is_readable_file(path)
    try:
        return host_compat == elf_utils.get_elf_compat(path)
    except (OSError, elf_utils.ElfParsingError):
        return spack.llnl.util.filesystem.is_readable_file(path)


def libraries_in_ld_and_system_library_path(
    path_hints: Optional[List[str]] = None,
) -> Dict[str, str]:
    """Get the paths of all libraries available from ``path_hints`` or the
    following defaults:

    - Environment variables (Linux: ``LD_LIBRARY_PATH``, Darwin: ``DYLD_LIBRARY_PATH``,
      and ``DYLD_FALLBACK_LIBRARY_PATH``)
    - Dynamic linker default paths (glibc: ld.so.conf, musl: ld-musl-<arch>.path)
    - Default system library paths.

    For convenience, this is constructed as a dictionary where the keys are
    the library paths and the values are the names of the libraries
    (i.e. the basename of the library path).

    There may be multiple paths with the same basename. In this case it is
    assumed there are two different instances of the library.

    Args:
        path_hints: list of paths to be searched. If None the list will be
            constructed based on the set of LD_LIBRARY_PATH, LIBRARY_PATH,
            DYLD_LIBRARY_PATH, and DYLD_FALLBACK_LIBRARY_PATH environment
            variables as well as the standard system library paths.
        path_hints (list): list of paths to be searched. If ``None``, the default
            system paths are used.
    """
    if path_hints:
        search_paths = spack.llnl.util.filesystem.search_paths_for_libraries(*path_hints)
    else:
        search_paths = []

        # Environment variables
        if sys.platform == "darwin":
            search_paths.extend(environment.get_path("DYLD_LIBRARY_PATH"))
            search_paths.extend(environment.get_path("DYLD_FALLBACK_LIBRARY_PATH"))
        elif sys.platform.startswith("linux"):
            search_paths.extend(environment.get_path("LD_LIBRARY_PATH"))

        # Dynamic linker paths
        search_paths.extend(spack.util.ld_so_conf.host_dynamic_linker_search_paths())

        # Drop redundant paths
        search_paths = list(filter(os.path.isdir, search_paths))

    # Make use we don't doubly list /usr/lib and /lib etc
    search_paths = dedupe_paths(search_paths)

    try:
        host_compat = elf_utils.get_elf_compat(sys.executable)
        accept = lambda path: accept_elf(path, host_compat)
    except (OSError, elf_utils.ElfParsingError):
        accept = spack.llnl.util.filesystem.is_readable_file

    path_to_lib = {}
    # Reverse order of search directories so that a lib in the first
    # search path entry overrides later entries
    for search_path in reversed(search_paths):
        for lib in os.listdir(search_path):
            lib_path = os.path.join(search_path, lib)
            if accept(lib_path):
                path_to_lib[lib_path] = lib
    return path_to_lib


def libraries_in_windows_paths(path_hints: Optional[List[str]] = None) -> Dict[str, str]:
    """Get the paths of all libraries available from the system PATH paths.

    For more details, see ``libraries_in_ld_and_system_library_path`` regarding
    return type and contents.

    Args:
        path_hints: list of paths to be searched. If None the list will be
            constructed based on the set of PATH environment
            variables as well as the standard system library paths.
    """
    search_hints = (
        path_hints if path_hints is not None else spack.util.environment.get_path("PATH")
    )
    search_paths = spack.llnl.util.filesystem.search_paths_for_libraries(*search_hints)
    # on Windows, some libraries (.dlls) are found in the bin directory or sometimes
    # at the search root. Add both of those options to the search scheme
    search_paths.extend(spack.llnl.util.filesystem.search_paths_for_executables(*search_hints))
    if path_hints is None:
        # if no user provided path was given, add defaults to the search
        search_paths.extend(WindowsKitExternalPaths.find_windows_kit_lib_paths())
        # SDK and WGL should be handled by above, however on occasion the WDK is in an atypical
        # location, so we handle that case specifically.
        search_paths.extend(WindowsKitExternalPaths.find_windows_driver_development_kit_paths())
    return path_to_dict(search_paths)


def _group_by_prefix(paths: List[str]) -> Dict[str, Set[str]]:
    groups = collections.defaultdict(set)
    for p in paths:
        groups[os.path.dirname(p)].add(p)
    return groups


class Finder:
    """Inspects the file-system looking for packages. Guesses places where to look using PATH."""

    def default_path_hints(self) -> List[str]:
        return []

    def search_patterns(self, *, pkg: Type["spack.package_base.PackageBase"]) -> List[str]:
        """Returns the list of patterns used to match candidate files.

        Args:
            pkg: package being detected
        """
        raise NotImplementedError("must be implemented by derived classes")

    def candidate_files(self, *, patterns: List[str], paths: List[str]) -> List[str]:
        """Returns a list of candidate files found on the system.

        Args:
            patterns: search patterns to be used for matching files
            paths: paths where to search for files
        """
        raise NotImplementedError("must be implemented by derived classes")

    def prefix_from_path(self, *, path: str) -> str:
        """Given a path where a file was found, returns the corresponding prefix.

        Args:
            path: path of a detected file
        """
        raise NotImplementedError("must be implemented by derived classes")

    def detect_specs(
        self, *, pkg: Type["spack.package_base.PackageBase"], paths: Iterable[str], repo_path
    ) -> List["spack.spec.Spec"]:
        """Given a list of files matching the search patterns, returns a list of detected specs.

        Args:
            pkg: package being detected
            paths: files matching the package search patterns
        """
        if not hasattr(pkg, "determine_spec_details"):
            warnings.warn(
                f"{pkg.name} must define 'determine_spec_details' in order"
                f" for Spack to detect externally-provided instances"
                f" of the package."
            )
            return []

        result = []
        resolved_specs: Dict[spack.spec.Spec, str] = {}  # spec -> prefix of first detection
        for candidate_path, items_in_prefix in _group_by_prefix(
            spack.llnl.util.lang.dedupe(paths)
        ).items():
            # TODO: multiple instances of a package can live in the same
            # prefix, and a package implementation can return multiple specs
            # for one prefix, but without additional details (e.g. about the
            # naming scheme which differentiates them), the spec won't be
            # usable.
            try:
                specs = _convert_to_iterable(
                    pkg.determine_spec_details(candidate_path, items_in_prefix)
                )
            except Exception as e:
                specs = []
                if spack.error.SHOW_BACKTRACE:
                    details = traceback.format_exc()
                else:
                    details = f"[{e.__class__.__name__}: {e}]"
                warnings.warn(
                    f'error detecting "{pkg.name}" from prefix {candidate_path}: {details}'
                )

            if not specs:
                files = ", ".join(_convert_to_iterable(items_in_prefix))
                spack.llnl.util.tty.debug(
                    f"The following files in {candidate_path} were decidedly not "
                    f"part of the package {pkg.name}: {files}"
                )

            for spec in specs:
                prefix = self.prefix_from_path(path=candidate_path)
                if not prefix:
                    continue

                if spec in resolved_specs:
                    prior_prefix = resolved_specs[spec]
                    warnings.warn(
                        f'"{spec}" detected in "{prefix}" was already detected in "{prior_prefix}"'
                    )
                    continue

                resolved_specs[spec] = prefix
                try:
                    # Validate the spec calling a package specific method
                    pkg_cls = repo_path.get_pkg_class(spec.name)
                    validate_fn = getattr(pkg_cls, "validate_detected_spec", lambda x, y: None)
                    validate_fn(spec, spec.extra_attributes)
                except Exception as e:
                    msg = (
                        f'"{spec}" has been detected on the system but will '
                        f"not be added to packages.yaml [reason={str(e)}]"
                    )
                    warnings.warn(msg)
                    continue

                if not spec.external_path:
                    spec.external_path = prefix

                result.append(spec)

        return result

    def find(
        self, *, pkg_name: str, repository, initial_guess: Optional[List[str]] = None
    ) -> List["spack.spec.Spec"]:
        """For a given package, returns a list of detected specs.

        Args:
            pkg_name: package being detected
            repository: repository to retrieve the package
            initial_guess: initial list of paths to search from the caller if None, default paths
                are searched. If this is an empty list, nothing will be searched.
        """
        pkg_cls = repository.get_pkg_class(pkg_name)
        patterns = self.search_patterns(pkg=pkg_cls)
        if not patterns:
            return []
        if initial_guess is None:
            initial_guess = self.default_path_hints()
            initial_guess.extend(common_windows_package_paths(pkg_cls))
        candidates = self.candidate_files(patterns=patterns, paths=initial_guess)
        return self.detect_specs(pkg=pkg_cls, paths=candidates, repo_path=repository)


class ExecutablesFinder(Finder):
    def default_path_hints(self) -> List[str]:
        return spack.util.environment.get_path("PATH")

    def search_patterns(self, *, pkg: Type["spack.package_base.PackageBase"]) -> List[str]:
        result = []
        if hasattr(pkg, "executables") and hasattr(pkg, "platform_executables"):
            result = pkg.platform_executables()
        return result

    def candidate_files(self, *, patterns: List[str], paths: List[str]) -> List[str]:
        executables_by_path = executables_in_path(path_hints=paths)
        joined_pattern = re.compile(r"|".join(patterns))
        result = [path for path, exe in executables_by_path.items() if joined_pattern.search(exe)]
        result.sort()
        return result

    def prefix_from_path(self, *, path: str) -> str:
        result = executable_prefix(path)
        if not result:
            msg = f"no bin/ dir found in {path}. Cannot add it as a Spack package"
            spack.llnl.util.tty.debug(msg)
        return result


class LibrariesFinder(Finder):
    """Finds libraries on the system, searching by LD_LIBRARY_PATH, LIBRARY_PATH,
    DYLD_LIBRARY_PATH, DYLD_FALLBACK_LIBRARY_PATH, and standard system library paths
    """

    def search_patterns(self, *, pkg: Type["spack.package_base.PackageBase"]) -> List[str]:
        result = []
        if hasattr(pkg, "libraries"):
            result = pkg.libraries
        return result

    def candidate_files(self, *, patterns: List[str], paths: List[str]) -> List[str]:
        libraries_by_path = (
            libraries_in_ld_and_system_library_path(path_hints=paths)
            if sys.platform != "win32"
            else libraries_in_windows_paths(path_hints=paths)
        )
        patterns = [re.compile(x) for x in patterns]
        result = []
        for compiled_re in patterns:
            for path, exe in libraries_by_path.items():
                if compiled_re.search(exe):
                    result.append(path)
        return result

    def prefix_from_path(self, *, path: str) -> str:
        result = library_prefix(path)
        if not result:
            msg = f"no lib/ or lib64/ dir found in {path}. Cannot add it as a Spack package"
            spack.llnl.util.tty.debug(msg)
        return result


def packages_to_search_for(
    *, names: Optional[List[str]], tags: List[str], exclude: Optional[List[str]]
) -> List[str]:
    """Return the list of packages to search for, filtered by names, tags, and exclusions.

    Args:
        names: optional list of package names (qualified or unqualified) to restrict the search
        tags: list of tags used to select the candidate packages from the repository
        exclude: optional list of package names to exclude from the result
    """
    # TODO: move to top-level once the circular import with spack.repo is resolved
    import spack.repo

    result = list(
        {pkg for tag in tags for pkg in spack.repo.PATH.packages_with_tags(tag, full=True)}
    )

    if names:
        parts = [rf"(^{x}$|[.]{x}$)" for x in names]
        select_re = re.compile("|".join(parts))
        result = [x for x in result if select_re.search(x)]

    if exclude:
        parts = [rf"(^{x}$|[.]{x}$)" for x in exclude]
        select_re = re.compile("|".join(parts))
        result = [x for x in result if not select_re.search(x)]

    return result


def by_path(
    packages_to_search: Iterable[str],
    *,
    path_hints: Optional[List[str]] = None,
    max_workers: Optional[int] = None,
) -> Dict[str, List["spack.spec.Spec"]]:
    """Return the list of packages that have been detected on the system, keyed by
    unqualified package name.

    Args:
        packages_to_search: list of packages to be detected. Each package can be either unqualified
            of fully qualified
        path_hints: initial list of paths to be searched
        max_workers: maximum number of workers to search for packages in parallel
    """
    # TODO: move to top-level once the circular import with spack.repo is resolved
    from spack.repo import PATH, partition_package_name

    # TODO: Packages should be able to define both .libraries and .executables in the future
    # TODO: determine_spec_details should get all relevant libraries and executables in one call
    executables_finder, libraries_finder = ExecutablesFinder(), LibrariesFinder()
    detected_specs_by_package: Dict[str, Tuple[concurrent.futures.Future, ...]] = {}

    result = collections.defaultdict(list)
    repository = PATH.ensure_unwrapped()

    executor: concurrent.futures.Executor
    if max_workers == 1:
        executor = spack.util.parallel.SequentialExecutor()
    else:
        executor = spack.util.parallel.make_concurrent_executor(max_workers, require_fork=False)
    with executor:
        for pkg in packages_to_search:
            executable_future = executor.submit(
                executables_finder.find,
                pkg_name=pkg,
                initial_guess=path_hints,
                repository=repository,
            )
            library_future = executor.submit(
                libraries_finder.find,
                pkg_name=pkg,
                initial_guess=path_hints,
                repository=repository,
            )
            detected_specs_by_package[pkg] = executable_future, library_future

        for pkg_name, futures in detected_specs_by_package.items():
            for future in futures:
                try:
                    detected = future.result(timeout=DETECTION_TIMEOUT)
                    if detected:
                        _, unqualified_name = partition_package_name(pkg_name)
                        result[unqualified_name].extend(detected)
                except concurrent.futures.TimeoutError:
                    spack.llnl.util.tty.debug(
                        f"[EXTERNAL DETECTION] Skipping {pkg_name}: timeout reached"
                    )
                except Exception:
                    spack.llnl.util.tty.debug(
                        f"[EXTERNAL DETECTION] Skipping {pkg_name}: {traceback.format_exc()}"
                    )

    return result


def _prefix_hints_from_unresolved_deps(
    detected_dependencies: "SpecToDepsDict",
    detected_packages: "PkgToSpecsDict",
    known_packages: List["spack.spec.Spec"],
) -> List[str]:
    """Return prefix hints from unresolved dependency specs that carry ``external_path``.

    When a package author declares a dependency via the dict form with a ``prefix`` key,
    ``_normalize_dependency`` stores that path as ``dep.spec.external_path``.  This helper
    collects those paths for deps that are not yet resolvable so the caller can pass them
    as additional ``path_hints`` to the next ``by_path`` round.

    Args:
        detected_dependencies: raw dependencies as returned by ``collect_dependencies``
        detected_packages: all currently detected packages
        known_packages: specs already present in ``packages.yaml``
    """
    all_available = [s for specs in detected_packages.values() for s in specs]
    all_available.extend(known_packages)

    hints = set()
    for dep_list in detected_dependencies.values():
        for dep in dep_list:
            if any(s.satisfies(dep.spec) for s in all_available):
                continue  # already resolvable, no need to hint
            if dep.spec.external_path:
                hints.add(dep.spec.external_path)
    return sorted(hints)


def by_path_with_dependencies(
    packages_to_search: Iterable[str],
    *,
    path_hints: Optional[List[str]] = None,
    max_workers: Optional[int] = None,
    known_packages: Optional[List["spack.spec.Spec"]] = None,
    exclude: Optional[List[str]] = None,
) -> Tuple[PkgToSpecsDict, SpecToDepsDict]:
    """Detect packages by path, then iteratively detect any missing dependencies.

    Starts with an initial round of ``by_path`` detection on ``packages_to_search``, then
    repeats detection for dependency packages that were declared by already-detected specs
    but could not yet be resolved. Iteration stops when no new packages are found or all
    declared dependencies are accounted for.

    Args:
        packages_to_search: initial list of packages to detect (qualified or unqualified names)
        path_hints: additional paths to search; falls back to PATH when ``None``
        max_workers: maximum number of parallel detection workers
        known_packages: specs already present in ``packages.yaml``. Used to skip deps that are
            already known without re-detecting them
        exclude: package names to exclude from every detection round

    Returns:
        A tuple ``(detected_packages, detected_dependencies)`` accumulated across all rounds.
    """
    detected_packages = by_path(packages_to_search, path_hints=path_hints, max_workers=max_workers)
    detected_dependencies = collect_dependencies(detected_packages)

    already_searched = set(detected_packages)
    known_packages = known_packages or []

    extra_prefix_hints = _prefix_hints_from_unresolved_deps(
        detected_dependencies, detected_packages, known_packages
    )

    to_detect = (
        missing_dependency_package_names(
            detected_packages=detected_packages,
            detected_dependencies=detected_dependencies,
            known_packages=known_packages,
        )
        - already_searched
    )

    while to_detect:
        extra_pkgs = packages_to_search_for(
            names=list(to_detect), tags=["detectable"], exclude=exclude
        )
        already_searched.update(to_detect)

        if not extra_pkgs:
            break

        combined_hints = (list(path_hints or []) + extra_prefix_hints) or None
        extra_detected = by_path(extra_pkgs, path_hints=combined_hints, max_workers=max_workers)

        if not extra_detected:
            break

        for name, specs in extra_detected.items():
            detected_packages.setdefault(name, []).extend(specs)

        extra_dependencies = collect_dependencies(extra_detected)
        detected_dependencies.update(extra_dependencies)

        extra_prefix_hints = _prefix_hints_from_unresolved_deps(
            extra_dependencies, detected_packages, known_packages
        )

        to_detect = (
            missing_dependency_package_names(
                detected_packages=detected_packages,
                detected_dependencies=extra_dependencies,
                known_packages=known_packages,
            )
            - already_searched
        )

    resolved_dependencies = determine_external_dependencies(
        detected_packages=detected_packages,
        detected_dependencies=detected_dependencies,
        known_packages=known_packages,
    )

    return detected_packages, resolved_dependencies


def collect_dependencies(detected_packages: PkgToSpecsDict) -> SpecToDepsDict:
    """Call ``determine_dependencies`` once per detected spec and returns a mapping from each
    detected spec to its list of unresolved dependencies.

    Args:
        detected_packages: mapping of package name to detected specs.
    """
    # TODO: move to top-level once the circular import with spack.repo is resolved
    import spack.repo

    result = {}
    for pkg_name, specs in detected_packages.items():
        try:
            pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        except Exception as e:
            spack.llnl.util.tty.debug(
                f"[{__name__}] cannot load package class for '{pkg_name}': {e}"
            )
            continue

        if not hasattr(pkg_cls, "determine_dependencies"):
            continue

        for spec in specs:
            try:
                detected_deps = _convert_to_iterable(pkg_cls.determine_dependencies(spec))
                normalized = [_normalize_dependency(dep) for dep in detected_deps]
            except Exception as e:
                warnings.warn(f'error calling determine_dependencies for "{spec}": {e}')
                continue

            if not normalized:
                continue

            result[spec] = normalized

    return result


def missing_dependency_package_names(
    *,
    detected_packages: Optional[Dict[str, List["spack.spec.Spec"]]] = None,
    detected_dependencies: Dict["spack.spec.Spec", List[DetectedDependency]],
    known_packages: Optional[List["spack.spec.Spec"]] = None,
) -> Set[str]:
    """Returns the package names declared as dependencies that cannot be resolved.

    Args:
        detected_packages: all currently detected packages
        detected_dependencies: pre-collected output of ``collect_dependencies`` for the packages
        known_packages: specs already present in ``packages.yaml``. Dependency candidates that
            match entries here are considered resolved and are not included in the returned set.
    """
    all_available = []
    if detected_packages is not None:
        all_available = [s for specs in detected_packages.values() for s in specs]
    all_available.extend(known_packages or [])

    missing = set()
    for dep_list in detected_dependencies.values():
        for dep in dep_list:
            if not any(s.satisfies(dep.spec) for s in all_available):
                missing.add(dep.spec.name)
    return missing
