# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Implements a sandboxing mechanism for build processes using Linux Landlock."""

import ctypes
import enum
import os
import platform
import stat
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Union

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


class LandlockSandbox(Sandbox):
    def __init__(self, libc=None):
        self.libc = libc if libc is not None else ctypes.CDLL(None, use_errno=True)
        self.abi_version = self._get_abi_version()
        self.path_rules: Dict[Path, int] = {}

    def _get_abi_version(self) -> int:
        res = self.libc.syscall(
            ctypes.c_long(SYSCALL_LANDLOCK_CREATE_RULESET),
            None,
            ctypes.c_size_t(0),
            ctypes.c_uint32(LANDLOCK_CREATE_RULESET_VERSION),
        )
        return _check_syscall(res, "landlock_create_ruleset(version)")

    def _get_write_flags(self) -> int:
        flags = (
            FSAccess.WRITE_FILE
            | FSAccess.REMOVE_DIR
            | FSAccess.REMOVE_FILE
            | FSAccess.MAKE_CHAR
            | FSAccess.MAKE_DIR
            | FSAccess.MAKE_REG
            | FSAccess.MAKE_SOCK
            | FSAccess.MAKE_FIFO
            | FSAccess.MAKE_BLOCK
            | FSAccess.MAKE_SYM
        )
        if self.abi_version >= 2:
            flags |= FSAccess.REFER
        if self.abi_version >= 3:
            flags |= FSAccess.TRUNCATE
        return flags

    def _get_read_flags(self) -> int:
        return FSAccess.EXECUTE | FSAccess.READ_FILE | FSAccess.READ_DIR

    def _allow_read(self, original: Path, resolved: Path):
        current_flags = self.path_rules.get(resolved, 0)
        self.path_rules[resolved] = current_flags | self._get_read_flags()

    def _allow_write(self, original: Path, resolved: Path):
        current_flags = self.path_rules.get(resolved, 0)
        self.path_rules[resolved] = (
            current_flags | self._get_write_flags() | self._get_read_flags()
        )

    def apply(self, block_network: bool = False):
        handled_fs = self._get_write_flags() | self._get_read_flags()
        attr = RulesetAttr(handled_access_fs=handled_fs)

        # Network access requires ABI v4
        if block_network and self.abi_version < 4:
            raise RuntimeError(
                f"Blocking network access requires Landlock ABI v4+ (kernel 6.7+), "
                f"but this kernel only supports ABI v{self.abi_version}."
            )
        if block_network:
            attr.handled_access_net = (
                LANDLOCK_ACCESS_NET_CONNECT_TCP | LANDLOCK_ACCESS_NET_BIND_TCP
            )

        ruleset_fd = _check_syscall(
            self.libc.syscall(
                ctypes.c_long(SYSCALL_LANDLOCK_CREATE_RULESET),
                ctypes.byref(attr),
                ctypes.c_size_t(ctypes.sizeof(attr)),
                ctypes.c_uint32(0),
            ),
            "landlock_create_ruleset",
        )

        try:
            for path, flags in self.path_rules.items():
                try:
                    fd = os.open(str(path), os.O_PATH | os.O_CLOEXEC)
                except OSError:
                    continue
                try:
                    st = os.fstat(fd)
                    if not stat.S_ISDIR(st.st_mode):
                        # Strip directory-specific flags
                        flags &= ~(
                            FSAccess.REMOVE_DIR
                            | FSAccess.REMOVE_FILE
                            | FSAccess.MAKE_DIR
                            | FSAccess.MAKE_CHAR
                            | FSAccess.MAKE_SOCK
                            | FSAccess.MAKE_FIFO
                            | FSAccess.MAKE_BLOCK
                            | FSAccess.MAKE_SYM
                            | FSAccess.REFER
                            | FSAccess.READ_DIR
                            | FSAccess.MAKE_REG
                        )

                    rule = PathBeneathAttr(allowed_access=flags, parent_fd=fd)
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
                finally:
                    os.close(fd)

            # Lock down the current process with this ruleset
            _check_syscall(
                self.libc.prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0), "prctl(PR_SET_NO_NEW_PRIVS)"
            )
            tsync_flag = LANDLOCK_RESTRICT_SELF_TSYNC if self.abi_version >= 8 else 0
            _check_syscall(
                self.libc.syscall(
                    ctypes.c_long(SYSCALL_LANDLOCK_RESTRICT_SELF),
                    ctypes.c_int(ruleset_fd),
                    ctypes.c_uint32(tsync_flag),
                ),
                "landlock_restrict_self",
            )
        finally:
            os.close(ruleset_fd)


def get_sandbox() -> Sandbox:
    if platform.system() == "Linux":
        return LandlockSandbox()

    raise OSError("Sandboxing is not supported on this platform.")
