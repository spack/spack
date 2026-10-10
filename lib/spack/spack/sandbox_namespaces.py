# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Linux user and mount namespace sandbox backend.

Provides a capability probe for unprivileged namespaces, helpers to hide host
directories by mounting empty stage-owned directories over them, and a sandbox
backend class that combines the namespace with Landlock. The namespace backend
is the preferred Linux confinement backend when available; Landlock-only is the
fallback.
"""

import ctypes
import enum
import errno
import json
import os
import platform
import shutil
import tempfile
from pathlib import Path
from typing import Any, Callable, Iterable, List, NamedTuple, NoReturn, Optional

from spack.sandbox_base import Sandbox, SandboxError

# Linux namespace and mount flags.
CLONE_NEWUSER = 0x10000000
CLONE_NEWNS = 0x00020000
MS_BIND = 0x00001000
MS_PRIVATE = 0x00040000
MS_REC = 0x00004000
LINUX_CAPABILITY_VERSION_3 = 0x20080522


class NamespaceCapability(NamedTuple):
    """Result of probing unprivileged user and mount namespaces."""

    available: bool
    operation: Optional[str]
    reason: Optional[str]


class NamespaceSandboxBackend(enum.Enum):
    """Backend selected after the namespace capability probe."""

    NAMESPACE = "namespace"
    LANDLOCK = "landlock"
    UNCONSTRAINED = "unconstrained"


class NamespaceSandboxDecision(NamedTuple):
    """Namespace preference and its constrained fallback decision."""

    backend: NamespaceSandboxBackend
    capability: NamespaceCapability

    @property
    def is_fallback(self) -> bool:
        return self.backend is not NamespaceSandboxBackend.NAMESPACE

    @property
    def is_constrained(self) -> bool:
        return self.backend is not NamespaceSandboxBackend.UNCONSTRAINED


class NamespaceSetupError(OSError):
    """Failure of a specific namespace setup operation."""

    def __init__(self, error_number: int, operation: str, reason: str) -> None:
        super().__init__(error_number, f"{operation}: {reason}")
        self.operation = operation
        self.reason = reason


class _CapabilityHeader(ctypes.Structure):
    _fields_ = [("version", ctypes.c_uint32), ("pid", ctypes.c_int)]


class _CapabilityData(ctypes.Structure):
    _fields_ = [
        ("effective", ctypes.c_uint32),
        ("permitted", ctypes.c_uint32),
        ("inheritable", ctypes.c_uint32),
    ]


def _check_syscall(result: int, name: str) -> int:
    """Raise OSError if a libc syscall returned a negative value."""
    if result < 0:
        err = ctypes.get_errno()
        raise NamespaceSetupError(err, name, os.strerror(err))
    return result


# Process-local set of PIDs that have already entered the user/mount namespace.
# Makes _enter_user_mount_namespace idempotent within a single process.
_namespace_entered_pids: set = set()

# The installer probes before launching build workers. POSIX workers inherit
# this result, avoiding a second fork after their logging thread has started.
_namespace_probe_result: Optional[NamespaceCapability] = None


def _raise_namespace_setup_error(operation: str, error: OSError) -> NoReturn:
    reason = error.strerror or str(error)
    raise NamespaceSetupError(error.errno or errno.EIO, operation, reason) from error


def _enter_user_mount_namespace(libc, _probe_child: bool = False) -> None:
    """Enter a private user and mount namespace and contain mount propagation.

    Creates ``CLONE_NEWUSER | CLONE_NEWNS``, writes the invoking user's UID
    and GID mapping, disables setgroups, and makes the root mount private
    (``MS_REC | MS_PRIVATE``) so mounts do not propagate back to the host.

    Idempotent within a single process: subsequent calls from the same PID
    are no-ops. A forked child gets its own copy of the guard.
    """

    my_pid = os.getpid()
    if not _probe_child and my_pid in _namespace_entered_pids:
        return

    user_id = os.getuid()
    group_id = os.getgid()
    _check_syscall(
        libc.unshare(ctypes.c_int(CLONE_NEWUSER | CLONE_NEWNS)),
        "unshare(CLONE_NEWUSER | CLONE_NEWNS)",
    )
    try:
        with open("/proc/self/setgroups", "w", encoding="ascii") as stream:
            stream.write("deny")
    except OSError as error:
        if error.errno != errno.ENOENT:
            _raise_namespace_setup_error("write /proc/self/setgroups", error)
    try:
        with open("/proc/self/uid_map", "w", encoding="ascii") as stream:
            stream.write("{0} {0} 1".format(user_id))
    except OSError as error:
        _raise_namespace_setup_error("write /proc/self/uid_map", error)
    try:
        with open("/proc/self/gid_map", "w", encoding="ascii") as stream:
            stream.write("{0} {0} 1".format(group_id))
    except OSError as error:
        _raise_namespace_setup_error("write /proc/self/gid_map", error)
    _check_syscall(
        libc.mount(None, b"/", None, ctypes.c_ulong(MS_REC | MS_PRIVATE), None),
        "mount(MS_PRIVATE)",
    )
    _namespace_entered_pids.add(my_pid)


def _drop_namespace_capabilities(libc) -> None:
    """Drop all capabilities gained by entering the private user namespace.

    Namespace setup temporarily needs mount authority. Once trusted code has
    prepared the mount tree, no later recipe or build tool may create mounts in
    this namespace.
    """
    header = _CapabilityHeader(version=LINUX_CAPABILITY_VERSION_3, pid=0)
    capabilities = (_CapabilityData * 2)()
    _check_syscall(
        libc.capset(ctypes.byref(header), capabilities), "capset(drop namespace capabilities)"
    )


def _encode_capability(capability: NamespaceCapability) -> bytes:
    return json.dumps(capability._asdict(), sort_keys=True).encode("utf-8")


def _decode_capability(payload: bytes) -> NamespaceCapability:
    if not payload:
        return NamespaceCapability(False, "namespace setup", "probe child returned no result")
    try:
        result = json.loads(payload.decode("utf-8"))
        return NamespaceCapability(
            bool(result["available"]), result.get("operation"), result.get("reason")
        )
    except (KeyError, TypeError, ValueError, UnicodeError) as error:
        return NamespaceCapability(False, "decode probe result", str(error))


def _probe_namespace_capability(libc) -> NamespaceCapability:
    """Probe namespace setup in a disposable child process.

    Forks, runs ``_enter_user_mount_namespace`` in the child, and reports
    a structured result through a pipe. The parent is never affected.
    """

    fork_fn = getattr(os, "fork", None)
    if fork_fn is None:
        return NamespaceCapability(False, "fork", "os.fork is unavailable")
    probe_root = None
    try:
        probe_root = tempfile.mkdtemp(prefix="spack-namespace-probe-")
        bind_source = os.path.join(probe_root, "source")
        bind_target = os.path.join(probe_root, "target")
        os.mkdir(bind_source)
        os.mkdir(bind_target)
    except OSError as error:
        if probe_root is not None:
            shutil.rmtree(probe_root, ignore_errors=True)
        _raise_namespace_setup_error("prepare directory bind probe", error)
    try:
        read_fd, write_fd = os.pipe()
    except OSError as error:
        shutil.rmtree(probe_root, ignore_errors=True)
        _raise_namespace_setup_error("create namespace probe pipe", error)
    try:
        pid = fork_fn()
    except OSError as error:
        os.close(read_fd)
        os.close(write_fd)
        shutil.rmtree(probe_root, ignore_errors=True)
        _raise_namespace_setup_error("fork namespace probe", error)
    except BaseException:
        os.close(read_fd)
        os.close(write_fd)
        shutil.rmtree(probe_root, ignore_errors=True)
        raise
    if pid == 0:
        # Never unwind into the caller in the forked child, even when setup
        # raises an unexpected exception. EOF also reports probe failure.
        try:
            os.close(read_fd)
            try:
                _enter_user_mount_namespace(libc, _probe_child=True)
                _check_syscall(
                    libc.mount(
                        os.fsencode(bind_source),
                        os.fsencode(bind_target),
                        None,
                        ctypes.c_ulong(MS_BIND),
                        None,
                    ),
                    "mount(MS_BIND probe)",
                )
                _drop_namespace_capabilities(libc)
            except NamespaceSetupError as error:
                result = NamespaceCapability(False, error.operation, error.reason)
            except OSError as error:
                result = NamespaceCapability(False, "namespace setup", str(error))
            except BaseException as error:
                result = NamespaceCapability(
                    False, "namespace setup", f"{type(error).__name__}: {error}"
                )
            else:
                result = NamespaceCapability(True, None, None)
            os.write(write_fd, _encode_capability(result))
        finally:
            os._exit(0)

    os.close(write_fd)
    try:
        chunks = []
        try:
            while True:
                chunk = os.read(read_fd, 4096)
                if not chunk:
                    break
                chunks.append(chunk)
        except OSError as error:
            _raise_namespace_setup_error("read namespace probe result", error)
        return _decode_capability(b"".join(chunks))
    finally:
        os.close(read_fd)
        try:
            os.waitpid(pid, 0)
        finally:
            shutil.rmtree(probe_root, ignore_errors=True)


def namespace_sandbox_capability(libc: Optional[ctypes.CDLL] = None) -> NamespaceCapability:
    """Return structured availability for unprivileged user and mount namespaces.

    Completed default-libc probes are cached. Parent-side operational failures
    remain retryable until a worker explicitly freezes its pre-thread result.
    """
    global _namespace_probe_result

    if platform.system() != "Linux":
        return NamespaceCapability(False, "platform", "Linux is required")
    use_cache = libc is None
    if use_cache and _namespace_probe_result is not None:
        return _namespace_probe_result
    try:
        if libc is None:
            try:
                libc = ctypes.CDLL(None, use_errno=True)
            except OSError as error:
                _raise_namespace_setup_error("load libc", error)
        result = _probe_namespace_capability(libc)
    except NamespaceSetupError as error:
        return NamespaceCapability(False, error.operation, error.reason)
    except OSError as error:
        return NamespaceCapability(False, "run namespace probe", str(error))
    if use_cache:
        _namespace_probe_result = result
    return result


def namespace_sandbox_available(libc: Optional[ctypes.CDLL] = None) -> bool:
    """Return whether unprivileged user and mount namespaces can be used.

    Returns ``False`` off Linux or when the probe fails. Returns ``True`` when
    such a namespace can be created.
    """
    return namespace_sandbox_capability(libc).available


def namespace_sandbox_decision() -> NamespaceSandboxDecision:
    """Prefer namespaces and otherwise select the constrained Landlock fallback."""
    capability = namespace_sandbox_capability()
    backend = (
        NamespaceSandboxBackend.NAMESPACE
        if capability.available
        else NamespaceSandboxBackend.LANDLOCK
    )
    return NamespaceSandboxDecision(backend, capability)


def freeze_namespace_sandbox_capability() -> NamespaceCapability:
    """Freeze the worker-local capability result before any worker thread starts.

    This is side-effect-free: it must not enter a namespace or create a mount.
    Namespace entry remains adjacent to trusted mount preparation and Landlock
    application, after recipe-controlled setup has completed.
    """
    global _namespace_probe_result

    capability = namespace_sandbox_capability()
    if _namespace_probe_result is None:
        _namespace_probe_result = capability
    return capability


def prepare_empty_directory_masking(
    paths: Iterable[str], libc: Optional[ctypes.CDLL] = None, cache_unavailable: bool = False
) -> bool:
    """Enter a private user and mount namespace for directory masking.

    Returns ``True`` once the namespace is active, ``False`` when
    unprivileged namespaces are not permitted by the kernel.

    Even when *paths* is empty, success means the calling process has entered
    the namespace. Setup errors after the probe propagate to the caller. When
    *cache_unavailable* is true, freeze an unavailable result so later backend
    selection in the same worker cannot start another probe after threads exist.
    """
    global _namespace_probe_result

    if platform.system() != "Linux":
        return False
    if os.getpid() in _namespace_entered_pids:
        return True
    capability = namespace_sandbox_capability(libc)
    if cache_unavailable and libc is None:
        freeze_namespace_sandbox_capability()
    if not capability.available:
        return False
    if libc is None:
        libc = ctypes.CDLL(None, use_errno=True)
    _enter_user_mount_namespace(libc)
    return True


def hide_directories_as_empty(
    paths: Iterable[str],
    stage_path: str,
    namespace_ready: bool = False,
    libc: Optional[ctypes.CDLL] = None,
) -> bool:
    """Mask each existing host directory with an empty stage-owned directory.

    Each existing directory in *paths* is covered by a bind-mount of an empty
    directory created under ``stage_path/spack-empty-host-dirs/<index>``.
    Sandboxed tools see an empty directory (``ENOENT`` for missing entries)
    instead of the host tree.

    Returns ``True`` on success (including an empty path list), ``False`` when
    the namespace backend is unavailable. Mount failures raise ``OSError``;
    callers must not continue with a partially prepared mount tree.
    """

    path_list = list(paths)
    if not path_list:
        return True
    if not namespace_ready and not prepare_empty_directory_masking(path_list, libc):
        return False
    if libc is None:
        libc = ctypes.CDLL(None, use_errno=True)
    empty_root = os.path.join(stage_path, "spack-empty-host-dirs")
    os.makedirs(empty_root, exist_ok=True)
    for index, path in enumerate(path_list):
        if not os.path.isdir(path):
            continue
        empty_dir = os.path.join(empty_root, str(index))
        os.mkdir(empty_dir)
        _check_syscall(
            libc.mount(
                os.fsencode(empty_dir), os.fsencode(path), None, ctypes.c_ulong(MS_BIND), None
            ),
            "mount(MS_BIND)",
        )
    return True


class NamespaceSandbox(Sandbox):
    """Sandbox backend that combines Linux user/mount namespaces with Landlock.

    On Linux, when unprivileged user and mount namespaces are available, this
    backend is preferred over the Landlock-only backend because it can hide host
    filesystem content via empty mounts and bind mounts, rather than only
    denying access through Landlock rules.

    The class delegates ``allow_read`` / ``allow_write`` to an internal
    ``LandlockSandbox`` so that Landlock's deny rules operate on the
    namespace-restricted mount tree.
    """

    def __init__(
        self,
        libc: Optional[ctypes.CDLL] = None,
        landlock: Optional[Any] = None,
        landlock_factory: Optional[Callable[[Optional[ctypes.CDLL]], Any]] = None,
    ) -> None:
        self.libc = libc
        self._namespace_ready = False
        self._hidden_dirs: List[str] = []
        self._stage_path: Optional[str] = None
        self._granted_dirs: List[Path] = []
        self._mount_authority_dropped = False
        # Create the internal Landlock sandbox lazily unless selection already
        # preflighted and supplied it.
        self._landlock = landlock
        self._landlock_factory = landlock_factory

    @property
    def namespace_available(self) -> bool:
        """Return whether the kernel permits unprivileged user+mount namespaces."""
        return namespace_sandbox_available(self.libc)

    @property
    def namespace_ready(self) -> bool:
        """Return whether the private namespace and mount tree are active."""
        return self._namespace_ready

    def _ensure_landlock(self) -> Any:
        """Create the internal LandlockSandbox on first use."""
        if self._landlock is None:
            if self._landlock_factory is None:
                raise SandboxError("Landlock backend is not configured")
            try:
                self._landlock = self._landlock_factory(self.libc)
            except OSError as error:
                raise SandboxError(f"Landlock is unavailable: {error}") from error
        return self._landlock

    def prepare_mount_tree(self, hidden_dirs: Iterable[str], stage_path: str) -> bool:
        """Enter the private namespace and mask *hidden_dirs* as empty.

        Called before Landlock rules are built so that Landlock operates on the
        namespace-restricted mount tree. Returns ``True`` if the namespace was
        entered or was already active, ``False`` if not available.
        """
        hidden_list = list(hidden_dirs)
        if self._namespace_ready:
            return True
        self._hidden_dirs = hidden_list
        self._stage_path = stage_path
        if not prepare_empty_directory_masking(hidden_list, self.libc):
            return False
        self._namespace_ready = hide_directories_as_empty(
            hidden_list, stage_path, namespace_ready=True, libc=self.libc
        )
        return self._namespace_ready

    def drop_mount_authority(self) -> bool:
        """Irreversibly drop namespace capabilities after trusted mount setup.

        The caller must prepare all namespace mounts first. Returns ``False``
        if the namespace is inactive and otherwise drops capability state once.
        """
        if not self._namespace_ready:
            return False
        if self._mount_authority_dropped:
            return True
        libc = self.libc
        if libc is None:
            libc = ctypes.CDLL(None, use_errno=True)
        _drop_namespace_capabilities(libc)
        self._mount_authority_dropped = True
        return True

    def bind_mount(self, source: str, target: Optional[str] = None) -> bool:
        """Bind-mount *source* at *target* inside the namespace.

        *target* defaults to *source*. Returns ``True`` if the mount was
        performed, ``False`` if the namespace is not active.
        """
        if not self._namespace_ready:
            return False
        if self._mount_authority_dropped:
            raise SandboxError("Namespace mount authority was already dropped")
        if target is None:
            target = source
        resolved_source = os.path.realpath(source)
        if not os.path.exists(resolved_source):
            return False
        libc = self.libc
        if libc is None:
            libc = ctypes.CDLL(None, use_errno=True)
        _check_syscall(
            libc.mount(
                os.fsencode(resolved_source),
                os.fsencode(target),
                None,
                ctypes.c_ulong(MS_BIND | (MS_REC if os.path.isdir(resolved_source) else 0)),
                None,
            ),
            "mount(MS_BIND)",
        )
        self._granted_dirs.append(Path(resolved_source))
        return True

    def _allow_read(self, original: Path, resolved: Path) -> None:
        self._ensure_landlock()._allow_read(original, resolved)  # type: ignore[attr-defined]

    def _allow_write(self, original: Path, resolved: Path) -> None:
        self._ensure_landlock()._allow_write(original, resolved)  # type: ignore[attr-defined]

    def apply(self, block_network: bool = False) -> None:
        """Apply Landlock on top of the namespace-restricted mount tree.

        If no rules were granted, an empty deny-by-default Landlock ruleset is
        still applied so the namespace is not left unconstrained.
        """
        self._ensure_landlock().apply(block_network=block_network)

    def cleanup(self) -> None:
        """No-op for the namespace case.

        The namespace, its mount tree, and the Landlock ruleset all die with the
        process.
        """
