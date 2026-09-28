# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Linux user and mount namespace sandbox backend.

Provides a capability probe for unprivileged namespaces, helpers to hide host
directories with read-only empty tmpfs sources, and a namespace-native sandbox
backend. The completed namespace policy uses hidden trees and bind-mounted
allowlists by default; Landlock is used only by the separate fallback backend.
"""

import ctypes
import enum
import errno
import json
import os
import platform
import shutil
import stat
import tempfile
import threading
from pathlib import Path
from typing import Any, Callable, Iterable, List, NamedTuple, NoReturn, Optional, Tuple

from spack.sandbox_base import Sandbox, SandboxError

# Linux namespace and mount flags.
CLONE_NEWUSER = 0x10000000
CLONE_NEWNS = 0x00020000
MS_BIND = 0x00001000
MS_PRIVATE = 0x00040000
MS_REC = 0x00004000
MS_RDONLY = 0x00000001
MS_NOSUID = 0x00000002
MS_NODEV = 0x00000004
MS_NOEXEC = 0x00000008
MS_REMOUNT = 0x00000020
AT_FDCWD = -100
AT_RECURSIVE = 0x00008000
MOUNT_ATTR_RDONLY = 0x00000001
LINUX_CAPABILITY_VERSION_3 = 0x20080522

_EMPTY_SOURCE_FLAGS = MS_NOSUID | MS_NODEV | MS_NOEXEC


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


class NamespaceMount(NamedTuple):
    """One validated source-to-target mount in a namespace plan."""

    source: str
    target: str


class NamespaceMountAccess(enum.Enum):
    """Access exposed through a preserved namespace mount."""

    READ_ONLY = "read-only"
    READ_WRITE = "read-write"


class NamespaceMountRequest(NamedTuple):
    """One source-to-target mount requested by namespace policy."""

    source: str
    target: str
    access: NamespaceMountAccess


class NamespaceGeneratedPath(NamedTuple):
    """One file or directory created only in the namespace view."""

    path: str
    is_directory: bool


class NamespaceGeneratedSymlink(NamedTuple):
    """One symlink created only in the namespace view."""

    path: str
    target: str


class NamespaceFilesystemPolicy(NamedTuple):
    """Immutable filesystem intent validated before namespace mutation."""

    hidden_roots: Tuple[str, ...]
    read_only_mounts: Tuple[NamespaceMountRequest, ...] = ()
    read_write_mounts: Tuple[NamespaceMountRequest, ...] = ()
    generated_paths: Tuple[NamespaceGeneratedPath, ...] = ()
    replacement_mounts: Tuple[NamespaceMountRequest, ...] = ()
    generated_symlinks: Tuple[NamespaceGeneratedSymlink, ...] = ()
    read_only_view: bool = False


class NamespacePreservedMount(NamedTuple):
    """A preserved bind mount with the source type needed at application time."""

    source: str
    target: str
    source_is_directory: bool
    access: NamespaceMountAccess


class NamespaceMountPlan(NamedTuple):
    """Immutable mount plan validated before namespace mutation."""

    stage_path: str
    mounts: Tuple[NamespaceMount, ...]
    preserved_mounts: Tuple[NamespacePreservedMount, ...] = ()
    restoration_mounts: Tuple[NamespacePreservedMount, ...] = ()
    generated_paths: Tuple[NamespaceGeneratedPath, ...] = ()
    replacement_mounts: Tuple[NamespacePreservedMount, ...] = ()
    generated_symlinks: Tuple[NamespaceGeneratedSymlink, ...] = ()
    read_only_view: bool = False


_active_namespace_mount_plan_scratch = set()
_namespace_mount_plan_scratch_lock = threading.Lock()


class NamespaceMountPlanScratch:
    """Supervisor-owned durable scratch for one namespace mount plan."""

    def __init__(self, path: str) -> None:
        self.path = path
        self._owner_pid = os.getpid()
        identity = os.stat(path)
        self._identity = (identity.st_dev, identity.st_ino)
        self._worker_pid: Optional[int] = None

    @property
    def worker_pid(self) -> Optional[int]:
        return self._worker_pid

    def attach_worker(self, worker_pid: int) -> None:
        """Associate a launched worker so cleanup can reject live processes."""
        if os.getpid() != self._owner_pid:
            _mount_plan_error(
                "attach namespace mount-plan worker", "only the scratch owner may attach a worker"
            )
        if not isinstance(worker_pid, int) or worker_pid <= 0 or worker_pid == self._owner_pid:
            _mount_plan_error(
                "attach namespace mount-plan worker", f"invalid worker PID: {worker_pid!r}"
            )
        if self._worker_pid is not None and self._worker_pid != worker_pid:
            _mount_plan_error(
                "attach namespace mount-plan worker",
                f"worker already attached: {self._worker_pid}",
            )
        self._worker_pid = worker_pid

    def cleanup(self) -> None:
        """Remove scratch after setup failure or after the attached worker exits."""
        if os.getpid() != self._owner_pid:
            _mount_plan_error(
                "cleanup namespace mount-plan scratch", "only the scratch owner may clean up"
            )
        if self._worker_pid is not None and _namespace_process_is_alive(self._worker_pid):
            _mount_plan_error(
                "cleanup namespace mount-plan scratch",
                f"worker is still alive: {self._worker_pid}",
                errno.EBUSY,
            )
        try:
            current = os.lstat(self.path)
        except FileNotFoundError:
            with _namespace_mount_plan_scratch_lock:
                _active_namespace_mount_plan_scratch.discard(self.path)
            return
        if stat.S_ISLNK(current.st_mode) or not stat.S_ISDIR(current.st_mode):
            _mount_plan_error(
                "cleanup namespace mount-plan scratch",
                f"scratch path changed type: {self.path}",
                errno.EEXIST,
            )
        if (current.st_dev, current.st_ino) != self._identity:
            _mount_plan_error(
                "cleanup namespace mount-plan scratch",
                f"scratch path was replaced: {self.path}",
                errno.EEXIST,
            )
        shutil.rmtree(self.path)
        with _namespace_mount_plan_scratch_lock:
            _active_namespace_mount_plan_scratch.discard(self.path)


def _namespace_process_is_alive(process_id: int) -> bool:
    try:
        os.kill(process_id, 0)
    except OSError as error:
        if error.errno == errno.ESRCH:
            return False
        if error.errno == errno.EPERM:
            return True
        raise
    return True


class _CapabilityHeader(ctypes.Structure):
    _fields_ = [("version", ctypes.c_uint32), ("pid", ctypes.c_int)]


class _CapabilityData(ctypes.Structure):
    _fields_ = [
        ("effective", ctypes.c_uint32),
        ("permitted", ctypes.c_uint32),
        ("inheritable", ctypes.c_uint32),
    ]


class _MountAttr(ctypes.Structure):
    _fields_ = [
        ("attr_set", ctypes.c_uint64),
        ("attr_clr", ctypes.c_uint64),
        ("propagation", ctypes.c_uint64),
        ("userns_fd", ctypes.c_uint64),
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


def _mount_plan_error(operation: str, reason: str, error_number: int = errno.EINVAL) -> NoReturn:
    raise NamespaceSetupError(error_number, operation, reason)


def _set_mount_access(libc: ctypes.CDLL, target: str, recursive: bool, read_only: bool) -> None:
    """Set one mount's access without changing its source mount."""
    try:
        mount_setattr = libc.mount_setattr
    except AttributeError:
        _mount_plan_error(
            "mount_setattr(MOUNT_ATTR_RDONLY)", "libc does not expose mount_setattr", errno.ENOSYS
        )
    attributes = _MountAttr(
        attr_set=MOUNT_ATTR_RDONLY if read_only else 0,
        attr_clr=0 if read_only else MOUNT_ATTR_RDONLY,
    )
    _check_syscall(
        mount_setattr(
            ctypes.c_int(AT_FDCWD),
            os.fsencode(target),
            ctypes.c_uint(AT_RECURSIVE if recursive else 0),
            ctypes.byref(attributes),
            ctypes.sizeof(attributes),
        ),
        "mount_setattr(MOUNT_ATTR_RDONLY)",
    )


