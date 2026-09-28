# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Build subprocess (child) side of the new installer.

This module holds everything that runs in (or directly manages) a single build's child process:
the :func:`worker_function` entry point, the install steps it drives, and the loop-side
:class:`ChildInfo` handle the parent uses to talk to the child. See :mod:`spack.installer`
for the overall design."""

import errno
import glob
import io
import json
import os
import selectors
import shlex
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import traceback
from gzip import GzipFile
from multiprocessing import Process
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Iterable, List, NamedTuple, Optional, Tuple

from spack.vendor.typing_extensions import Protocol

import spack.binary_distribution
import spack.build_environment
import spack.builder
import spack.caches
import spack.compilers.config
import spack.config
import spack.error
import spack.hooks
import spack.mirrors.mirror
import spack.paths
import spack.repo
import spack.sandbox
import spack.sandbox_namespaces
import spack.spec
import spack.store
import spack.url_buildcache
import spack.util.environment
import spack.util.filesystem as fs
import spack.util.ld_so_conf
import spack.util.lock
import spack.util.spack_yaml as syaml
import spack.util.timer
import spack.util.tty
from spack.installer.base import (
    ExitCode,
    FdInfo,
    InstallPolicy,
    IpcChannel,
    JobServerBase,
    Makeflags,
    ProcessExitNotifier,
)
from spack.subprocess_context import GlobalStateMarshaler
from spack.util.executable import ProcessError, which_string

if sys.platform == "win32":
    from spack.installer.windows import WindowsSentinelBridge as ExitNotifier
    from spack.installer.windows import WindowsTee as Tee
    from spack.installer.windows import create_build_channels, make_state_stream
else:
    from spack.installer.posix import PosixExitNotifier as ExitNotifier
    from spack.installer.posix import PosixTee as Tee
    from spack.installer.posix import create_build_channels, make_state_stream

if TYPE_CHECKING:
    import spack.package_base

#: Suffix for temporary backup during overwrite install
OVERWRITE_BACKUP_SUFFIX = ".old"

#: Suffix for temporary cleanup during failed install
OVERWRITE_GARBAGE_SUFFIX = ".garbage"


class ProcessLike(Protocol):
    """The part of the ``multiprocessing.Process`` interface the event loop relies on. Tests
    provide synthetic implementations to exercise the loop without forking."""

    @property
    def pid(self) -> Optional[int]: ...

    @property
    def exitcode(self) -> Optional[int]: ...

    def terminate(self) -> None: ...

    def kill(self) -> None: ...

    def is_alive(self) -> bool: ...

    def join(self, timeout: Optional[float] = None) -> None: ...


class NamespacePolicyInputPaths(NamedTuple):
    """Trusted host paths selected before namespace policy compilation."""

    hidden_roots: Tuple[str, ...]
    compiler_paths: Tuple[str, ...]
    tool_paths: Tuple[str, ...]
    header_paths: Tuple[str, ...]
    runtime_paths: Tuple[str, ...]
    temporary_paths: Tuple[str, ...]


class NamespaceActivation(NamedTuple):
    """Immutable namespace policy data prepared by trusted installer setup."""

    policy: spack.sandbox_namespaces.NamespaceFilesystemPolicy
    mount_plan_stage: str
    worker_root: str


class NamespaceHostDeviceWorkerPaths(NamedTuple):
    """Trusted host, device, and worker-state paths selected before policy compilation."""

    hidden_roots: Tuple[str, ...]
    replacement_roots: Tuple[str, ...]
    host_runtime_paths: Tuple[str, ...]
    device_paths: Tuple[str, ...]
    read_only_paths: Tuple[str, ...]
    writable_paths: Tuple[str, ...]


class ResolvedSandboxPath(NamedTuple):
    """Preserve the requested spelling separately from its canonical source path."""

    spelling: str
    source: str


SANDBOX_POLICY_PATH = os.path.join(spack.paths.share_path, "sandbox", "sandbox.yaml")
LINUX_HEADER_POLICY_PATH = os.path.join(
    spack.paths.share_path, "sandbox", "linux-header-policy.yaml"
)


def _policy_error(policy_name: str, path: str, key: str, detail: str) -> spack.error.InstallError:
    return spack.error.InstallError(f"Invalid {policy_name} key {key!r} in {path}: {detail}")


def _load_policy_document(policy_name: str, path: str):
    try:
        with open(path, encoding="utf-8") as stream:
            policy = syaml.load(stream)
    except (OSError, syaml.SpackYAMLError) as error:
        raise spack.error.InstallError(f"Cannot load {policy_name} {path}: {error}") from error

    if not isinstance(policy, dict):
        raise _policy_error(policy_name, path, "<document>", "expected a mapping")
    if type(policy.get("version")) is not int or policy["version"] != 1:
        raise _policy_error(policy_name, path, "version", "expected integer 1")
    return policy


def _validate_string_list(policy_name: str, path: str, policy: dict, key: str) -> None:
    value = policy.get(key)
    if not isinstance(value, list) or not all(isinstance(entry, str) for entry in value):
        raise _policy_error(policy_name, path, key, "expected a list of strings")


def _validate_absolute_path_list(policy_name: str, path: str, policy: dict, key: str) -> None:
    _validate_string_list(policy_name, path, policy, key)
    if any(not os.path.isabs(entry) for entry in policy[key]):
        raise _policy_error(policy_name, path, key, "expected absolute paths")


def _validate_empty_directory_paths(policy_name: str, path: str, policy: dict) -> None:
    value = policy.get("empty_directory_paths")
    if not isinstance(value, list):
        raise _policy_error(policy_name, path, "empty_directory_paths", "expected a list")
    for index, entry in enumerate(value):
        if not isinstance(entry, dict):
            raise _policy_error(
                policy_name, path, f"empty_directory_paths[{index}]", "expected a mapping"
            )
        directory = entry.get("path")
        if not isinstance(directory, str) or not os.path.isabs(directory):
            raise _policy_error(
                policy_name,
                path,
                f"empty_directory_paths[{index}].path",
                "expected an absolute path",
            )
        constraints = entry.get("unless_external_specs", [])
        if not isinstance(constraints, list) or not all(
            isinstance(constraint, str) for constraint in constraints
        ):
            raise _policy_error(
                policy_name,
                path,
                f"empty_directory_paths[{index}].unless_external_specs",
                "expected a list of strings",
            )
        for constraint in constraints:
            try:
                spack.spec.Spec(constraint)
            except (spack.error.SpecError, spack.error.SpecSyntaxError) as error:
                raise _policy_error(
                    policy_name,
                    path,
                    f"empty_directory_paths[{index}].unless_external_specs",
                    f"invalid spec {constraint!r}: {error}",
                ) from error


def _load_sandbox_policy(path: str = SANDBOX_POLICY_PATH) -> dict:
    """Load and validate the shipped namespace sandbox compatibility policy."""
    policy_name = "sandbox policy"
    policy = _load_policy_document(policy_name, path)
    if "commands" in policy:
        raise _policy_error(
            policy_name, path, "commands", "Landlock command stubs are unsupported"
        )

    list_keys = (
        "host_runtime_read_paths",
        "file_runtime_read_paths",
        "compiler_languages",
        "compiler_programs",
        "binutils_programs",
        "coreutils_install_programs",
        "coreutils_file_programs",
        "coreutils_util_programs",
        "build_utilities_programs",
        "script_interpreter_programs",
        "compiler_files",
        "stage_programs",
        "device_nodes",
    )
    for key in list_keys:
        _validate_string_list(policy_name, path, policy, key)
    for key in ("hidden_roots", "replacement_roots", "tmpfs_paths", "mount_plan_scratch_paths"):
        _validate_absolute_path_list(policy_name, path, policy, key)
    _validate_empty_directory_paths(policy_name, path, policy)

    device_symlinks = policy.get("device_symlinks")
    if not isinstance(device_symlinks, dict) or not all(
        isinstance(link, str)
        and os.path.isabs(link)
        and isinstance(target, str)
        and os.path.isabs(target)
        for link, target in device_symlinks.items()
    ):
        raise _policy_error(
            policy_name, path, "device_symlinks", "expected an absolute path-to-target mapping"
        )

    aliases = policy.get("compiler_driver_aliases")
    languages = policy.get("compiler_languages")
    if not isinstance(aliases, dict) or set(aliases) != set(languages):
        raise _policy_error(
            policy_name,
            path,
            "compiler_driver_aliases",
            "expected exactly one string-list entry for each compiler language",
        )
    for language in languages:
        aliases_for_language = aliases.get(language)
        if not isinstance(aliases_for_language, list) or not all(
            isinstance(entry, str) for entry in aliases_for_language
        ):
            raise _policy_error(
                policy_name,
                path,
                f"compiler_driver_aliases.{language}",
                "expected a list of strings",
            )
    return policy


def _validate_relative_header_paths(path: str, policy: dict, section: str, key: str) -> None:
    full_key = f"{section}.{key}"
    value = policy[section].get(key)
    if not isinstance(value, list) or not all(isinstance(entry, str) for entry in value):
        raise _policy_error("Linux header policy", path, full_key, "expected a list of strings")
    for entry in value:
        normalized = entry.replace("\\", "/")
        if (
            not normalized
            or os.path.isabs(entry)
            or normalized.startswith("/")
            or ".." in normalized.split("/")
        ):
            raise _policy_error(
                "Linux header policy", path, full_key, f"unsafe relative path {entry!r}"
            )


def _load_linux_header_policy(path: str = LINUX_HEADER_POLICY_PATH) -> dict:
    """Load and validate the shipped Linux system-header policy."""
    policy = _load_policy_document("Linux header policy", path)
    include_root = policy.get("system_include_root")
    if not isinstance(include_root, str) or not os.path.isabs(include_root):
        raise _policy_error(
            "Linux header policy", path, "system_include_root", "expected an absolute path"
        )
    _validate_absolute_path_list("Linux header policy", path, policy, "compiler_roots")

    for section in ("glibc", "linux"):
        value = policy.get(section)
        if not isinstance(value, dict):
            raise _policy_error("Linux header policy", path, section, "expected a mapping")
        required_keys = (
            ("files", "directories", "target_files", "target_directories")
            if section == "glibc"
            else ("directories", "target_directories")
        )
        for key in required_keys:
            _validate_relative_header_paths(path, policy, section, key)
    libstdcxx = policy.get("libstdcxx")
    if (
        not isinstance(libstdcxx, dict)
        or type(libstdcxx.get("maximum_major_for_non_gcc")) is not int
    ):
        raise _policy_error(
            "Linux header policy",
            path,
            "libstdcxx.maximum_major_for_non_gcc",
            "expected an integer",
        )
    return policy


def _selected_compilers(
    spec: spack.spec.Spec, policy: Optional[dict] = None
) -> List[Tuple[str, str, spack.spec.Spec]]:
    """Return selected language, driver path, and compiler spec tuples without duplicates."""
    policy = policy if policy is not None else _load_sandbox_policy()
    languages = tuple(policy["compiler_languages"])
    compiler_names = set(spack.compilers.config.supported_compilers(repo=spack.repo.PATH))
    result = []
    seen = set()

    for node in spec.traverse():
        for edge in node.edges_to_dependencies():
            selected_languages = set(edge.virtuals) & set(languages)
            configured = (edge.spec.extra_attributes or {}).get("compilers", {})
            for language in languages:
                path = configured.get(language)
                if language in selected_languages and path and (language, path) not in seen:
                    seen.add((language, path))
                    result.append((language, path, edge.spec))
        if node.name not in compiler_names:
            continue
        configured = (node.extra_attributes or {}).get("compilers", {})
        for language in languages:
            path = configured.get(language)
            if path and (language, path) not in seen:
                seen.add((language, path))
                result.append((language, path, node))
    return result


def _compiler_query(compiler_path: str, option: str) -> Optional[str]:
    try:
        completed = subprocess.run(
            [compiler_path, option],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    reported = completed.stdout.strip()
    return reported if os.path.isabs(reported) else None


def _resolved_sandbox_path(spelling: str, source: str) -> ResolvedSandboxPath:
    return ResolvedSandboxPath(spelling, os.path.realpath(source))


def _is_spack_binutils_wrapper(path: str) -> bool:
    parts = Path(path).parts
    return any(parts[index : index + 2] == ("libexec", "spack") for index in range(len(parts) - 1))


def compiler_support_paths(
    compiler_path: str, policy: Optional[dict] = None
) -> List[ResolvedSandboxPath]:
    """Return compiler-reported support programs and files without PATH fallback."""
    policy = policy if policy is not None else _load_sandbox_policy()
    result = []
    for program in policy["compiler_programs"] + policy["binutils_programs"]:
        reported = _compiler_query(compiler_path, f"-print-prog-name={program}")
        if reported is None or (
            program in policy["binutils_programs"] and _is_spack_binutils_wrapper(reported)
        ):
            continue
        result.append(_resolved_sandbox_path(program, reported))

    for filename in policy["compiler_files"]:
        reported = _compiler_query(compiler_path, f"-print-file-name={filename}")
        if reported is not None:
            result.append(_resolved_sandbox_path(filename, reported))
    return result


def compiler_driver_paths(
    spec: spack.spec.Spec, policy: Optional[dict] = None
) -> List[ResolvedSandboxPath]:
    """Return selected compiler drivers and the first target for each alias spelling."""
    policy = policy if policy is not None else _load_sandbox_policy()
    result = []
    seen = set()
    for language, compiler_path, _compiler_spec in _selected_compilers(spec, policy):
        source = os.path.realpath(compiler_path)
        spellings = [compiler_path]
        spellings.extend(
            os.path.join(os.path.dirname(compiler_path), alias)
            for alias in policy["compiler_driver_aliases"][language]
        )
        for spelling in spellings:
            entry = _resolved_sandbox_path(spelling, source)
            if entry.spelling not in seen:
                seen.add(entry.spelling)
                result.append(entry)
    return result


def compiler_alias_symlink_paths(
    spec: spack.spec.Spec, policy: Optional[dict] = None
) -> List[spack.sandbox_namespaces.NamespaceGeneratedSymlink]:
    """Convert selected compiler alias spellings into generated namespace symlinks."""
    return [
        spack.sandbox_namespaces.NamespaceGeneratedSymlink(entry.spelling, entry.source)
        for entry in compiler_driver_paths(spec, policy)
        if entry.spelling != entry.source
    ]


def executable_support_paths(
    executable: str, policy: Optional[dict] = None
) -> List[ResolvedSandboxPath]:
    """Return exact data files required by a selected executable."""
    policy = policy if policy is not None else _load_sandbox_policy()
    if os.path.basename(executable) == "file":
        return [
            _resolved_sandbox_path(path, path)
            for path in policy["file_runtime_read_paths"]
            if os.path.exists(path)
        ]
    if os.path.basename(executable) != "cpp":
        return []
    reported = _compiler_query(executable, "-print-prog-name=cc1")
    return [_resolved_sandbox_path("cc1", reported)] if reported is not None else []


def git_support_paths(git_path: str) -> List[ResolvedSandboxPath]:
    """Return Git's configured helper directory, without searching for Git again."""
    try:
        completed = subprocess.run(
            [git_path, "--exec-path"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
        )
    except OSError:
        return []
    exec_path = completed.stdout.strip()
    if completed.returncode != 0 or not os.path.isabs(exec_path):
        return []
    return [_resolved_sandbox_path(f"{git_path} --exec-path", exec_path)]


def _tool_paths_for_programs(programs: Iterable[str]) -> List[ResolvedSandboxPath]:
    helper_closure = {"gunzip": ("gzip", "sh"), "bunzip2": ("bzip2", "sh")}
    names = list(programs)
    for name in tuple(names):
        for helper in helper_closure.get(name, ()):
            if helper not in names:
                names.append(helper)

    result = []
    seen = set()
    for name in names:
        source = which_string(name)
        if source is None:
            continue
        entry = _resolved_sandbox_path(name, source)
        if (entry.spelling, entry.source) not in seen:
            seen.add((entry.spelling, entry.source))
            result.append(entry)
        if name == "git":
            for support in git_support_paths(source):
                if (support.spelling, support.source) not in seen:
                    seen.add((support.spelling, support.source))
                    result.append(support)
    return result


def stage_tool_paths(policy: Optional[dict] = None) -> List[ResolvedSandboxPath]:
    """Select fetch and expansion tools, their helper chain, and Git support."""
    policy = policy if policy is not None else _load_sandbox_policy()
    return _tool_paths_for_programs(policy["stage_programs"])


def install_tool_paths(policy: Optional[dict] = None) -> List[ResolvedSandboxPath]:
    """Select coreutils and build utilities needed during package installation."""
    policy = policy if policy is not None else _load_sandbox_policy()
    program_groups = (
        "binutils_programs",
        "coreutils_install_programs",
        "coreutils_file_programs",
        "coreutils_util_programs",
        "build_utilities_programs",
        "script_interpreter_programs",
    )
    return _tool_paths_for_programs(
        program for group in program_groups for program in policy[group]
    )


def tool_alias_symlink_paths(
    tool_entries: Iterable[ResolvedSandboxPath], hidden_roots: Iterable[str]
) -> List[spack.sandbox_namespaces.NamespaceGeneratedSymlink]:
    """Restore selected tool spellings when their executables are symlinks."""
    result = []
    for entry in tool_entries:
        spelling = which_string(entry.spelling)
        if spelling is None:
            continue
        spelling = os.path.abspath(spelling)
        alias = os.path.join(
            os.path.realpath(os.path.dirname(spelling)), os.path.basename(spelling)
        )
        if alias == entry.source or os.path.realpath(spelling) != entry.source:
            continue
        if any(os.path.commonpath((root, alias)) == root for root in hidden_roots):
            result.append(spack.sandbox_namespaces.NamespaceGeneratedSymlink(alias, entry.source))
    return result


def _canonical_existing_paths(
    paths: Iterable[str], *, character_devices: bool = False
) -> Tuple[str, ...]:
    result = []
    seen = set()
    for path in paths:
        resolved = os.path.realpath(os.path.abspath(path))
        if not os.path.exists(resolved):
            continue
        if character_devices and not stat.S_ISCHR(os.stat(resolved).st_mode):
            continue
        if resolved not in seen:
            seen.add(resolved)
            result.append(resolved)
    return tuple(sorted(result))


def _canonical_required_paths(paths: Iterable[str], category: str) -> Tuple[str, ...]:
    result = []
    seen = set()
    for path in paths:
        absolute = os.path.abspath(path)
        resolved = os.path.realpath(absolute)
        if not os.path.lexists(absolute):
            raise spack.sandbox_namespaces.NamespaceSetupError(
                errno.ENOENT,
                "select namespace policy inputs",
                f"{category} path does not exist: {path}",
            )
        if absolute != resolved:
            raise spack.sandbox_namespaces.NamespaceSetupError(
                errno.EINVAL,
                "select namespace policy inputs",
                f"{category} path is not canonical: {path} resolves to {resolved}",
            )
        if resolved not in seen:
            seen.add(resolved)
            result.append(resolved)
    return tuple(sorted(result))


def select_namespace_host_device_worker_paths(
    config: dict,
    spec: spack.spec.Spec,
    stage_path: str,
    *,
    log_path: Optional[str],
    jobserver_paths: Iterable[str],
    worker_root: str,
    fetch_cache_path: str,
    policy: Optional[dict] = None,
) -> NamespaceHostDeviceWorkerPaths:
    """Select host, device, and worker-state inputs without changing the worker filesystem.

    Host runtime paths are candidates and are omitted when unavailable. Lifecycle and worker
    paths are explicit trusted inputs and fail closed when missing or non-canonical.
    """
    policy = policy if policy is not None else _load_sandbox_policy()
    hidden_roots = _canonical_existing_paths(policy["hidden_roots"])
    replacement_roots = tuple(
        root
        for root in _canonical_existing_paths(policy["replacement_roots"])
        if root in hidden_roots
    )
    host_runtime_paths = _canonical_existing_paths(
        policy["host_runtime_read_paths"]
        + policy["file_runtime_read_paths"]
        + spack.util.ld_so_conf.host_dynamic_linker_search_paths()
    )
    device_paths = _canonical_existing_paths(policy["device_nodes"], character_devices=True)

    repositories = tuple(spack.repo.PATH.repos)
    read_only_candidates = [
        spack.paths.bin_path,
        spack.paths.lib_path,
        spack.paths.share_path,
        spack.paths.etc_path,
        spack.paths.user_config_path,
        spack.paths.system_config_path,
        *host_runtime_paths,
        *[str(dep.prefix) for dep in spec.traverse(root=False) if not dep.external],
        *[repo.root for repo in repositories],
        *[repo.python_path for repo in repositories if getattr(repo, "python_path", None)],
        os.path.join(spack.store.STORE.unpadded_root, "bin", "sbang"),
        *[
            os.path.join(upstream_db.root, "bin", "sbang")
            for upstream_db in spack.store.STORE.upstreams or ()
        ],
        spack.paths.user_cache_path,
        spack.caches.misc_cache_location(config=spack.config.CONFIG),
        *config.get("allow_read", []),
    ]
    read_only_paths = _canonical_existing_paths(read_only_candidates)

    required_worker_paths = [stage_path, str(spec.prefix), worker_root, fetch_cache_path]
    if log_path is not None:
        required_worker_paths.append(log_path)
    required_worker_paths.extend(jobserver_paths)
    writable_paths = list(_canonical_required_paths(required_worker_paths, "worker"))
    writable_paths.extend(_canonical_existing_paths(config.get("allow_write", [])))

    return NamespaceHostDeviceWorkerPaths(
        hidden_roots,
        replacement_roots,
        host_runtime_paths,
        device_paths,
        read_only_paths,
        tuple(sorted(set(writable_paths))),
    )


def tool_runtime_paths(spec: spack.spec.Spec, tool_paths) -> List[str]:
    """Return Spack tool prefixes and link/run dependency prefixes owning selected tools."""
    sources = [
        path.source if isinstance(path, ResolvedSandboxPath) else os.path.realpath(path)
        for path in tool_paths
    ]
    result = []
    seen = set()
    for node in spec.traverse():
        if getattr(node, "external", False):
            continue
        prefix = os.path.realpath(str(node.prefix))
        try:
            owns_tool = any(os.path.commonpath((source, prefix)) == prefix for source in sources)
        except ValueError:
            owns_tool = False
        if not owns_tool:
            continue
        for path in [str(node.prefix)] + [
            str(dependency.prefix)
            for dependency in node.traverse(root=False, deptype=("link", "run"))
        ]:
            resolved = os.path.realpath(path)
            if resolved not in seen:
                seen.add(resolved)
                result.append(resolved)
    return result


def _gcc_installation(compiler_path: str, policy: Optional[dict] = None) -> Optional[Path]:
    """Return the system GCC installation directory reported by a compiler driver."""
    policy = policy if policy is not None else _load_linux_header_policy()
    try:
        completed = subprocess.run(
            [compiler_path, "-print-libgcc-file-name"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
        )
    except OSError:
        return None
    if completed.returncode != 0 or not os.path.isabs(completed.stdout.strip()):
        return None
    installation = Path(completed.stdout.strip()).resolve().parent
    roots = tuple(Path(root).resolve() for root in policy["compiler_roots"])
    return installation if installation.parent.parent in roots else None


def _versioned_directories_by_major(root: Path) -> Dict[int, List[Path]]:
    """Return immediate child directories grouped by numeric major version."""
    result: Dict[int, List[Path]] = {}
    try:
        entries = sorted(root.iterdir())
    except OSError:
        return result
    for entry in entries:
        if not entry.is_dir():
            continue
        try:
            major = int(entry.name.split(".", 1)[0])
        except ValueError:
            continue
        result.setdefault(major, []).append(entry)
    return result


def _major_version(value) -> Optional[int]:
    try:
        return int(str(value).split(".", 1)[0])
    except (TypeError, ValueError):
        return None


def _permitted_gcc_installation(
    compiler_path: str, compiler_spec: spack.spec.Spec, policy: dict
) -> Optional[Path]:
    """Select the GCC installation whose libstdc++ headers may be read."""
    reported = _gcc_installation(compiler_path, policy)
    if reported is None:
        return None
    installations = _versioned_directories_by_major(reported.parent)
    if compiler_spec.name == "gcc":
        candidates = [reported]
    else:
        maximum_major = policy["libstdcxx"]["maximum_major_for_non_gcc"]
        safe_majors = [major for major in installations if major <= maximum_major]
        permitted_major = max(safe_majors) if safe_majors else _major_version(reported.name)
        candidates = installations.get(permitted_major, []) if permitted_major is not None else []
    if not candidates:
        return None
    header_root = Path(policy["system_include_root"]) / "c++"
    return next(
        (path for path in reversed(candidates) if (header_root / path.name).is_dir()), None
    )


def _policy_paths(root: Path, values) -> List[str]:
    """Resolve safe relative policy entries below a trusted root."""
    result = []
    for value in values:
        if not isinstance(value, str) or os.path.isabs(value) or ".." in Path(value).parts:
            raise spack.error.InstallError(f"Invalid relative Linux header policy path: {value!r}")
        result.append(str(root / value))
    return result


def system_compiler_header_paths(
    spec: spack.spec.Spec, policy: Optional[dict] = None
) -> List[str]:
    """Return explicit libc, Linux UAPI, and selected libstdc++ header paths."""
    policy = policy if policy is not None else _load_linux_header_policy()
    selected = _selected_compilers(spec)
    system_selected = [
        entry
        for entry in selected
        if os.path.commonpath((str(Path(entry[1]).resolve()), "/usr")) == "/usr"
    ]
    if not system_selected:
        return []

    include_root = Path(policy["system_include_root"])
    paths = _policy_paths(
        include_root,
        policy["glibc"]["files"]
        + policy["glibc"]["directories"]
        + policy["glibc"]["target_files"]
        + policy["glibc"]["target_directories"]
        + policy["linux"]["directories"]
        + policy["linux"]["target_directories"],
    )
    targets = set()
    for _language, compiler_path, _compiler_spec in system_selected:
        installation = _gcc_installation(compiler_path, policy)
        if installation is not None:
            targets.add(installation.parent.name)
    for target in targets:
        target_root = include_root / target
        paths.extend(
            _policy_paths(
                target_root,
                policy["glibc"]["target_files"]
                + policy["glibc"]["target_directories"]
                + policy["linux"]["target_directories"],
            )
        )

    for language, compiler_path, compiler_spec in system_selected:
        installation = _gcc_installation(compiler_path, policy)
        if installation is None:
            continue
        if language == "cxx":
            installation = _permitted_gcc_installation(compiler_path, compiler_spec, policy)
            if installation is None:
                continue
            version = installation.name
            paths.extend(
                [
                    str(include_root / "c++" / version),
                    str(include_root / installation.parent.name / "c++" / version),
                    str(include_root / "c++" / version / installation.parent.name),
                ]
            )
        paths.extend([str(installation / "include"), str(installation / "include-fixed")])
    return list(dict.fromkeys(paths))


def gcc_installation_dirs_to_mask(
    spec: spack.spec.Spec, policy: Optional[dict] = None
) -> List[str]:
    """Hide system GCC installations other than the permitted selected C++ installation."""
    policy = policy if policy is not None else _load_linux_header_policy()
    selected = _selected_compilers(spec, _load_sandbox_policy())
    required_installations = {
        installation
        for _language, compiler_path, compiler_spec in selected
        for installation in [_gcc_installation(compiler_path, policy)]
        if compiler_spec.name == "gcc" and installation is not None
    }
    for language, compiler_path, compiler_spec in selected:
        if (
            language != "cxx"
            or os.path.commonpath((str(Path(compiler_path).resolve()), "/usr")) != "/usr"
        ):
            continue
        permitted = _permitted_gcc_installation(compiler_path, compiler_spec, policy)
        if permitted is None:
            return []
        return [
            str(path)
            for paths in _versioned_directories_by_major(permitted.parent).values()
            for path in paths
            if path != permitted and path not in required_installations
        ]
    return []


class ChildInfo:
    """Loop-side handle to a running build: the child process and its IPC channels. Owns the
    prefix write lock while the build runs; on success ownership transfers to the pending
    ``AddSpecAction`` DB insert."""

    __slots__ = (
        "proc",
        "spec",
        "output_r_conn",
        "state_r_conn",
        "control_w_conn",
        "notifier",
        "log_path",
        "prefix_lock",
        "lifecycle",
        "state_buffer",
    )

    def __init__(
        self,
        proc: ProcessLike,
        spec: spack.spec.Spec,
        output_r_conn: IpcChannel,
        state_r_conn: IpcChannel,
        control_w_conn: IpcChannel,
        notifier: ProcessExitNotifier,
        log_path: str,
        lifecycle: Optional["BuildLifecycle"] = None,
    ) -> None:
        self.proc = proc
        self.spec = spec
        self.output_r_conn = output_r_conn
        self.state_r_conn = state_r_conn
        self.control_w_conn = control_w_conn
        self.notifier = notifier
        self.log_path = log_path
        self.prefix_lock: Optional[spack.util.lock.Lock] = None
        self.lifecycle = lifecycle
        # Buffer for partially received state data from this child. Kept as raw bytes and split on
        # b"\n": the newline byte cannot occur inside a multi-byte UTF-8 sequence, so framing is
        # safe without decoding partial reads.
        self.state_buffer = b""

    def release_prefix_lock(self) -> None:
        if self.prefix_lock is not None:
            try:
                self.prefix_lock.release_write()
            except Exception:
                pass
        self.prefix_lock = None

    def finalize_lifecycle(self, exitcode: int) -> None:
        if self.lifecycle is not None:
            self.lifecycle.finalize(exitcode)

    def register_with_selector(self, selector: selectors.BaseSelector, build_id: str) -> None:
        """Register output, state, and sentinel channels with the selector."""
        selector.register(self.output_r_conn, selectors.EVENT_READ, FdInfo(build_id, "output"))
        selector.register(self.state_r_conn, selectors.EVENT_READ, FdInfo(build_id, "state"))
        selector.register(
            self.notifier.fileobj, selectors.EVENT_READ, FdInfo(build_id, "sentinel")
        )

    def close(self, selector: selectors.BaseSelector) -> int:
        """Unregister and close file descriptors, and join the child process.
        Returns the exit code of the child process."""
        try:
            selector.unregister(self.output_r_conn)
        except (KeyError, OSError):
            pass
        try:
            selector.unregister(self.state_r_conn)
        except (KeyError, OSError):
            pass
        try:
            selector.unregister(self.notifier.fileobj)
        except (KeyError, ValueError, OSError):
            pass
        self.output_r_conn.close()
        self.state_r_conn.close()
        self.control_w_conn.close()
        self.notifier.close()
        self.proc.join()
        exit_code = self.proc.exitcode
        assert exit_code is not None, "Finished build should have exit code set"
        if hasattr(self.proc, "close"):  # No known equivalent in Python 3.6
            self.proc.close()
        return exit_code


def dump_packages(spec: spack.spec.Spec, path: str) -> None:
    """
    Dump all package information for a spec and its dependencies.

    This creates a package repository within path for every namespace in the
    spec DAG, and fills the repos with package files and patch files for every
    node in the DAG.

    Args:
        spec: the Spack spec whose package information is to be dumped
        path: the path to the build packages directory
    """
    fs.mkdirp(path)

    # Copy in package.py files from any dependencies.
    # Note that we copy them in as they are in the *install* directory
    # NOT as they are in the repository, because we want a snapshot of
    # how *this* particular build was done.
    for node in spec.traverse(deptype="all"):
        assert node.namespace is not None
        if node is not spec:
            # Locate the dependency package in the install tree and find
            # its provenance information.
            source = spack.store.STORE.layout.build_packages_path(node)
            source_repo_root = os.path.join(source, node.namespace)

            # If there's no provenance installed for the package, skip it.
            # If it's external, skip it because it either:
            # 1) it wasn't built with Spack, so it has no Spack metadata
            # 2) it was built by another Spack instance, and we do not
            # (currently) use Spack metadata to associate repos with externals
            # built by other Spack instances.
            # Spack can always get something current from the builtin repo.
            if node.external or not os.path.isdir(source_repo_root):
                continue

            # Create a source repo and get the pkg directory out of it.
            try:
                source_repo = spack.repo.from_path(source_repo_root)
                source_pkg_dir = source_repo.dirname_for_package_name(node.name)
            except spack.repo.RepoError as err:
                spack.util.tty.debug(f"Failed to create source repo for {node.name}: {str(err)}")
                source_pkg_dir = None
                spack.util.tty.warn(f"Warning: Couldn't copy in provenance for {node.name}")

        # Create a destination repository
        pkg_api = spack.repo.PATH.get_repo(node.namespace).package_api
        repo_root = os.path.join(path, node.namespace) if pkg_api < (2, 0) else path
        repo = spack.repo.create_or_construct(
            repo_root, namespace=node.namespace, package_api=pkg_api
        )

        # Get the location of the package in the dest repo.
        dest_pkg_dir = repo.dirname_for_package_name(node.name)
        if node is spec:
            spack.repo.PATH.dump_provenance(node, dest_pkg_dir)
        elif source_pkg_dir:
            fs.install_tree(source_pkg_dir, dest_pkg_dir)


def _do_fake_install(pkg: "spack.package_base.PackageBase") -> None:
    """Make a fake install directory with fake executables, headers, and libraries."""
    command = pkg.name
    header = pkg.name
    library = pkg.name

    # Avoid double 'lib' for packages whose names already start with lib
    if not pkg.name.startswith("lib"):
        library = "lib" + library

    plat_shared = ".dll" if sys.platform == "win32" else ".so"
    plat_static = ".lib" if sys.platform == "win32" else ".a"
    dso_suffix = ".dylib" if sys.platform == "darwin" else plat_shared

    # Install fake command
    fs.mkdirp(pkg.prefix.bin)
    executable = lambda path, flags: os.open(path, flags, 0o700)
    open(os.path.join(pkg.prefix.bin, command), "wb", opener=executable).close()

    # Install fake header file
    fs.mkdirp(pkg.prefix.include)
    fs.touch(os.path.join(pkg.prefix.include, header + ".h"))

    # Install fake shared and static libraries
    fs.mkdirp(pkg.prefix.lib)
    for suffix in [dso_suffix, plat_static]:
        fs.touch(os.path.join(pkg.prefix.lib, library + suffix))

    # Install fake man page
    fs.mkdirp(pkg.prefix.man.man1)

    packages_dir = spack.store.STORE.layout.build_packages_path(pkg.spec)
    dump_packages(pkg.spec, packages_dir)


def _write_timer_json(
    pkg: "spack.package_base.PackageBase", timer: spack.util.timer.Timer, cache: bool
) -> None:
    extra_attributes = {"name": pkg.name, "cache": cache, "hash": pkg.spec.dag_hash()}
    try:
        with open(pkg.times_log_path, "w", encoding="utf-8") as timelog:
            timer.write_json(timelog, extra_attributes=extra_attributes)
    except Exception as e:
        spack.util.tty.debug(str(e))
        return


def send_state(state: str, state_pipe: io.TextIOWrapper) -> None:
    """Send a state update message."""
    json.dump({"state": state}, state_pipe, separators=(",", ":"))
    state_pipe.write("\n")


def send_progress(current: int, total: int, state_pipe: io.TextIOWrapper) -> None:
    """Send a progress update message."""
    json.dump({"progress": current, "total": total}, state_pipe, separators=(",", ":"))
    state_pipe.write("\n")


def send_installed_from_binary_cache(state_pipe: io.TextIOWrapper) -> None:
    """Send a notification that the package was installed from binary cache."""
    json.dump({"installed_from_binary_cache": True}, state_pipe, separators=(",", ":"))
    state_pipe.write("\n")


def install_from_buildcache(
    mirrors: List[spack.url_buildcache.MirrorMetadata],
    spec: spack.spec.Spec,
    unsigned: Optional[bool],
    state_stream: io.TextIOWrapper,
    timer: spack.util.timer.BaseTimer = spack.util.timer.NULL_TIMER,
) -> bool:
    # Skip if no configured mirror accepts this spec (select/exclude filters)
    if not any(
        m.matches_binary(spec, direction="fetch")
        for m in spack.mirrors.mirror.MirrorCollection(binary=True).values()
    ):
        return False

    send_state("fetching from build cache", state_stream)
    try:
        with timer.measure("fetch"):
            tarball_stage = spack.binary_distribution.download_tarball(
                spec.build_spec, unsigned, mirrors
            )
    except spack.binary_distribution.NoConfiguredBinaryMirrors:
        return False

    if tarball_stage is None:
        return False

    send_state("relocating", state_stream)
    with timer.measure("install"):
        spack.binary_distribution.extract_tarball(spec, tarball_stage, force=False, timer=timer)

    if spec.spliced:  # overwrite old metadata with new
        spack.store.STORE.layout.write_spec(spec, spack.store.STORE.layout.spec_file_path(spec))

    # now a block of curious things follow that should be fixed.
    pkg = spec.package
    pkg.installed_from_binary_cache = True

    # inform also the parent that this package was installed from binary cache.
    send_installed_from_binary_cache(state_stream)

    return True


class PrefixPivoter:
    """Manages the installation prefix of a build."""

    def __init__(self, prefix: str, keep_prefix: bool = False) -> None:
        """Initialize the prefix pivoter.

        Args:
            prefix: The installation prefix path
            keep_prefix: Whether to keep a failed installation prefix
        """
        self.prefix = prefix
        #: Whether to keep a failed installation prefix
        self.keep_prefix = keep_prefix
        #: Temporary location for the original prefix
        self.tmp_prefix: Optional[str] = None
        self.parent = os.path.dirname(prefix)

    def __enter__(self) -> "PrefixPivoter":
        """Enter the context: move existing prefix to temporary location if needed."""
        self.prepare()
        return self

    def prepare(self, create_target: bool = False) -> None:
        """Move an existing prefix aside and optionally create the new target."""
        if self._lexists(self.prefix):
            self.tmp_prefix = self._mkdtemp(
                dir=self.parent, prefix=".", suffix=OVERWRITE_BACKUP_SUFFIX
            )
            self._rename(self.prefix, self.tmp_prefix)
        if create_target:
            fs.mkdirp(self.prefix)

    def __exit__(
        self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[object]
    ) -> None:
        """Exit the context: cleanup on success, restore on failure."""
        self.finalize(exc_type)

    def finalize(self, exc_type: Optional[type]) -> None:
        """Finalize the pivot after the worker has stopped using the prefix."""
        if exc_type is None:
            # Success: remove the backup
            if self.tmp_prefix is not None:
                self._rmtree_ignore_errors(self.tmp_prefix)
            return

        # Failure handling:
        if self.keep_prefix and not issubclass(exc_type, BinaryCacheMiss):
            # Leave the failed prefix in place, discard the backup. Except for binary cache misses,
            # which is a scheduling failure and not a build failure.
            if self.tmp_prefix is not None:
                self._rmtree_ignore_errors(self.tmp_prefix)
        elif self.tmp_prefix is not None:
            # There was a pre-existing prefix: pivot back to it and discard the failed build
            garbage = self._mkdtemp(dir=self.parent, prefix=".", suffix=OVERWRITE_GARBAGE_SUFFIX)
            try:
                self._rename(self.prefix, garbage)
                has_failed_prefix = True
            except FileNotFoundError:  # build never created the prefix dir
                has_failed_prefix = False
            self._rename(self.tmp_prefix, self.prefix)
            if has_failed_prefix:
                self._rmtree_ignore_errors(garbage)
        elif self._lexists(self.prefix):
            # No backup, just remove the failed installation
            garbage = self._mkdtemp(dir=self.parent, prefix=".", suffix=OVERWRITE_GARBAGE_SUFFIX)
            self._rename(self.prefix, garbage)
            self._rmtree_ignore_errors(garbage)

    def _lexists(self, path: str) -> bool:
        return os.path.lexists(path)

    def _rename(self, src: str, dst: str) -> None:
        fs.rename(src, dst)

    def _mkdtemp(self, dir: str, prefix: str, suffix: str) -> str:
        return tempfile.mkdtemp(dir=dir, prefix=prefix, suffix=suffix)

    def _rmtree_ignore_errors(self, path: str) -> None:
        shutil.rmtree(path, ignore_errors=True)


class BuildLifecycle:
    """Own host-backed stage and prefix transitions for one build."""

    def __init__(self, spec: spack.spec.Spec, keep_stage: bool, keep_prefix: bool = False) -> None:
        self.spec = spec
        self.keep_stage = keep_stage
        self.stage = spec.package.stage
        self.stage_parent: Optional[str] = None
        self.stage_path: Optional[str] = None
        self.prefix_pivoter = PrefixPivoter(str(spec.prefix), keep_prefix=keep_prefix)
        self.namespace_mount_plan_scratch: Optional[
            spack.sandbox_namespaces.NamespaceMountPlanScratch
        ] = None
        self._prepared = False
        self._finalized = False

    def prepare(self, create_prefix_target: bool = False) -> None:
        """Allocate a private stage parent and prepare the empty install target."""
        stage_root = self.stage[0].stage_root
        fs.mkdirp(stage_root)
        self.stage_parent = tempfile.mkdtemp(dir=stage_root, prefix=".spack-stage-")
        previous_stage = None
        previous_stage_path = os.path.join(stage_root, self.stage[0].name)
        if os.path.lexists(previous_stage_path):
            previous_stage = tempfile.mkdtemp(dir=stage_root, prefix=".spack-stage-previous-")
            os.rmdir(previous_stage)
            fs.rename(previous_stage_path, previous_stage)
        for stage in self.stage:
            stage.path = os.path.join(self.stage_parent, stage.name)
        if previous_stage is not None:
            fs.rename(previous_stage, self.stage.path)
        self.stage_path = self.stage.path
        try:
            self.prefix_pivoter.prepare(create_target=create_prefix_target)
        except BaseException:
            shutil.rmtree(self.stage_parent, ignore_errors=True)
            raise
        self._prepared = True

    def finalize(self, exitcode: int) -> None:
        """Finalize host paths after the child namespace and process are gone."""
        if not self._prepared or self._finalized:
            return
        try:
            if exitcode == ExitCode.SUCCESS:
                self.prefix_pivoter.finalize(None)
            elif exitcode == ExitCode.BUILD_CACHE_MISS:
                self.prefix_pivoter.finalize(BinaryCacheMiss)
            else:
                self.prefix_pivoter.finalize(RuntimeError)
            if exitcode in (ExitCode.SUCCESS, ExitCode.BUILD_CACHE_MISS) and not self.keep_stage:
                assert self.stage_parent is not None
                self.stage[0].path = os.path.join(self.stage[0].stage_root, self.stage[0].name)
                shutil.rmtree(self.stage_parent, ignore_errors=True)
        finally:
            if self.namespace_mount_plan_scratch is not None:
                self.namespace_mount_plan_scratch.cleanup()
                self.namespace_mount_plan_scratch = None
            self._finalized = True


class BuildRequest(NamedTuple):
    """Plain data describing a single build to be launched: the input of a build launcher."""

    spec: spack.spec.Spec
    explicit: bool
    mirrors: List[spack.url_buildcache.MirrorMetadata]
    unsigned: Optional[bool]
    install_policy: InstallPolicy
    dirty: bool
    keep_stage: bool
    restage: bool
    keep_prefix: bool
    skip_patch: bool
    fake: bool
    install_source: bool
    run_tests: bool
    log_path: str
    stop_before: Optional[str]
    stop_at: Optional[str]
    stage_parent: Optional[str] = None
    stage_path: Optional[str] = None
    namespace_activation: Optional[NamespaceActivation] = None


def worker_function(
    request: BuildRequest,
    state: IpcChannel,
    parent: IpcChannel,
    tee_control_r: IpcChannel,
    tee_control_w: Optional[IpcChannel],
    makeflags: Makeflags,
    global_state: GlobalStateMarshaler,
) -> None:
    """
    Function run in the build child process. Installs the requested spec, sending state updates
    and build output back to the parent process.

    Args:
        request: Description of the build to perform
        state: Connection to send state updates to
        parent: Connection to send build output to
        tee_control_r: Read end of the control pipe; the parent sends echo on/off here
        tee_control_w: Write end of the control pipe; used to stop the tee thread on POSIX
        makeflags: Sets MAKEFLAGS in this process, so that the build uses Spack's jobserver
        global_state: Global state to restore
    """
    spec, log_path = request.spec, request.log_path

    # TODO: don't start a build for external packages
    if spec.external:
        return

    global_state.restore()

    if sys.platform != "win32":
        # Isolate the process group to shield against Ctrl+C and enable safe killpg() cleanup. In
        # contrast to setsid(), this keeps a neat process group hierarchy for utils like pstree.
        os.setpgid(0, 0)

        # Reset SIGTSTP to default in case the parent had a custom handler.
        signal.signal(signal.SIGTSTP, signal.SIG_DFL)

    def handle_sigterm(signum, frame):
        # This SIGTERM handler forwards the signal to child processes (cmake, make, etc). We wait
        # for all child processes to exit before raising KeyboardInterrupt. This ensures all
        # __exit__ and finally blocks run after the child processes have stopped, meaning that we
        # get to clean up the prefix without risking that the child process writes to it
        # afterwards.
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        if sys.platform != "win32":
            os.killpg(0, signal.SIGTERM)
            try:
                while True:
                    os.waitpid(-1, 0)
            except ChildProcessError:
                pass

        raise KeyboardInterrupt("Installation interrupted")

    signal.signal(signal.SIGTERM, handle_sigterm)

    makeflags.apply(os.environ)

    # Save encodings before the Tee redirects fds 1/2 to the pipe. We need them to create the
    # line-buffered wrappers after the Tee starts.
    _stdout_enc = sys.stdout.encoding or "utf-8"
    _stderr_enc = sys.stderr.encoding or "utf-8"

    # Detach stdin from the terminal like `./build < /dev/null`. This would not be necessary if we
    # used os.setsid() instead of os.setpgid(), but that would "break" pstree output.
    sys.stdin = open(os.devnull, "r", encoding=sys.stdin.encoding)
    os.dup2(sys.stdin.fileno(), 0)

    tee, state_stream, sandbox = _start_worker_output(
        spack.config.CONFIG.get("config:sandbox", {}),
        state,
        tee_control_r,
        tee_control_w,
        parent,
        log_path,
        spec=spec,
        stage_path=request.stage_parent or request.stage_path or spec.package.stage.path,
        namespace_activation=request.namespace_activation,
    )

    # Use closefd=False because of the connection objects. Use line buffering.
    # Replace sys.stdout/stderr AFTER the Tee redirected fds 1/2 so Python creates FileIO
    # (WriteFile) rather than ConsoleIO (WriteConsoleW). On Windows, if fds 1/2 are still console
    # handles when os.fdopen() is called, Python picks ConsoleIO; WriteConsoleW on a pipe handle
    # returns ERROR_INVALID_FUNCTION. Post-redirect the fds are pipe handles, so FileIO is chosen.
    sys.stdout = os.fdopen(
        sys.stdout.fileno(), "w", buffering=1, encoding=_stdout_enc, closefd=False
    )
    sys.stderr = os.fdopen(
        sys.stderr.fileno(), "w", buffering=1, encoding=_stderr_enc, closefd=False
    )
    exit_code = ExitCode.SUCCESS

    try:
        _install(request, state_stream, spack.store.STORE, sandbox=sandbox)
    except spack.error.StopPhase:
        exit_code = ExitCode.STOPPED_AT_PHASE
    except ProcessError as e:
        print(e, file=sys.stderr)
        exit_code = ExitCode.BUILD_ERROR
    except BinaryCacheMiss:
        exit_code = ExitCode.BUILD_CACHE_MISS
    except BaseException:
        traceback.print_exc(limit=-4)
        exit_code = ExitCode.BUILD_ERROR
    finally:
        tee.close()
        state_stream.close()

    if exit_code == ExitCode.SUCCESS:
        # Try to install the compressed log file
        if not os.path.lexists(spec.package.install_log_path):
            try:
                with open(log_path, "rb") as f, open(spec.package.install_log_path, "wb") as g:
                    # Use GzipFile directly so we can omit filename / mtime in header
                    gzip_file = GzipFile(
                        filename="", mode="wb", compresslevel=6, mtime=0, fileobj=g
                    )
                    shutil.copyfileobj(f, gzip_file)
                    gzip_file.close()
            except Exception:
                pass  # don't fail the build just because log compression failed

    sys.exit(exit_code)


def _archive_build_metadata(pkg: "spack.package_base.PackageBase") -> None:
    """Copy build metadata from stage to install prefix .spack directory.

    Mirrors what the old installer's log() function does in the parent process.
    Only called after a successful source build (not for binary cache installs).
    Errors are suppressed to avoid failing the build over metadata archiving."""

    try:
        if os.path.lexists(pkg.env_mods_path):
            shutil.copy2(pkg.env_mods_path, pkg.install_env_path)
    except OSError as e:
        spack.util.tty.debug(e)
    try:
        if os.path.lexists(pkg.configure_args_path):
            shutil.copy2(pkg.configure_args_path, pkg.install_configure_args_path)
    except OSError as e:
        spack.util.tty.debug(e)

    # Archive install-phase test log if present
    try:
        pkg.archive_install_test_log()
    except Exception as e:
        spack.util.tty.debug(e)

    # Archive package-specific files matched by archive_files glob patterns
    try:
        with fs.working_dir(pkg.stage.path):
            target_dir = os.path.join(
                spack.store.STORE.layout.metadata_path(pkg.spec), "archived-files"
            )
            errors = io.StringIO()
            for glob_expr in spack.builder.create(pkg).archive_files:
                abs_expr = os.path.realpath(glob_expr)
                if os.path.realpath(pkg.stage.path) not in abs_expr:
                    errors.write(f"[OUTSIDE SOURCE PATH]: {glob_expr}\n")
                    continue
                if os.path.isabs(glob_expr):
                    glob_expr = os.path.relpath(glob_expr, pkg.stage.path)
                for f in glob.glob(glob_expr):
                    try:
                        target = os.path.join(target_dir, f)
                        fs.mkdirp(os.path.dirname(target))
                        fs.install(f, target)
                    except Exception as e:
                        spack.util.tty.debug(e)
                        errors.write(f"[FAILED TO ARCHIVE]: {f}")
            if errors.getvalue():
                error_file = os.path.join(target_dir, "errors.txt")
                fs.mkdirp(target_dir)
                with open(error_file, "w", encoding="utf-8") as err:
                    err.write(errors.getvalue())
                spack.util.tty.warn(f"Errors occurred when archiving files.\n\tSee: {error_file}")
    except Exception as e:
        spack.util.tty.debug(e)

    try:
        packages_dir = spack.store.STORE.layout.build_packages_path(pkg.spec)
        dump_packages(pkg.spec, packages_dir)
    except Exception as e:
        spack.util.tty.debug(e)

    try:
        spack.store.STORE.layout.write_host_environment(pkg.spec)
    except Exception as e:
        spack.util.tty.debug(e)


def configured_empty_directory_paths(
    spec: spack.spec.Spec, policy: Optional[dict] = None
) -> List[str]:
    """Return policy-configured host directories hidden as empty for this build."""
    policy = policy if policy is not None else _load_sandbox_policy()
    external_dependencies = [
        dep for dep in spec.traverse(root=False) if getattr(dep, "external", False)
    ]
    return [
        entry["path"]
        for entry in policy["empty_directory_paths"]
        if not any(
            any(
                dependency.satisfies(constraint, deps=False)
                for dependency in external_dependencies
            )
            for constraint in entry.get("unless_external_specs", [])
        )
    ]


def namespace_filesystem_policy_from_inputs(
    config: dict, spec: spack.spec.Spec, stage_path: str
) -> spack.sandbox_namespaces.NamespaceFilesystemPolicy:
    """Classify trusted installer inputs without changing the worker filesystem."""
    read_only_paths = [str(dep.prefix) for dep in spec.traverse(root=False) if not dep.external]
    read_only_paths.append(os.path.join(spack.store.STORE.unpadded_root, "bin", "sbang"))
    read_only_paths.extend(
        os.path.join(upstream_db.root, "bin", "sbang")
        for upstream_db in spack.store.STORE.upstreams or []
    )
    read_only_paths.extend(config.get("allow_read", []))

    read_write_paths = [stage_path, str(spec.prefix), tempfile.gettempdir(), os.devnull]
    read_write_paths.extend(config.get("allow_write", []))

    def existing_identity_mounts(paths):
        resolved_paths = []
        for path in paths:
            resolved = os.path.realpath(os.path.abspath(path))
            if os.path.exists(resolved):
                resolved_paths.append(resolved)
        minimal_paths = []
        for path in sorted(set(resolved_paths)):
            if any(
                parent != path and os.path.commonpath((parent, path)) == parent
                for parent in minimal_paths
            ):
                continue
            minimal_paths.append(path)
        return ((path, path) for path in minimal_paths)

    return spack.sandbox_namespaces.build_namespace_filesystem_policy(
        (path for path in configured_empty_directory_paths(spec) if os.path.isdir(path)),
        existing_identity_mounts(read_only_paths),
        existing_identity_mounts(read_write_paths),
    )


def namespace_selected_filesystem_policy_from_inputs(
    config: dict,
    spec: spack.spec.Spec,
    stage_path: str,
    selected_paths: NamespacePolicyInputPaths,
    replacement_mounts: Iterable[Tuple[str, str]] = (),
    generated_symlinks: Iterable[spack.sandbox_namespaces.NamespaceGeneratedSymlink] = (),
    tmpfs_paths: Iterable[str] = (),
) -> spack.sandbox_namespaces.NamespaceFilesystemPolicy:
    """Build a trusted selected-tree policy without activating it.

    Host compiler, tool, header, runtime, and scoped temporary paths are
    explicit because a concrete compiler prefix such as ``/usr`` is too broad
    to restore below a hidden tree. Active package repositories and immutable
    Spack source subtrees are selected from trusted process state.
    """

    required_categories = (
        ("hidden root", selected_paths.hidden_roots),
        ("compiler", selected_paths.compiler_paths),
        ("tool", selected_paths.tool_paths),
        ("header", selected_paths.header_paths),
        ("runtime", selected_paths.runtime_paths),
        ("temporary", selected_paths.temporary_paths),
    )
    optional_categories = {"compiler", "header"}
    for category, paths in required_categories:
        if not paths and category not in optional_categories:
            raise spack.sandbox_namespaces.NamespaceSetupError(
                errno.EINVAL,
                "select namespace policy inputs",
                f"no {category} paths were selected",
            )

    repositories = tuple(spack.repo.PATH.repos)
    repository_roots = tuple(os.path.realpath(repo.root) for repo in repositories)
    if not repository_roots:
        raise spack.sandbox_namespaces.NamespaceSetupError(
            errno.EINVAL,
            "select namespace policy inputs",
            "no package repository roots were selected",
        )
    spack_source_paths = (
        spack.paths.bin_path,
        spack.paths.lib_path,
        spack.paths.share_path,
        spack.paths.etc_path,
    )

    read_only_paths = [str(dep.prefix) for dep in spec.traverse(root=False) if not dep.external]
    for _, paths in required_categories[1:-1]:
        read_only_paths.extend(paths)
    read_only_paths.extend(repository_roots)
    read_only_paths.extend(spack_source_paths)
    read_only_paths.extend(config.get("allow_read", []))

    sbang_paths = [os.path.join(spack.store.STORE.unpadded_root, "bin", "sbang")]
    sbang_paths.extend(
        os.path.join(upstream_db.root, "bin", "sbang")
        for upstream_db in spack.store.STORE.upstreams or []
    )
    read_only_paths.extend(sbang_paths)

    read_write_paths = [stage_path, str(spec.prefix), os.devnull]
    read_write_paths.extend(selected_paths.temporary_paths)
    read_write_paths.extend(config.get("allow_write", []))

    def canonical_required_paths(paths):
        result = []
        for path in paths:
            absolute = os.path.abspath(path)
            resolved = os.path.realpath(absolute)
            if not os.path.exists(resolved):
                raise spack.sandbox_namespaces.NamespaceSetupError(
                    errno.ENOENT,
                    "select namespace policy inputs",
                    f"required path does not exist: {path}",
                )
            if absolute != resolved:
                raise spack.sandbox_namespaces.NamespaceSetupError(
                    errno.EINVAL,
                    "select namespace policy inputs",
                    f"required path is not canonical: {path} resolves to {resolved}",
                )
            result.append(resolved)
        return tuple(sorted(set(result)))

    requested_hidden_roots = canonical_required_paths(selected_paths.hidden_roots)
    requested_read_only = canonical_required_paths(read_only_paths)
    requested_read_write = canonical_required_paths(read_write_paths)

    def minimal_paths(paths):
        result = []
        for path in paths:
            if any(
                parent == path or os.path.commonpath((parent, path)) == parent for parent in result
            ):
                continue
            result.append(path)
        return tuple(result)

    effective_read_write = minimal_paths(requested_read_write)
    effective_read_only = minimal_paths(
        path
        for path in requested_read_only
        if not any(
            path == writable or os.path.commonpath((path, writable)) == writable
            for writable in effective_read_write
        )
    )

    hidden_roots = minimal_paths(
        root for root in requested_hidden_roots if root not in effective_read_only
    )
    mounted_read_only = tuple(
        path
        for path in effective_read_only
        if any(os.path.commonpath((root, path)) == root for root in hidden_roots)
    )

    policy = spack.sandbox_namespaces.build_namespace_filesystem_policy(
        hidden_roots,
        ((path, path) for path in mounted_read_only),
        ((path, path) for path in effective_read_write),
        replacement_mounts=replacement_mounts,
        generated_symlinks=generated_symlinks,
        read_only_view=True,
        tmpfs_paths=tmpfs_paths,
    )

    def assert_covered(paths, mounts, access):
        targets = tuple(mount.target for mount in mounts)
        for path in paths:
            if not any(
                target == path or os.path.commonpath((target, path)) == target
                for target in targets
            ):
                raise spack.sandbox_namespaces.NamespaceSetupError(
                    errno.EINVAL,
                    "validate namespace policy coverage",
                    f"{access} path is not represented by the policy: {path}",
                )

    assert_covered(mounted_read_only, policy.read_only_mounts, "read-only")
    assert_covered(requested_read_write, policy.read_write_mounts, "read-write")
    return policy


def namespace_filesystem_policy_and_plan_from_inputs(
    config: dict,
    spec: spack.spec.Spec,
    stage_path: str,
    mount_plan_stage: str,
    selected_paths: NamespacePolicyInputPaths,
    replacement_mounts: Iterable[Tuple[str, str]] = (),
    generated_symlinks: Iterable[spack.sandbox_namespaces.NamespaceGeneratedSymlink] = (),
    tmpfs_paths: Iterable[str] = (),
) -> Tuple[
    spack.sandbox_namespaces.NamespaceFilesystemPolicy, spack.sandbox_namespaces.NamespaceMountPlan
]:
    """Compile and validate a trusted selected-tree policy without activating it."""
    policy = namespace_selected_filesystem_policy_from_inputs(
        config,
        spec,
        stage_path,
        selected_paths,
        replacement_mounts,
        generated_symlinks,
        tmpfs_paths,
    )
    plan = spack.sandbox_namespaces.build_namespace_mount_plan_from_policy(
        policy, mount_plan_stage
    )
    return policy, plan


def prepare_namespace_activation(
    config: dict,
    spec: spack.spec.Spec,
    stage_path: str,
    log_path: str,
    jobserver_paths: Iterable[str],
    worker_root: str,
    fetch_cache_path: str,
) -> Tuple[NamespaceActivation, spack.sandbox_namespaces.NamespaceMountPlanScratch]:
    """Select, compile, and lease one build's complete namespace policy."""
    fetch_cache_path = os.path.abspath(fetch_cache_path)
    if fetch_cache_path != os.path.realpath(fetch_cache_path):
        raise spack.sandbox_namespaces.NamespaceSetupError(
            errno.EINVAL,
            "prepare namespace fetch cache",
            f"fetch cache path is not canonical: {fetch_cache_path}",
        )
    os.makedirs(fetch_cache_path, mode=0o700, exist_ok=True)
    host_paths = select_namespace_host_device_worker_paths(
        config,
        spec,
        stage_path,
        log_path=log_path,
        jobserver_paths=jobserver_paths,
        worker_root=worker_root,
        fetch_cache_path=fetch_cache_path,
    )

    compiler_paths = []
    compiler_support_entries = []
    for entry in compiler_driver_paths(spec):
        compiler_paths.append(entry.source)
    for _language, compiler_path, _compiler_spec in _selected_compilers(spec):
        support_entries = compiler_support_paths(compiler_path)
        compiler_support_entries.extend(support_entries)
        compiler_paths.extend(entry.source for entry in support_entries)

    tool_entries = list(dict.fromkeys((*stage_tool_paths(), *install_tool_paths())))
    tool_paths = [entry.source for entry in tool_entries]
    tool_paths.extend(tool_runtime_paths(spec, tool_entries))

    runtime_paths = list(host_paths.host_runtime_paths)
    runtime_paths.extend(host_paths.read_only_paths)
    python_executable = os.path.abspath(sys.executable)
    python_source = os.path.realpath(python_executable)
    runtime_paths.append(python_source)
    runtime_paths.extend(
        os.path.realpath(path) for path in sys.path if os.path.isabs(path) and os.path.exists(path)
    )

    writable_paths = set(host_paths.writable_paths)
    writable_paths.update(host_paths.device_paths)

    selected_paths = NamespacePolicyInputPaths(
        host_paths.hidden_roots,
        tuple(sorted(set(path for path in compiler_paths if os.path.exists(path)))),
        tuple(sorted(set(path for path in tool_paths if os.path.exists(path)))),
        tuple(path for path in system_compiler_header_paths(spec) if os.path.exists(path)),
        tuple(sorted(set(path for path in runtime_paths if os.path.exists(path)))),
        tuple(sorted(writable_paths)),
    )
    replacement_mounts = tuple((worker_root, root) for root in host_paths.replacement_roots)
    device_policy = _load_sandbox_policy()
    tmpfs_paths = tuple(device_policy["tmpfs_paths"])
    generated_symlinks = tuple(
        dict.fromkeys(
            (
                *compiler_alias_symlink_paths(spec),
                *tool_alias_symlink_paths(
                    (*tool_entries, *compiler_support_entries), host_paths.hidden_roots
                ),
                *(
                    (
                        spack.sandbox_namespaces.NamespaceGeneratedSymlink(
                            python_executable, python_source
                        ),
                    )
                    if python_executable != python_source
                    and any(
                        os.path.commonpath((root, python_executable)) == root
                        for root in host_paths.hidden_roots
                    )
                    else ()
                ),
                *(
                    spack.sandbox_namespaces.NamespaceGeneratedSymlink(link, target)
                    for link, target in device_policy["device_symlinks"].items()
                ),
            )
        )
    )
    policy = namespace_selected_filesystem_policy_from_inputs(
        config,
        spec,
        stage_path,
        selected_paths,
        replacement_mounts,
        generated_symlinks,
        tmpfs_paths,
    )

    scratch = None
    last_error = None
    for base_path in (
        tempfile.gettempdir(),
        spack.paths.var_path,
        *device_policy["mount_plan_scratch_paths"],
    ):
        try:
            scratch = spack.sandbox_namespaces.allocate_namespace_mount_plan_scratch(
                policy,
                stage_path,
                excluded_paths=(worker_root, str(spec.prefix)),
                base_path=base_path,
            )
            break
        except OSError as error:
            last_error = error
    if scratch is None:
        assert last_error is not None
        raise last_error

    try:
        policy, _plan = namespace_filesystem_policy_and_plan_from_inputs(
            config,
            spec,
            stage_path,
            scratch.path,
            selected_paths,
            replacement_mounts,
            generated_symlinks,
            tmpfs_paths,
        )
    except BaseException:
        scratch.cleanup()
        raise
    return NamespaceActivation(policy, scratch.path, worker_root), scratch


def validate_namespace_policy_before_threads(
    config: dict,
    spec: spack.spec.Spec,
    stage_path: str,
    mount_plan_stage: str,
    selected_paths: NamespacePolicyInputPaths,
    replacement_mounts: Iterable[Tuple[str, str]] = (),
    generated_symlinks: Iterable[spack.sandbox_namespaces.NamespaceGeneratedSymlink] = (),
) -> Optional[
    Tuple[
        spack.sandbox_namespaces.NamespaceFilesystemPolicy,
        spack.sandbox_namespaces.NamespaceMountPlan,
    ]
]:
    """Validate the selected namespace policy before any worker mutation.

    Validation is unconditional whenever this helper is called. Callers can retain the returned
    immutable policy and mount plan for a later activation step.
    """
    return namespace_filesystem_policy_and_plan_from_inputs(
        config,
        spec,
        stage_path,
        mount_plan_stage,
        selected_paths,
        replacement_mounts,
        generated_symlinks,
    )


def _validate_namespace_worker_root(activation: NamespaceActivation) -> None:
    """Require an existing canonical worker root covered by a writable identity mount."""
    root = activation.worker_root
    (canonical_root,) = _canonical_required_paths((root,), "worker root")
    if root != canonical_root:
        raise spack.error.InstallError("Namespace worker root must be canonical and absolute")
    if (
        not os.path.isabs(root)
        or not os.path.isdir(root)
        or not any(
            mount.source == mount.target
            and os.path.commonpath((mount.target, root)) == mount.target
            for mount in activation.policy.read_write_mounts
        )
    ):
        raise spack.error.InstallError("Namespace worker root requires a writable identity mount")


def _configure_namespace_worker_environment(worker_root: str) -> None:
    """Create private worker state and publish it only in the confined child."""
    home = os.path.join(worker_root, "home")
    cache = os.path.join(worker_root, "cache")
    temporary = os.path.join(worker_root, "tmp")
    for path in (home, cache, temporary):
        os.mkdir(path, mode=0o700)
    java_options = " ".join(
        shlex.quote(option) for option in (f"-Duser.home={home}", f"-Djava.io.tmpdir={temporary}")
    )
    inherited_java_options = os.environ.get("JAVA_TOOL_OPTIONS", "")
    os.environ.update(
        HOME=home,
        XDG_CACHE_HOME=cache,
        TMPDIR=temporary,
        TMP=temporary,
        TEMP=temporary,
        JAVA_TOOL_OPTIONS=" ".join(
            option for option in (inherited_java_options, java_options) if option
        ),
    )
    tempfile.tempdir = temporary


def _require_staging_network(sandbox: Optional[spack.sandbox.Sandbox]) -> None:
    """Reject a namespace worker whose network was isolated before staging."""
    namespace_module = getattr(spack, "sandbox_namespaces", None)
    if (
        namespace_module is not None
        and isinstance(sandbox, namespace_module.NamespaceSandbox)
        and sandbox.network_namespace_active
    ):
        raise spack.error.InstallError(
            "Network namespace must remain inactive while staging sources"
        )


def _prepare_namespace_sandbox_before_threads(
    config: dict,
    spec: spack.spec.Spec,
    stage_path: str,
    *,
    mount_plan_stage: Optional[str] = None,
    selected_paths: Optional[NamespacePolicyInputPaths] = None,
    replacement_mounts: Iterable[Tuple[str, str]] = (),
    generated_symlinks: Iterable[spack.sandbox_namespaces.NamespaceGeneratedSymlink] = (),
    namespace_activation: Optional[NamespaceActivation] = None,
) -> Optional[spack.sandbox.Sandbox]:
    """Prepare the namespace view and drop mount authority before ``Tee``.

    The worker is still single-threaded here. Complete policy activation also
    configures worker-local state; mount authority is retained until sandbox
    activation after staging.
    """
    if not config.get("enable", False):
        return None

    if namespace_activation is not None:
        if mount_plan_stage is not None or selected_paths is not None:
            raise spack.error.InstallError("Namespace activation received duplicate policy inputs")
        mount_plan_stage = namespace_activation.mount_plan_stage
    if namespace_activation is None and (
        mount_plan_stage is not None or selected_paths is not None
    ):
        if mount_plan_stage is None or selected_paths is None:
            raise spack.error.InstallError(
                "Namespace policy validation requires selected paths and mount-plan scratch"
            )
        validate_namespace_policy_before_threads(
            config,
            spec,
            stage_path,
            mount_plan_stage,
            selected_paths,
            replacement_mounts,
            generated_symlinks,
        )

    spack.sandbox_namespaces.freeze_namespace_sandbox_capability()
    try:
        sandbox = spack.sandbox.get_sandbox()
    except spack.sandbox.SandboxError as error:
        raise spack.error.InstallError(f"Cannot enable build sandbox: {error}") from error

    if isinstance(sandbox, spack.sandbox_namespaces.NamespaceSandbox):
        if namespace_activation is not None:
            _validate_namespace_worker_root(namespace_activation)
            prepared = sandbox.prepare_filesystem_policy(
                namespace_activation.policy, namespace_activation.mount_plan_stage
            )
            if not prepared:
                raise spack.error.InstallError("Cannot apply selected namespace filesystem policy")
        else:
            prepared = sandbox.prepare_mount_tree(
                configured_empty_directory_paths(spec), stage_path
            )
            if not prepared:
                spack.util.tty.warn(
                    "Build sandbox could not mask host directories; kernel namespaces unavailable"
                )
        if prepared and namespace_activation is not None:
            _configure_namespace_worker_environment(namespace_activation.worker_root)
    return sandbox


def _start_tee_after_namespace(
    config: dict,
    tee_control_r: IpcChannel,
    tee_control_w: Optional[IpcChannel],
    parent: IpcChannel,
    log_path: str,
    spec: Optional[spack.spec.Spec] = None,
    stage_path: Optional[str] = None,
    namespace_activation: Optional[NamespaceActivation] = None,
):
    sandbox = None
    if config.get("enable", False):
        assert spec is not None and stage_path is not None
        if namespace_activation is None:
            sandbox = _prepare_namespace_sandbox_before_threads(config, spec, stage_path)
        else:
            sandbox = _prepare_namespace_sandbox_before_threads(
                config, spec, stage_path, namespace_activation=namespace_activation
            )
    return Tee(tee_control_r, tee_control_w, parent, log_path), sandbox


def _start_worker_output(
    config: dict,
    state: IpcChannel,
    tee_control_r: IpcChannel,
    tee_control_w: Optional[IpcChannel],
    parent: IpcChannel,
    log_path: str,
    spec: Optional[spack.spec.Spec] = None,
    stage_path: Optional[str] = None,
    namespace_activation: Optional[NamespaceActivation] = None,
):
    state_stream = make_state_stream(state)
    try:
        tee, sandbox = _start_tee_after_namespace(
            config,
            tee_control_r,
            tee_control_w,
            parent,
            log_path,
            spec,
            stage_path,
            namespace_activation,
        )
    except BaseException:
        error = traceback.format_exc()
        try:
            with open(log_path, "a", encoding="utf-8") as stream:
                stream.write(error)
        except OSError:
            print(error, file=sys.stderr)
        state_stream.close()
        sys.exit(ExitCode.BUILD_ERROR)
    return tee, state_stream, sandbox


def _enable_sandbox(
    config: dict,
    spec: spack.spec.Spec,
    stage_path: str,
    sandbox: Optional[spack.sandbox.Sandbox] = None,
) -> None:
    if not config.get("enable", False):
        return

    namespace_prepared = sandbox is not None
    if sandbox is None:
        try:
            sandbox = spack.sandbox.get_sandbox()
        except spack.sandbox.SandboxError as e:
            raise spack.error.InstallError(f"Cannot enable build sandbox: {e}") from e

    namespace_module = getattr(spack, "sandbox_namespaces", None)
    if (
        namespace_module is not None
        and isinstance(sandbox, namespace_module.NamespaceSandbox)
        and sandbox.filesystem_policy_active
    ):
        if not config.get("allow_network", False):
            try:
                sandbox.prepare_network_namespace()
            except spack.sandbox.SandboxError as e:
                raise spack.error.InstallError(f"Cannot enable build sandbox: {e}") from e
        if not sandbox.drop_mount_authority():
            raise spack.error.InstallError("Cannot drop namespace mount authority")
        return
    # Direct callers prepare the namespace view here. The install worker hands
    # in an already-prepared instance whose mount authority is dropped below.
    if (
        namespace_module is not None
        and isinstance(sandbox, namespace_module.NamespaceSandbox)
        and not namespace_prepared
    ):
        hidden_dirs = configured_empty_directory_paths(spec)
        if not sandbox.prepare_mount_tree(hidden_dirs, stage_path):
            spack.util.tty.warn(
                "Build sandbox could not mask host directories; kernel namespaces unavailable"
            )
        else:
            if not config.get("allow_network", False):
                sandbox.prepare_network_namespace()
            if not sandbox.drop_mount_authority():
                raise spack.error.InstallError("Cannot drop namespace mount authority")

    try:
        for dep in spec.traverse(root=False):
            if not dep.external:
                sandbox.allow_read(dep.prefix)

        sandbox.allow_write(stage_path)
        sandbox.allow_write(spec.prefix)

        # POSIX prescribes /tmp and /dev/null are present. In the future we can consider setting
        # TMPPATH to a sibling of the stage path to isolate concurrent builds better.
        sandbox.allow_write(tempfile.gettempdir())
        sandbox.allow_write(os.devnull)

        # Allow read access to sbang, which might be needed to run build scripts.
        sandbox.allow_read(os.path.join(spack.store.STORE.unpadded_root, "bin", "sbang"))
        for upstream_db in spack.store.STORE.upstreams or []:
            sandbox.allow_read(os.path.join(upstream_db.root, "bin", "sbang"))

        # User-configured paths
        for p in config.get("allow_read", []):
            sandbox.allow_read(p)
        for p in config.get("allow_write", []):
            sandbox.allow_write(p)

        sandbox.apply(block_network=not config.get("allow_network", False))
    except spack.sandbox.SandboxError as e:
        raise spack.error.InstallError(f"Cannot enable build sandbox: {e}") from e


def _rewire_no_db(
    spec: spack.spec.Spec, timer: spack.util.timer.BaseTimer = spack.util.timer.NULL_TIMER
) -> None:
    """Rewire a spliced spec from its build_spec prefix, without writing to the database."""
    tmpdir = tempfile.mkdtemp()
    try:
        with timer.measure("setup"):
            tarball = os.path.join(tmpdir, f"{spec.dag_hash()}.tar.gz")
            spack.binary_distribution.create_tarball(spec.build_spec, tarball)
        with timer.measure("pre-install"):
            spack.hooks.pre_install(spec)
        with timer.measure("extract"):
            spack.binary_distribution.extract_buildcache_tarball(tarball, destination=spec.prefix)
        with timer.measure("relocate"):
            spack.binary_distribution.relocate_package(spec)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def _install(
    request: BuildRequest,
    state_stream: io.TextIOWrapper,
    store: spack.store.Store,
    sandbox: Optional[spack.sandbox.Sandbox] = None,
) -> None:
    """Install a spec from build cache or source."""
    spec, explicit, install_policy = request.spec, request.explicit, request.install_policy

    # Create the stage and log file before starting the tee thread.
    pkg = spec.package
    if request.stage_parent is not None:
        for stage in pkg.stage:
            stage.path = os.path.join(request.stage_parent, stage.name)
    pkg.run_tests = request.run_tests

    # timer for install phases, dumped to install_times.json on success
    timer = spack.util.timer.Timer()

    if request.fake:
        store.layout.create_install_directory(spec)
        _do_fake_install(pkg)
        _post_install(pkg, spec, explicit, timer, cache=False)
        return

    # Try to install from buildcache, unless user asked for source only
    if install_policy != "source_only":
        if install_from_buildcache(request.mirrors, spec, request.unsigned, state_stream, timer):
            _post_install(pkg, spec, explicit, timer, cache=True)
            return
        elif install_policy == "cache_only":
            send_state("no binary available", state_stream)
            raise BinaryCacheMiss(f"No binary available for {spec}")

    # Spliced spec: rewire from build_spec prefix, or trigger build_spec installation.
    if spec.build_spec is not spec:
        if install_policy == "source_only":
            send_state("rewiring", state_stream)
            _rewire_no_db(spec, timer)
            _post_install(pkg, spec, explicit, timer, cache=False)
            return
        # Binary cache was the only option; signal miss for force_source expansion.
        send_state("no binary available", state_stream)
        raise BinaryCacheMiss(f"No binary available for {spec}")

    unmodified_env = os.environ.copy()
    env_mods = spack.build_environment.setup_package(pkg, dirty=request.dirty)
    store.layout.create_install_directory(spec)

    stage = pkg.stage
    # The supervisor removes successful stages after the child namespace is gone. Keeping the
    # stage here also leaves failed stages untouched for inspection.
    stage.keep = True

    # Then try a source build.
    with stage:
        if request.restage:
            stage.destroy()
        stage.create()

        # Write build environment and env-mods to stage
        spack.util.environment.dump_environment(pkg.env_path)
        with open(pkg.env_mods_path, "w", encoding="utf-8") as f:
            f.write(env_mods.shell_modifications(explicit=True, env=unmodified_env))

        # Try to snapshot configure/cmake args before phases run
        for attr in ("configure_args", "cmake_args"):
            try:
                args = getattr(pkg, attr)()
                with open(pkg.configure_args_path, "w", encoding="utf-8") as f:
                    f.write(" ".join(shlex.quote(a) for a in args))
                break
            except Exception:
                pass

        # For develop packages or non-develop packages with --keep-stage there may be a
        # pre-existing symlink at pkg.log_path which would cause the new symlink to fail.
        # Try removing it if it exists.
        try:
            os.unlink(pkg.log_path)
        except OSError:
            pass
        os.symlink(request.log_path, pkg.log_path)

        _require_staging_network(sandbox)
        send_state("staging", state_stream)

        with timer.measure("stage"):
            if not request.skip_patch:
                pkg.do_patch()
            else:
                pkg.do_stage()

        os.chdir(stage.source_path)

        if request.install_source and os.path.isdir(stage.source_path):
            src_target = os.path.join(spec.prefix, "share", spec.name, "src")
            fs.install_tree(stage.source_path, src_target)

        spack.hooks.pre_install(spec)

        builder = spack.builder.create(pkg)
        stop_before, stop_at = request.stop_before, request.stop_at
        if stop_before is not None and stop_before not in builder.phases:
            raise spack.error.InstallError(f"'{stop_before}' is not a valid phase for {pkg.name}")
        if stop_at is not None and stop_at not in builder.phases:
            raise spack.error.InstallError(f"'{stop_at}' is not a valid phase for {pkg.name}")

        _enable_sandbox(
            spack.config.CONFIG.get("config:sandbox", {}),
            spec,
            request.stage_parent or stage.path,
            sandbox=sandbox,
        )

        for phase in builder:
            if stop_before is not None and phase.name == stop_before:
                send_state(f"stopped before {stop_before}", state_stream)
                raise spack.error.StopPhase(f"Stopping before '{stop_before}'")
            send_state(phase.name, state_stream)
            spack.util.tty.msg(f"{pkg.name}: Executing phase: '{phase.name}'")
            # Run the install phase with debug output enabled.
            old_debug = spack.util.tty.debug_level()
            spack.util.tty.set_debug(1)
            try:
                with timer.measure(phase.name):
                    phase.execute()
            finally:
                spack.util.tty.set_debug(old_debug)
            if stop_at is not None and phase.name == stop_at:
                send_state(f"stopped after {stop_at}", state_stream)
                raise spack.error.StopPhase(f"Stopping at '{stop_at}'")

        _archive_build_metadata(pkg)
        _post_install(pkg, spec, explicit, timer, cache=False)


def _post_install(
    pkg: "spack.package_base.PackageBase",
    spec: spack.spec.Spec,
    explicit: bool,
    timer: spack.util.timer.Timer,
    cache: bool = False,
) -> None:
    # Do post install (and potentially post binary install) hooks
    with timer.measure("post-install"):
        if cache:
            if hasattr(pkg, "_post_buildcache_install_hook"):
                pkg._post_buildcache_install_hook()
        spack.hooks.post_install(spec, explicit)

    timer.stop()
    _write_timer_json(pkg, timer, cache)


def start_build(request: BuildRequest, jobserver: JobServerBase) -> ChildInfo:
    """Start a new build in a child process."""
    spec = request.spec
    channels = create_build_channels()

    # Obtain the MAKEFLAGS to be set in the child process, in a style the package's gmake accepts.
    gmake = next(iter(spec.dependencies("gmake")), None)
    makeflags = jobserver.makeflags(gmake)

    # As a performance optimization, we do not serialize the environment which
    # is slow to serialize and not needed in the build job
    proc = Process(
        target=worker_function,
        args=(
            request,
            channels.state_w,
            channels.output_w,
            channels.control_r,
            channels.tee_control_w,
            makeflags,
            GlobalStateMarshaler(serialize_env=False),
        ),
    )
    proc.start()

    # The parent process does not need the write ends of the main pipes or the read end of control.
    channels.close_child_ends()

    return ChildInfo(
        proc,
        spec,
        channels.output_r,
        channels.state_r,
        channels.control_w,
        ExitNotifier(proc),
        request.log_path,
    )


class BinaryCacheMiss(spack.error.SpackError):
    pass
