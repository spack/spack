# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module implements an unprivileged sandbox for build environments.

It enforces path-based filesystem whitelisting and optional network isolation,
dynamically adapting to the host kernel's supported Landlock ABI version.

By design, to support standard build system behaviors like `try_compile` tests,
read access implicitly includes execution rights. IOCTLs and IPC mechanisms are
left unrestricted to ensure compatibility with compilers, terminal output, and
build jobservers.
"""

import atexit
import ctypes
import enum
import os
import platform
import stat
import sys
import uuid
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Union

# os.O_PATH is only defined on linux. Appease mypy with our own O_PATH.
if sys.platform == "linux":
    O_PATH = os.O_PATH
else:
    O_PATH = 0

import spack.error
import spack.util.executable

# Linux landlock syscalls
SYSCALL_LANDLOCK_CREATE_RULESET = 444
SYSCALL_LANDLOCK_ADD_RULE = 445
SYSCALL_LANDLOCK_RESTRICT_SELF = 446

PR_SET_NO_NEW_PRIVS = 38
LANDLOCK_CREATE_RULESET_VERSION = 1 << 0
LANDLOCK_RULE_PATH_BENEATH = 1
LANDLOCK_ACCESS_NET_BIND_TCP = 1 << 0
LANDLOCK_ACCESS_NET_CONNECT_TCP = 1 << 1
LANDLOCK_RESTRICT_SELF_TSYNC = 1 << 3


class FSAccess(enum.IntFlag):
    EXECUTE = 1 << 0
    WRITE_FILE = 1 << 1
    READ_FILE = 1 << 2
    READ_DIR = 1 << 3
    REMOVE_DIR = 1 << 4
    REMOVE_FILE = 1 << 5
    MAKE_CHAR = 1 << 6
    MAKE_DIR = 1 << 7
    MAKE_REG = 1 << 8
    MAKE_SOCK = 1 << 9
    MAKE_FIFO = 1 << 10
    MAKE_BLOCK = 1 << 11
    MAKE_SYM = 1 << 12
    REFER = 1 << 13  # ABI v2
    TRUNCATE = 1 << 14  # ABI v3


def _check_syscall(result: int, name: str) -> int:
    """Raise OSError if a libc syscall returned a negative value.

    Mirrors what Python's stdlib does for syscall-backed os.* functions.
    """
    if result < 0:
        err = ctypes.get_errno()
        raise OSError(err, f"{name}: {os.strerror(err)}")
    return result


class RulesetAttr(ctypes.Structure):
    _fields_ = [
        ("handled_access_fs", ctypes.c_uint64),
        ("handled_access_net", ctypes.c_uint64),
        ("scoped", ctypes.c_uint64),
    ]


class PathBeneathAttr(ctypes.Structure):
    _fields_ = [("allowed_access", ctypes.c_uint64), ("parent_fd", ctypes.c_int32)]


class Sandbox(ABC):
    """Abstract base class for sandbox implementations."""

    def allow_read(self, path: Union[str, Path]):
        p = Path(path).absolute()
        resolved = p.resolve()
        if resolved.exists():
            self._allow_read(p, resolved)

    def allow_write(self, path: Union[str, Path]):
        p = Path(path).absolute()
        resolved = p.resolve()
        if resolved.exists():
            self._allow_write(p, resolved)

    @abstractmethod
    def _allow_read(self, original: Path, resolved: Path): ...

    @abstractmethod
    def _allow_write(self, original: Path, resolved: Path): ...

    @abstractmethod
    def apply(self, block_network: bool = False): ...

    def cleanup(self) -> None:
        """Release any resources held by the sandbox. No-op by default.

        Landlock's restrictions live in the kernel and are torn down automatically when the
        process exits, so LandlockSandbox does not need to override this. Backends that hold
        external state (e.g. Windows AppContainer profiles and ACL grants) must override it.
        """


def _get_write_flags(abi_version: int) -> int:
    flags = (
        FSAccess.MAKE_BLOCK
        | FSAccess.MAKE_CHAR
        | FSAccess.MAKE_DIR
        | FSAccess.MAKE_FIFO
        | FSAccess.MAKE_REG
        | FSAccess.MAKE_SOCK
        | FSAccess.MAKE_SYM
        | FSAccess.REMOVE_DIR
        | FSAccess.REMOVE_FILE
        | FSAccess.WRITE_FILE
    )
    if abi_version >= 2:
        flags |= FSAccess.REFER
    if abi_version >= 3:
        flags |= FSAccess.TRUNCATE
    return flags


class LandlockSandbox(Sandbox):
    def __init__(self, libc=None):
        self.libc = libc if libc is not None else ctypes.CDLL(None, use_errno=True)
        self.abi_version = self._get_abi_version()
        self.path_rules: Dict[Path, int] = {}
        self.write_flags = _get_write_flags(self.abi_version)
        self.read_flags = FSAccess.EXECUTE | FSAccess.READ_FILE | FSAccess.READ_DIR
        self.dir_flags = (
            FSAccess.MAKE_BLOCK
            | FSAccess.MAKE_CHAR
            | FSAccess.MAKE_DIR
            | FSAccess.MAKE_FIFO
            | FSAccess.MAKE_REG
            | FSAccess.MAKE_SOCK
            | FSAccess.MAKE_SYM
            | FSAccess.READ_DIR
            | FSAccess.REFER
            | FSAccess.REMOVE_DIR
            | FSAccess.REMOVE_FILE
        )

    def _get_abi_version(self) -> int:
        res = self.libc.syscall(
            ctypes.c_long(SYSCALL_LANDLOCK_CREATE_RULESET),
            None,
            ctypes.c_size_t(0),
            ctypes.c_uint32(LANDLOCK_CREATE_RULESET_VERSION),
        )
        return _check_syscall(res, "landlock_create_ruleset(version)")

    def _allow_read(self, original: Path, resolved: Path):
        current_flags = self.path_rules.get(resolved, 0)
        self.path_rules[resolved] = current_flags | self.read_flags

    def _allow_write(self, original: Path, resolved: Path):
        current_flags = self.path_rules.get(resolved, 0)
        self.path_rules[resolved] = current_flags | self.write_flags | self.read_flags

    def _syscall_create_ruleset(self, handled_access_fs: int, handled_access_net: int) -> int:
        attr = RulesetAttr(
            handled_access_fs=handled_access_fs, handled_access_net=handled_access_net
        )
        return _check_syscall(
            self.libc.syscall(
                ctypes.c_long(SYSCALL_LANDLOCK_CREATE_RULESET),
                ctypes.byref(attr),
                ctypes.c_size_t(ctypes.sizeof(attr)),
                ctypes.c_uint32(0),
            ),
            "landlock_create_ruleset",
        )

    def _syscall_add_rule(self, ruleset_fd: int, allowed_access: int, path_fd: int) -> None:
        rule = PathBeneathAttr(allowed_access=allowed_access, parent_fd=path_fd)
        _check_syscall(
            self.libc.syscall(
                ctypes.c_long(SYSCALL_LANDLOCK_ADD_RULE),
                ctypes.c_int(ruleset_fd),
                ctypes.c_int(LANDLOCK_RULE_PATH_BENEATH),
                ctypes.byref(rule),
                ctypes.c_uint32(0),
            ),
            "landlock_add_rule",
        )

    def _syscall_restrict_self(self, ruleset_fd: int, tsync_flag: int) -> None:
        _check_syscall(
            self.libc.syscall(
                ctypes.c_long(SYSCALL_LANDLOCK_RESTRICT_SELF),
                ctypes.c_int(ruleset_fd),
                ctypes.c_uint32(tsync_flag),
            ),
            "landlock_restrict_self",
        )

    def _prctl_no_new_privs(self) -> None:
        _check_syscall(
            self.libc.prctl(
                ctypes.c_int(PR_SET_NO_NEW_PRIVS),
                ctypes.c_ulong(1),
                ctypes.c_ulong(0),
                ctypes.c_ulong(0),
                ctypes.c_ulong(0),
            ),
            "prctl(PR_SET_NO_NEW_PRIVS)",
        )

    def apply(self, block_network: bool = False):
        # Network access requires ABI v4
        if block_network and self.abi_version < 4:
            raise SandboxError(
                f"Blocking network access requires Landlock ABI v4+ (kernel 6.7+), "
                f"but this kernel only supports ABI v{self.abi_version}."
            )
        net_flags = (
            LANDLOCK_ACCESS_NET_CONNECT_TCP | LANDLOCK_ACCESS_NET_BIND_TCP if block_network else 0
        )
        try:
            self._apply(net_flags)
        except OSError as e:
            raise SandboxError(f"Failed to apply build sandbox: {e}") from e

    def _apply(self, net_flags: int) -> None:
        ruleset_fd = self._syscall_create_ruleset(self.write_flags | self.read_flags, net_flags)

        try:
            for path, flags in self.path_rules.items():
                try:
                    # use O_PATH to get an fd w/o needing permissions, and O_NOFOLLOW to avoid
                    # TOCTOU issues after we've called resolve() on the path.
                    fd = os.open(str(path), O_PATH | os.O_CLOEXEC | os.O_NOFOLLOW)
                except OSError as e:
                    warnings.warn(f"Cannot allow sandbox access to {path} due to: {e}")
                    continue
                try:
                    st = os.fstat(fd)
                    if not stat.S_ISDIR(st.st_mode):
                        # Strip directory-specific flags
                        flags &= ~self.dir_flags
                    self._syscall_add_rule(ruleset_fd, flags, fd)
                finally:
                    os.close(fd)

            # Lock down the current process with this ruleset
            self._prctl_no_new_privs()
            tsync_flag = LANDLOCK_RESTRICT_SELF_TSYNC if self.abi_version >= 8 else 0
            self._syscall_restrict_self(ruleset_fd, tsync_flag)
        finally:
            os.close(ruleset_fd)


#: Capabilities granted when ``allow_network`` is true. An AppContainer starts with *no* network
#: access at all, so approximating Landlock's "unrestricted unless blocked" default takes all
#: three: ``internetClient`` is outbound-internet only, ``internetClientServer`` adds inbound,
#: and ``privateNetworkClientServer`` covers RFC1918/LAN hosts such as an internal Spack mirror.
#: Loopback is not reachable via any capability; it needs a separate exemption Spack does not
#: configure (see the Windows section of the sandboxing docs).
NETWORK_CAPABILITIES = ["internetClient", "internetClientServer", "privateNetworkClientServer"]


class WindowsAppContainerSandbox(Sandbox):
    """Sandbox backend using Windows AppContainer isolation.

    Unlike Landlock, an AppContainer can only be established at process-creation time: there
    is no supported way to convert an already-running process into one. As a result, this
    backend cannot self-restrict the current process the way LandlockSandbox does. Instead,
    `apply()` finalizes a policy (a set of granted paths, plus capabilities) and installs
    `_spawn_in_container` as `spack.util.executable`'s process spawner, so that every build
    tool Spack runs from that point on starts inside the container. Direct in-process Python
    file I/O performed by package recipes is therefore not confined on Windows.
    """

    def __init__(self) -> None:
        # Imported lazily so non-Windows interpreters never touch ctypes.wintypes-based code.
        import spack.util.win_acl as win_acl
        import spack.util.win_appcontainer as win_appcontainer

        self._win = win_appcontainer
        # Side-effect-free probe: raises OSError if the required APIs aren't resolvable.
        # installer_dispatch.py calls get_sandbox() eagerly just to fail fast, and discards
        # the result, so no profile may be created here.
        self._win.probe_support()

        self.container_name = f"spack-{os.getpid()}-{uuid.uuid4().hex[:8]}"
        self.path_rules: Dict[Path, int] = {}
        # Read implies execute, matching Landlock, so that configure-time compile probes run.
        self.read_mask = (
            win_acl.FileAccessRights.FILE_GENERIC_READ
            | win_acl.FileAccessRights.FILE_GENERIC_EXECUTE
        )
        self.write_mask = (
            self.read_mask
            | win_acl.FileAccessRights.FILE_GENERIC_WRITE
            | win_acl.StandardAccessRights.DELETE
        )

        self.sid: Optional[int] = None
        self.capabilities: List[int] = []
        self._granted_paths: List[Path] = []
        self._active = False
        self._previous_spawner: Optional[spack.util.executable.ProcessSpawner] = None

    @staticmethod
    def _is_securable(resolved: Path) -> bool:
        """Whether `resolved` is an object an ACL can actually be attached to.

        Windows reserved device names (NUL, CON, ...) pass Path.exists() from any directory but
        have no DACL, so trying to grant on them fails with ERROR_ACCESS_DENIED. NUL in
        particular is always reachable from an AppContainer, and _enable_sandbox always asks for
        os.devnull, so silently skipping devices avoids a warning on every single build.
        """
        return resolved.is_dir() or resolved.is_file()

    def _allow_read(self, original: Path, resolved: Path):
        if not self._is_securable(resolved):
            return
        current_mask = self.path_rules.get(resolved, 0)
        self.path_rules[resolved] = current_mask | self.read_mask

    def _allow_write(self, original: Path, resolved: Path):
        if not self._is_securable(resolved):
            return
        current_mask = self.path_rules.get(resolved, 0)
        self.path_rules[resolved] = current_mask | self.write_mask

    # Each Win32 call below is wrapped in its own one-line method so tests can override it
    # individually, the same way test/sandbox.py's SpyLandlockSandbox stubs out syscalls.

    def _create_app_container(self) -> int:
        return self._win.create_or_derive_app_container_sid(self.container_name)

    def _derive_capabilities(self, names: List[str]) -> List[int]:
        return self._win.derive_capability_sids(names)

    def _grant(self, path: Path, sid: int) -> None:
        self._win.grant_access(str(path), sid, self.path_rules[path])

    def _revoke(self, path: Path, sid: int) -> None:
        self._win.revoke_access(str(path), sid)

    def _delete_profile(self) -> None:
        self._win.delete_app_container_profile(self.container_name, self.sid)
        self._win.release_capability_sids(self.capabilities)
        self.capabilities = []

    def _spawn_in_container(
        self,
        cmd: List[str],
        *,
        env: Dict[str, str],
        stdin: spack.util.executable.StreamType,
        stdout: spack.util.executable.StreamType,
        stderr: spack.util.executable.StreamType,
    ) -> spack.util.executable.SpawnedProcess:
        """Start `cmd` inside this sandbox's AppContainer.

        Installed as spack.util.executable's process spawner for as long as this sandbox is
        applied, which is what confines the build tools Spack runs.
        """
        assert self.sid is not None, "the spawner is only installed between apply() and cleanup()"
        return self._win.create_process(
            cmd,
            env=env,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            sid=self.sid,
            capabilities=self.capabilities,
        )

    def apply(self, block_network: bool = False) -> None:
        # An AppContainer has no network access at all unless a capability is granted, the
        # opposite default of Landlock, which is unrestricted unless block_network=True.
        capability_names = [] if block_network else list(NETWORK_CAPABILITIES)
        try:
            self.sid = self._create_app_container()
            # From here on the profile exists in the OS, so any later failure has to go
            # through cleanup() rather than leaving an orphaned container behind.
            self._active = True
            self.capabilities = self._derive_capabilities(capability_names)
        except OSError as e:
            self.cleanup()
            raise SandboxError(f"Failed to apply build sandbox: {e}") from e

        for path in self.path_rules:
            try:
                self._grant(path, self.sid)
            except OSError as e:
                warnings.warn(f"Cannot allow sandbox access to {path} due to: {e}")
                continue
            self._granted_paths.append(path)

        # Route every subsequent Executable through the container. Done last, so a spawn can
        # never observe a half-built policy.
        self._previous_spawner = spack.util.executable.set_process_spawner(
            self._spawn_in_container
        )
        _set_active_sandbox(self)
        # Safety net for paths that bypass the installer's explicit cleanup (e.g. an
        # exception escaping the build worker). cleanup() is idempotent, so running twice
        # is harmless.
        atexit.register(self.cleanup)

    def cleanup(self) -> None:
        if not self._active:
            return
        self._active = False
        atexit.unregister(self.cleanup)

        # Stop routing spawns into the container before dismantling it, so nothing can be
        # launched against a container whose grants are already being revoked.
        if self._previous_spawner is not None:
            spack.util.executable.set_process_spawner(self._previous_spawner)
            self._previous_spawner = None

        # A path can only have been granted against a SID, so one exists whenever this is
        # non-empty; apply() bails out before granting anything if the container never came up.
        if self._granted_paths:
            assert self.sid is not None, "granted paths always imply a live container SID"
            for path in self._granted_paths:
                try:
                    self._revoke(path, self.sid)
                except OSError as e:
                    warnings.warn(f"Cannot revoke sandbox access to {path} due to: {e}")
            self._granted_paths = []

        try:
            self._delete_profile()
        except OSError as e:
            warnings.warn(f"Cannot delete sandbox AppContainer profile due to: {e}")
        # The SID memory is freed by _delete_profile; drop the now-dangling pointer so a
        # stale use is a clean AttributeError-style failure rather than a wild pointer.
        self.sid = None

        if active_sandbox() is self:
            _set_active_sandbox(None)


def get_sandbox() -> Sandbox:
    system = platform.system()
    try:
        if system == "Linux":
            return LandlockSandbox()
        elif system == "Windows":
            return WindowsAppContainerSandbox()
        else:
            raise SandboxError(f"Build sandboxing is not supported on {system}")
    except OSError as e:
        raise SandboxError(f"Sandboxing is unavailable: {e}") from e


_active_sandbox: Optional[Sandbox] = None


def active_sandbox() -> Optional[Sandbox]:
    """Return the sandbox currently active for this process, if any.

    Only backends holding resources that outlive `apply()` register here, so that the installer
    can tear them down; today that means WindowsAppContainerSandbox. LandlockSandbox restricts
    the process itself in place and its ruleset dies with the process, so it never registers.
    """
    return _active_sandbox


def _set_active_sandbox(sandbox: Optional[Sandbox]) -> None:
    global _active_sandbox
    _active_sandbox = sandbox


def cleanup_active_sandbox() -> None:
    """Idempotent no-op if no sandbox is active."""
    sandbox = active_sandbox()
    if sandbox is not None:
        sandbox.cleanup()


class SandboxError(spack.error.SpackError):
    """Raised when the build sandbox cannot be set up or applied."""