def _set_mount_read_only(libc: ctypes.CDLL, target: str, recursive: bool) -> None:
    """Make one bind mount or mount tree read-only without changing its source mount."""
    _set_mount_access(libc, target, recursive, True)


def _set_mount_writable(libc: ctypes.CDLL, target: str, recursive: bool) -> None:
    """Clear read-only access on one bind mount without changing its source mount."""
    _set_mount_access(libc, target, recursive, False)


def _path_contains(parent: str, child: str) -> bool:
    return parent != child and os.path.commonpath((parent, child)) == parent


def _validate_non_overlapping_paths(paths: Iterable[Tuple[str, str]], operation: str) -> None:
    sorted_paths = sorted(paths, key=lambda item: item[0])
    for index, (path, category) in enumerate(sorted_paths):
        for previous_path, previous_category in sorted_paths[:index]:
            if path == previous_path:
                _mount_plan_error(
                    operation,
                    f"duplicate or access-conflicting {category} and "
                    f"{previous_category} path: {path}",
                )
            if _path_contains(previous_path, path):
                _mount_plan_error(
                    operation,
                    f"overlapping {previous_category} and {category} paths: "
                    f"{previous_path} and {path}",
                )


def allocate_namespace_mount_plan_scratch(
    policy: NamespaceFilesystemPolicy,
    stage_path: str,
    excluded_paths: Iterable[str] = (),
    base_path: Optional[str] = None,
) -> NamespaceMountPlanScratch:
    """Allocate private mount endpoints outside the policy's writable roots.

    The caller owns the returned lease and must clean it up after any worker
    using it has been reaped. The directory is ordinary host-backed scratch;
    it is not the build stage and does not change stage or prefix lifecycle.
    """
    policy = _validated_namespace_filesystem_policy(policy)
    forbidden_paths = list(policy.hidden_roots)
    for mount in policy.read_only_mounts + policy.read_write_mounts:
        forbidden_paths.extend((mount.source, mount.target))
    for mount in policy.replacement_mounts:
        forbidden_paths.extend((mount.source, mount.target))
    forbidden_paths.append(stage_path)
    forbidden_paths.extend(excluded_paths)
    resolved_forbidden = tuple(
        sorted({os.path.realpath(os.path.abspath(path)) for path in forbidden_paths})
    )

    requested_base = tempfile.gettempdir() if base_path is None else base_path
    absolute_base = os.path.abspath(requested_base)
    resolved_base = os.path.realpath(absolute_base)
    if absolute_base != resolved_base:
        _mount_plan_error(
            "allocate namespace mount-plan scratch", f"scratch base is symlinked: {requested_base}"
        )
    if not os.path.isdir(resolved_base):
        _mount_plan_error(
            "allocate namespace mount-plan scratch",
            f"scratch base is not a directory: {requested_base}",
            errno.ENOTDIR,
        )
    if any(
        root == resolved_base or _path_contains(root, resolved_base) for root in resolved_forbidden
    ):
        _mount_plan_error(
            "allocate namespace mount-plan scratch",
            f"scratch base overlaps a policy root: {resolved_base}",
            errno.EEXIST,
        )

    scratch_path = os.path.abspath(
        tempfile.mkdtemp(prefix="spack-namespace-mount-", dir=resolved_base)
    )
    if scratch_path != os.path.realpath(scratch_path) or os.path.islink(scratch_path):
        _mount_plan_error(
            "allocate namespace mount-plan scratch",
            f"allocated scratch is symlinked: {scratch_path}",
            errno.EEXIST,
        )
    if any(
        root == scratch_path
        or _path_contains(root, scratch_path)
        or _path_contains(scratch_path, root)
        for root in resolved_forbidden
    ):
        _mount_plan_error(
            "allocate namespace mount-plan scratch",
            f"allocated scratch collides with a policy root: {scratch_path}",
            errno.EEXIST,
        )
    if not os.path.isdir(scratch_path):
        _mount_plan_error(
            "allocate namespace mount-plan scratch",
            f"allocated scratch is not a real directory: {scratch_path}",
            errno.ENOTDIR,
        )
    with _namespace_mount_plan_scratch_lock:
        if scratch_path in _active_namespace_mount_plan_scratch:
            _mount_plan_error(
                "allocate namespace mount-plan scratch",
                f"scratch allocation collision: {scratch_path}",
                errno.EEXIST,
            )
        _active_namespace_mount_plan_scratch.add(scratch_path)
    os.chmod(scratch_path, 0o700)
    return NamespaceMountPlanScratch(scratch_path)


