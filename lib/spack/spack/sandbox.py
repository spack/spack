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

import ctypes
import enum
import os
import platform
import stat
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Union

import spack.error

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
                    fd = os.open(str(path), os.O_PATH | os.O_CLOEXEC | os.O_NOFOLLOW)
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


def get_sandbox() -> Sandbox:
    if platform.system() != "Linux":
        raise SandboxError("Build sandboxing is only supported on Linux")
    try:
        return LandlockSandbox()
    except OSError as e:
        raise SandboxError(f"Landlock sandboxing is unavailable: {e}") from e


class SandboxError(spack.error.SpackError):
    """Raised when the build sandbox cannot be set up or applied."""