def build_namespace_filesystem_policy(
    hidden_roots: Iterable[str],
    read_only_mounts: Iterable[Tuple[str, str]] = (),
    read_write_mounts: Iterable[Tuple[str, str]] = (),
    generated_paths: Iterable[NamespaceGeneratedPath] = (),
    replacement_mounts: Iterable[Tuple[str, str]] = (),
    generated_symlinks: Iterable[NamespaceGeneratedSymlink] = (),
    read_only_view: bool = False,
) -> NamespaceFilesystemPolicy:
    """Canonicalize and validate namespace filesystem intent.

    Entries in different access categories may not duplicate or overlap. This
    function performs no filesystem mutation. Policy-to-plan compilation
    separately checks whether the current mount implementation can express all
    classified paths below the selected hidden roots.
    """
    resolved_hidden_roots = []
    for root in hidden_roots:
        if not os.path.exists(root):
            _mount_plan_error(
                "validate namespace policy hidden root",
                f"hidden root does not exist: {root}",
                errno.ENOENT,
            )
        if not os.path.isdir(root):
            _mount_plan_error(
                "validate namespace policy hidden root",
                f"hidden root is not a directory: {root}",
                errno.ENOTDIR,
            )
        resolved_hidden_roots.append(os.path.realpath(os.path.abspath(root)))
    _validate_non_overlapping_paths(
        ((path, "hidden root") for path in resolved_hidden_roots),
        "validate namespace policy hidden roots",
    )
    sorted_hidden_roots = tuple(sorted(resolved_hidden_roots))

    def canonicalize_mounts(
        requests: Iterable[Tuple[str, str]], access: NamespaceMountAccess
    ) -> Tuple[NamespaceMountRequest, ...]:
        mounts = []
        for source, target in requests:
            resolved_source = os.path.realpath(os.path.abspath(source))
            if not os.path.exists(resolved_source):
                _mount_plan_error(
                    "validate namespace policy mount source",
                    f"mount source does not exist: {source}",
                    errno.ENOENT,
                )
            resolved_target = os.path.realpath(os.path.abspath(target))
            mounts.append(NamespaceMountRequest(resolved_source, resolved_target, access))
        return tuple(sorted(mounts, key=lambda item: (item.target, item.source)))

    canonical_read_only = canonicalize_mounts(read_only_mounts, NamespaceMountAccess.READ_ONLY)
    canonical_read_write = canonicalize_mounts(read_write_mounts, NamespaceMountAccess.READ_WRITE)
    canonical_generated_list = []
    for path in generated_paths:
        if not isinstance(path, NamespaceGeneratedPath) or not isinstance(path.is_directory, bool):
            _mount_plan_error(
                "validate namespace policy generated path", f"invalid generated path: {path!r}"
            )
        canonical_generated_list.append(
            NamespaceGeneratedPath(os.path.abspath(path.path), path.is_directory)
        )
    canonical_generated = tuple(sorted(canonical_generated_list, key=lambda item: item.path))

    canonical_replacement_list = []
    for source, target in replacement_mounts:
        resolved_source = os.path.realpath(os.path.abspath(source))
        resolved_target = os.path.realpath(os.path.abspath(target))
        if not os.path.exists(resolved_source):
            _mount_plan_error(
                "validate namespace policy replacement source",
                f"replacement source does not exist: {source}",
                errno.ENOENT,
            )
        if not os.path.isdir(resolved_source):
            _mount_plan_error(
                "validate namespace policy replacement source",
                f"replacement source is not a directory: {source}",
                errno.ENOTDIR,
            )
        if resolved_target not in sorted_hidden_roots:
            _mount_plan_error(
                "validate namespace policy replacement target",
                f"replacement target is not a hidden root: {target}",
            )
        canonical_replacement_list.append(
            NamespaceMountRequest(
                resolved_source, resolved_target, NamespaceMountAccess.READ_WRITE
            )
        )
    canonical_replacement = tuple(
        sorted(canonical_replacement_list, key=lambda item: (item.target, item.source))
    )

    canonical_symlink_list = []
    for symlink in generated_symlinks:
        if not isinstance(symlink, NamespaceGeneratedSymlink) or not os.path.isabs(symlink.target):
            _mount_plan_error(
                "validate namespace policy generated symlink",
                f"invalid generated symlink: {symlink!r}",
            )
        canonical_symlink_list.append(
            NamespaceGeneratedSymlink(
                os.path.abspath(symlink.path), os.path.realpath(os.path.abspath(symlink.target))
            )
        )
    canonical_symlinks = tuple(sorted(canonical_symlink_list, key=lambda item: item.path))

    classified_paths = [
        (mount.target, mount.access.value) for mount in canonical_read_only + canonical_read_write
    ]
    classified_paths.extend((path.path, "generated") for path in canonical_generated)
    classified_paths.extend((path.path, "generated symlink") for path in canonical_symlinks)
    sorted_classified_paths = sorted(classified_paths, key=lambda item: item[0])
    for index, (path, category) in enumerate(sorted_classified_paths):
        for previous_path, previous_category in sorted_classified_paths[:index]:
            if path == previous_path:
                _mount_plan_error(
                    "validate namespace policy classified paths",
                    f"duplicate or access-conflicting {category} and "
                    f"{previous_category} path: {path}",
                )
            if _path_contains(previous_path, path) and not (
                read_only_view
                and previous_category == NamespaceMountAccess.READ_ONLY.value
                and category == NamespaceMountAccess.READ_WRITE.value
            ):
                _mount_plan_error(
                    "validate namespace policy classified paths",
                    f"overlapping {previous_category} and {category} paths: "
                    f"{previous_path} and {path}",
                )
    _validate_non_overlapping_paths(
        ((mount.target, "replacement") for mount in canonical_replacement),
        "validate namespace policy replacement mounts",
    )
    for path, category in classified_paths:
        for root in sorted_hidden_roots:
            if path == root:
                _mount_plan_error(
                    "validate namespace policy categories",
                    f"duplicate hidden root and {category} path: {path}",
                )
            if _path_contains(path, root):
                _mount_plan_error(
                    "validate namespace policy categories",
                    f"overlapping {category} path and hidden root: {path} and {root}",
                )
        if category == "generated" and not any(
            _path_contains(root, path) for root in sorted_hidden_roots
        ):
            _mount_plan_error(
                "validate namespace policy generated path",
                f"generated path is not below a hidden root: {path}",
            )
        if category == "generated symlink" and not any(
            _path_contains(root, path) for root in sorted_hidden_roots
        ):
            _mount_plan_error(
                "validate namespace policy generated symlink",
                f"generated symlink is not below a hidden root: {path}",
            )

    return NamespaceFilesystemPolicy(
        sorted_hidden_roots,
        canonical_read_only,
        canonical_read_write,
        canonical_generated,
        canonical_replacement,
        canonical_symlinks,
        read_only_view,
    )


def _validated_namespace_filesystem_policy(
    policy: NamespaceFilesystemPolicy,
) -> NamespaceFilesystemPolicy:
    if not isinstance(policy, NamespaceFilesystemPolicy):
        _mount_plan_error("validate namespace policy", f"invalid policy: {policy!r}")
    if not isinstance(policy.read_only_view, bool):
        _mount_plan_error(
            "validate namespace policy read-only view",
            f"invalid read-only view: {policy.read_only_view!r}",
        )
    read_only_mounts = []
    read_write_mounts = []
    for mount in policy.read_only_mounts:
        if not isinstance(mount, NamespaceMountRequest) or (
            mount.access is not NamespaceMountAccess.READ_ONLY
        ):
            _mount_plan_error(
                "validate namespace policy access", f"invalid read-only mount: {mount!r}"
            )
        read_only_mounts.append((mount.source, mount.target))
    for mount in policy.read_write_mounts:
        if not isinstance(mount, NamespaceMountRequest) or (
            mount.access is not NamespaceMountAccess.READ_WRITE
        ):
            _mount_plan_error(
                "validate namespace policy access", f"invalid read-write mount: {mount!r}"
            )
        read_write_mounts.append((mount.source, mount.target))
    replacement_mounts = []
    for mount in policy.replacement_mounts:
        if not isinstance(mount, NamespaceMountRequest) or (
            mount.access is not NamespaceMountAccess.READ_WRITE
        ):
            _mount_plan_error(
                "validate namespace policy access", f"invalid replacement mount: {mount!r}"
            )
        replacement_mounts.append((mount.source, mount.target))
    validated = build_namespace_filesystem_policy(
        policy.hidden_roots,
        read_only_mounts,
        read_write_mounts,
        policy.generated_paths,
        replacement_mounts,
        policy.generated_symlinks,
        policy.read_only_view,
    )
    if policy != validated:
        _mount_plan_error("validate namespace policy", "policy is not canonical")
    return validated


def build_namespace_mount_plan_from_policy(
    policy: NamespaceFilesystemPolicy, stage_path: str
) -> NamespaceMountPlan:
    """Compile validated filesystem policy into deterministic mount operations."""
    policy = _validated_namespace_filesystem_policy(policy)
    resolved_stage = os.path.realpath(os.path.abspath(stage_path))
    reserved_stage_paths = (
        os.path.join(resolved_stage, "spack-empty-host-dirs"),
        os.path.join(resolved_stage, "spack-preserved-host-paths"),
    )
    for root in policy.hidden_roots:
        if resolved_stage == root or _path_contains(root, resolved_stage):
            _mount_plan_error(
                "compile namespace policy",
                f"mount-plan stage must be outside hidden roots: {resolved_stage}",
            )
        if any(root == path or _path_contains(path, root) for path in reserved_stage_paths):
            _mount_plan_error(
                "compile namespace policy", f"hidden root overlaps mount-plan scratch: {root}"
            )
    hidden_read_only_paths = [mount.target for mount in policy.read_only_mounts]
    hidden_generated_paths = [path.path for path in policy.generated_paths]
    hidden_generated_paths.extend(path.path for path in policy.generated_symlinks)
    for path in hidden_read_only_paths + hidden_generated_paths:
        if not any(_path_contains(root, path) for root in policy.hidden_roots):
            _mount_plan_error(
                "compile namespace policy", f"classified path is not below a hidden root: {path}"
            )
    if not policy.read_only_view:
        for mount in policy.read_write_mounts:
            if not any(_path_contains(root, mount.target) for root in policy.hidden_roots):
                _mount_plan_error(
                    "compile namespace policy",
                    f"classified path is not below a hidden root: {mount.target}",
                )
    mounts = policy.read_only_mounts + policy.read_write_mounts
    plan = _build_namespace_mount_plan(
        policy.hidden_roots,
        stage_path,
        mounts,
        policy.replacement_mounts,
        policy.generated_paths,
        policy.generated_symlinks,
    )
    return NamespaceMountPlan(
        plan.stage_path,
        plan.mounts,
        plan.preserved_mounts,
        plan.restoration_mounts,
        policy.generated_paths,
        plan.replacement_mounts,
        policy.generated_symlinks,
        policy.read_only_view,
    )


def build_namespace_mount_plan(
    paths: Iterable[str], stage_path: str, preserved_sources: Iterable[NamespaceMountRequest] = ()
) -> NamespaceMountPlan:
    """Validate and deterministically plan namespace bind mounts.

    Missing targets retain the narrow masking helper's no-op behavior. Existing
    targets must be directories. Canonical targets are sorted before assigning
    stage-owned sources. Preserved requests explicitly declare read-only or
    read-write access. Sources are mounted to stage-owned locations before masks
    and restored into their canonical targets afterward. Duplicate or
    conflicting relationships are rejected before entering a namespace or
    creating a source directory.
    """
    resolved_paths = []
    for path in paths:
        if not os.path.exists(path):
            continue
        if not os.path.isdir(path):
            _mount_plan_error(
                "validate mount plan target",
                f"mount target is not a directory: {path}",
                errno.ENOTDIR,
            )
        resolved_paths.append(os.path.realpath(os.path.abspath(path)))
    sorted_paths = sorted(resolved_paths)
    for index, path in enumerate(sorted_paths):
        for previous_path in sorted_paths[:index]:
            if path == previous_path:
                _mount_plan_error("validate mount plan targets", f"duplicate mount target: {path}")
            if _path_contains(previous_path, path):
                _mount_plan_error(
                    "validate mount plan targets",
                    f"conflicting mount targets: {previous_path} and {path}",
                )

    read_only_mounts = []
    read_write_mounts = []
    for request in preserved_sources:
        if request.access is NamespaceMountAccess.READ_ONLY:
            read_only_mounts.append((request.source, request.target))
        elif request.access is NamespaceMountAccess.READ_WRITE:
            read_write_mounts.append((request.source, request.target))
        else:
            _mount_plan_error(
                "validate preserved access", f"invalid preserved mount access: {request.access!r}"
            )
        if not os.path.exists(request.source):
            _mount_plan_error(
                "validate preserved source",
                f"preserved source does not exist: {request.source}",
                errno.ENOENT,
            )
        resolved_target = os.path.realpath(os.path.abspath(request.target))
        if not any(_path_contains(root, resolved_target) for root in sorted_paths):
            _mount_plan_error(
                "validate preserved relationship",
                f"preserved target is not below a hidden directory: {request.target}",
            )
    policy = build_namespace_filesystem_policy(sorted_paths, read_only_mounts, read_write_mounts)
    return build_namespace_mount_plan_from_policy(policy, stage_path)


def _build_namespace_mount_plan(
    paths: Iterable[str],
    stage_path: str,
    preserved_sources: Iterable[NamespaceMountRequest],
    replacement_mounts: Iterable[NamespaceMountRequest] = (),
    generated_paths: Iterable[NamespaceGeneratedPath] = (),
    generated_symlinks: Iterable[NamespaceGeneratedSymlink] = (),
) -> NamespaceMountPlan:
    """Build concrete operations from canonical validated policy entries."""
    resolved_stage = os.path.realpath(os.path.abspath(stage_path))
    if os.path.exists(resolved_stage) and not os.path.isdir(resolved_stage):
        _mount_plan_error(
            "validate mount plan stage",
            f"stage path is not a directory: {stage_path}",
            errno.ENOTDIR,
        )

    targets = []
    for path in paths:
        targets.append(path)

    sorted_targets = sorted(targets)
    for index, target in enumerate(sorted_targets):
        for previous_target in sorted_targets[:index]:
            if target == previous_target:
                _mount_plan_error(
                    "validate mount plan targets", f"duplicate mount target: {target}"
                )
            if _path_contains(previous_target, target):
                _mount_plan_error(
                    "validate mount plan targets",
                    f"conflicting mount targets: {previous_target} and {target}",
                )

    preserved_requests = []
    for source, target, access in preserved_sources:
        resolved_source = source
        source_is_directory = os.path.isdir(resolved_source)
        resolved_target = target
        if os.path.exists(resolved_target):
            if os.path.isdir(resolved_target) != source_is_directory:
                _mount_plan_error(
                    "validate preserved target",
                    f"preserved source and target types differ: {source} -> {target}",
                    errno.ENOTDIR,
                )
        elif not os.path.isdir(os.path.dirname(resolved_target)):
            _mount_plan_error(
                "validate preserved target",
                f"preserved target parent does not exist: {target}",
                errno.ENOENT,
            )
        preserved_requests.append((resolved_source, resolved_target, source_is_directory, access))

    preserved_requests.sort(key=lambda item: (item[1], item[0]))
    for index, (_, target, _, _) in enumerate(preserved_requests):
        if index and target == preserved_requests[index - 1][1]:
            _mount_plan_error(
                "validate preserved targets", f"duplicate preserved target: {target}"
            )

    empty_root = os.path.join(resolved_stage, "spack-empty-host-dirs")
    mounts = tuple(
        NamespaceMount(os.path.join(empty_root, str(index)), target)
        for index, target in enumerate(sorted_targets)
    )
    preserved_root = os.path.join(resolved_stage, "spack-preserved-host-paths")
    preserved_mounts = tuple(
        NamespacePreservedMount(
            source, os.path.join(preserved_root, str(index)), source_is_directory, access
        )
        for index, (source, _, source_is_directory, access) in enumerate(preserved_requests)
    )
    restoration_mounts = tuple(
        NamespacePreservedMount(
            preserved_mount.target,
            target,
            preserved_mount.source_is_directory,
            preserved_mount.access,
        )
        for preserved_mount, (_, target, _, _) in sorted(
            zip(preserved_mounts, preserved_requests),
            key=lambda item: (item[1][1].count(os.sep), item[1][1]),
        )
    )
    replacement_requests = []
    for request in replacement_mounts:
        if request.access is not NamespaceMountAccess.READ_WRITE:
            _mount_plan_error(
                "validate replacement access", f"invalid replacement access: {request!r}"
            )
        if not os.path.isdir(request.source):
            _mount_plan_error(
                "validate replacement source",
                f"replacement source is not a directory: {request.source}",
                errno.ENOTDIR,
            )
        if request.target not in sorted_targets:
            _mount_plan_error(
                "validate replacement target",
                f"replacement target is not a hidden directory: {request.target}",
            )
        replacement_requests.append(
            NamespacePreservedMount(request.source, request.target, True, request.access)
        )
    replacement_requests.sort(key=lambda item: (item.target, item.source))
    return NamespaceMountPlan(
        resolved_stage,
        mounts,
        preserved_mounts,
        restoration_mounts,
        tuple(generated_paths),
        tuple(replacement_requests),
        tuple(generated_symlinks),
    )


def _apply_namespace_mount_plan(plan: NamespaceMountPlan, libc: ctypes.CDLL) -> bool:
    """Create and apply a previously validated namespace mount plan."""
    if (
        not plan.mounts
        and not plan.preserved_mounts
        and not plan.replacement_mounts
        and not plan.read_only_view
    ):
        return True

    os.makedirs(plan.stage_path, exist_ok=True)

    for preserved in plan.preserved_mounts + plan.replacement_mounts:
        if not os.path.exists(preserved.source):
            _mount_plan_error(
                "apply mount plan source",
                f"mount source disappeared: {preserved.source}",
                errno.ENOENT,
            )
        if os.path.isdir(preserved.source) != preserved.source_is_directory:
            _mount_plan_error(
                "apply mount plan source",
                f"mount source type changed: {preserved.source}",
                errno.ENOTDIR,
            )
    for preserved in plan.preserved_mounts:
        if preserved.source_is_directory:
            os.makedirs(preserved.target, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(preserved.target), exist_ok=True)
            Path(preserved.target).touch()

    def apply_mount(
        source: str,
        target: str,
        source_is_directory: bool,
        recursive: bool,
        access: NamespaceMountAccess = NamespaceMountAccess.READ_WRITE,
    ) -> None:
        if not os.path.exists(source):
            _mount_plan_error(
                "apply mount plan source", f"mount source disappeared: {source}", errno.ENOENT
            )
        if os.path.isdir(source) != source_is_directory:
            _mount_plan_error(
                "apply mount plan source", f"mount source type changed: {source}", errno.ENOTDIR
            )
        if not os.path.exists(target):
            if source_is_directory:
                os.makedirs(target)
            else:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                Path(target).touch()
        if os.path.isdir(target) != source_is_directory:
            _mount_plan_error(
                "apply mount plan target", f"mount endpoint type changed: {target}", errno.ENOTDIR
            )
        _check_syscall(
            libc.mount(
                os.fsencode(source),
                os.fsencode(target),
                None,
                ctypes.c_ulong(MS_BIND | (MS_REC if recursive else 0)),
                None,
            ),
            "mount(MS_BIND)",
        )
        if access is NamespaceMountAccess.READ_ONLY:
            _set_mount_read_only(libc, target, recursive)
        elif plan.read_only_view:
            _set_mount_writable(libc, target, recursive)

    if not plan.read_only_view:
        for preserved_mount in plan.preserved_mounts:
            apply_mount(
                preserved_mount.source,
                preserved_mount.target,
                preserved_mount.source_is_directory,
                preserved_mount.source_is_directory,
                preserved_mount.access,
            )

    if plan.mounts:
        empty_root = os.path.join(plan.stage_path, "spack-empty-host-dirs")
        os.makedirs(empty_root, exist_ok=True)
        _check_syscall(
            libc.mount(
                b"tmpfs",
                os.fsencode(empty_root),
                b"tmpfs",
                ctypes.c_ulong(_EMPTY_SOURCE_FLAGS),
                None,
            ),
            "mount(tmpfs mask source)",
        )
        for mount in plan.mounts:
            os.makedirs(mount.source)
        for restoration in plan.restoration_mounts:
            mask = next(
                (
                    mount
                    for mount in plan.mounts
                    if os.path.commonpath((mount.target, restoration.target)) == mount.target
                ),
                None,
            )
            if mask is None:
                continue
            endpoint = os.path.join(mask.source, os.path.relpath(restoration.target, mask.target))
            if restoration.source_is_directory:
                os.makedirs(endpoint, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(endpoint), exist_ok=True)
                Path(endpoint).touch()
        for generated in plan.generated_paths:
            mask = next(
                mount for mount in plan.mounts if _path_contains(mount.target, generated.path)
            )
            endpoint = os.path.join(mask.source, os.path.relpath(generated.path, mask.target))
            if generated.is_directory:
                os.makedirs(endpoint, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(endpoint), exist_ok=True)
                Path(endpoint).touch()
        for generated in plan.generated_symlinks:
            mask = next(
                mount for mount in plan.mounts if _path_contains(mount.target, generated.path)
            )
            endpoint = os.path.join(mask.source, os.path.relpath(generated.path, mask.target))
            os.makedirs(os.path.dirname(endpoint), exist_ok=True)
            os.symlink(generated.target, endpoint)
        _check_syscall(
            libc.mount(
                None,
                os.fsencode(empty_root),
                None,
                ctypes.c_ulong(MS_REMOUNT | MS_RDONLY | _EMPTY_SOURCE_FLAGS),
                None,
            ),
            "mount(MS_REMOUNT, MS_RDONLY mask source)",
        )

    if plan.read_only_view:
        _set_mount_read_only(libc, "/", True)

    if plan.read_only_view:
        for preserved_mount in plan.preserved_mounts:
            apply_mount(
                preserved_mount.source,
                preserved_mount.target,
                preserved_mount.source_is_directory,
                preserved_mount.source_is_directory,
                preserved_mount.access,
            )
    for mount in plan.mounts:
        apply_mount(
            mount.source,
            mount.target,
            True,
            False,
            NamespaceMountAccess.READ_ONLY
            if plan.read_only_view
            else NamespaceMountAccess.READ_WRITE,
        )
    for replacement in plan.replacement_mounts:
        apply_mount(
            replacement.source,
            replacement.target,
            replacement.source_is_directory,
            True,
            replacement.access,
        )
    for restoration_mount in plan.restoration_mounts:
        apply_mount(
            restoration_mount.source,
            restoration_mount.target,
            restoration_mount.source_is_directory,
            restoration_mount.source_is_directory,
            restoration_mount.access,
        )
    return True


def _enter_user_mount_namespace(libc, _probe_child: bool = False) -> None:
    """Enter a private user and mount namespace and contain mount propagation.

    Creates ``CLONE_NEWUSER | CLONE_NEWNS``, writes the invoking user's UID
    and GID mapping, disables setgroups, and makes the root mount private
    (``MS_REC | MS_PRIVATE``) so mounts do not propagate back to the host.

    Idempotent within a single process: subsequent calls from the same PID are
    no-ops. A forked child gets its own copy of the guard.
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
                        b"tmpfs",
                        os.fsencode(bind_source),
                        b"tmpfs",
                        ctypes.c_ulong(_EMPTY_SOURCE_FLAGS),
                        None,
                    ),
                    "mount(tmpfs probe)",
                )
                _check_syscall(
                    libc.mount(
                        None,
                        os.fsencode(bind_source),
                        None,
                        ctypes.c_ulong(MS_REMOUNT | MS_RDONLY | _EMPTY_SOURCE_FLAGS),
                        None,
                    ),
                    "mount(MS_REMOUNT, MS_RDONLY probe)",
                )
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
                _set_mount_read_only(libc, "/", True)
                _set_mount_read_only(libc, bind_target, True)
                _set_mount_writable(libc, bind_target, False)
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
    preserved_sources: Iterable[NamespaceMountRequest] = (),
) -> bool:
    """Mask each existing host directory with a read-only empty tmpfs directory.

    A tmpfs mounted at ``stage_path/spack-empty-host-dirs`` is populated only
    with planned mount points and then remounted read-only. Each existing
    directory in *paths* is covered by a bind mount of one of those empty
    directories.
    Sandboxed tools see an empty directory (``ENOENT`` for missing entries)
    instead of the host tree.

    Returns ``True`` on success (including an empty path list), ``False`` when
    the namespace backend is unavailable. Mount failures raise ``OSError``;
    callers must not continue with a partially prepared mount tree.
    """

    path_list = list(paths)
    plan = build_namespace_mount_plan(path_list, stage_path, preserved_sources)
    if not namespace_ready and not prepare_empty_directory_masking(path_list, libc):
        return False
    if libc is None:
        libc = ctypes.CDLL(None, use_errno=True)
    return _apply_namespace_mount_plan(plan, libc)


class NamespaceSandbox(Sandbox):
    """Sandbox backend that applies Linux user/mount namespace filesystem policy.

    On Linux, when unprivileged user and mount namespaces are available, this
    backend is preferred over the Landlock-only backend because it can hide host
    filesystem content via empty mounts and bind mounts, rather than only
    denying access through Landlock rules.

    The legacy narrow mount path may still delegate ``allow_read`` /
    ``allow_write`` to an internal ``LandlockSandbox``. A complete selected
    filesystem policy does not construct or apply Landlock.
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
        self._filesystem_policy_active = False
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

    @property
    def filesystem_policy_active(self) -> bool:
        """Return whether the complete selected filesystem policy is active."""
        return self._filesystem_policy_active

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

    def prepare_mount_tree(
        self,
        hidden_dirs: Iterable[str],
        stage_path: str,
        preserved_sources: Iterable[NamespaceMountRequest] = (),
    ) -> bool:
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
        plan = build_namespace_mount_plan(hidden_list, stage_path, preserved_sources)
        if not prepare_empty_directory_masking(hidden_list, self.libc):
            return False
        libc = self.libc or ctypes.CDLL(None, use_errno=True)
        self._namespace_ready = _apply_namespace_mount_plan(plan, libc)
        return self._namespace_ready

    def prepare_filesystem_policy(
        self, policy: NamespaceFilesystemPolicy, stage_path: str
    ) -> bool:
        """Validate and apply a complete policy before entering the namespace."""
        if self._namespace_ready:
            return True
        plan = build_namespace_mount_plan_from_policy(policy, stage_path)
        self._hidden_dirs = list(policy.hidden_roots)
        self._stage_path = stage_path
        if not prepare_empty_directory_masking(policy.hidden_roots, self.libc):
            return False
        libc = self.libc or ctypes.CDLL(None, use_errno=True)
        self._namespace_ready = _apply_namespace_mount_plan(plan, libc)
        self._filesystem_policy_active = self._namespace_ready
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
        """Apply legacy Landlock rules when no complete policy is active.

        If no rules were granted, an empty deny-by-default Landlock ruleset is
        still applied so the namespace is not left unconstrained.
        """
        if self._filesystem_policy_active:
            return
        self._ensure_landlock().apply(block_network=block_network)

    def cleanup(self) -> None:
        """No-op for the namespace case.

        The namespace, its mount tree, and the Landlock ruleset all die with the
        process.
        """
