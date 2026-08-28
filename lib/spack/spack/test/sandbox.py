# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Unit tests for Linux Landlock sandboxing in the new installer."""

import sys

import pytest

if sys.platform != "linux":
    pytest.skip("Landlock sandboxing is Linux only", allow_module_level=True)

import os
import pathlib
from typing import List, Tuple

import spack.sandbox


class SpyLandlockSandbox(spack.sandbox.LandlockSandbox):
    """LandlockSandbox that records _syscall_* and _prctl_* calls."""

    def __init__(self, abi_version: int = 3) -> None:
        self._abi_version_override = abi_version
        super().__init__()
        self._fds: List[int] = []
        self.ruleset_fd = -1
        # (fs_flags, net_flags)
        self.create_ruleset_calls: List[Tuple[int, int]] = []
        # (ruleset_fd, allowed_access, path_fd)
        self.add_rule_calls: List[Tuple[int, int, int]] = []
        # (ruleset_fd, tsync_flag)
        self.restrict_self_calls: List[Tuple[int, int]] = []
        self.prctl_called: bool = False

    def __del__(self):
        for fd in self._fds:
            os.close(fd)

    def _new_fd(self) -> int:
        fd = os.open(os.devnull, os.O_RDONLY)
        self._fds.append(fd)
        return fd

    def _get_abi_version(self) -> int:
        return self._abi_version_override

    def _syscall_create_ruleset(self, handled_access_fs: int, handled_access_net: int) -> int:
        self.create_ruleset_calls.append((handled_access_fs, handled_access_net))
        self.ruleset_fd = self._new_fd()
        return self.ruleset_fd

    def _syscall_add_rule(self, ruleset_fd: int, allowed_access: int, path_fd: int) -> None:
        self.add_rule_calls.append((ruleset_fd, allowed_access, path_fd))

    def _syscall_restrict_self(self, ruleset_fd: int, tsync_flag: int) -> None:
        self.restrict_self_calls.append((ruleset_fd, tsync_flag))

    def _prctl_no_new_privs(self) -> None:
        self.prctl_called = True


def test_landlock_sandbox_syscall_args(tmp_path: pathlib.Path):
    """Test that LandlockSandbox passes correct arguments to each syscall."""
    sandbox = SpyLandlockSandbox(abi_version=3)

    test_dir = tmp_path / "dir"
    test_dir.mkdir()
    test_file = test_dir / "file"
    test_file.touch()

    sandbox.allow_read(test_dir)
    sandbox.allow_write(test_file)
    sandbox.apply(block_network=False)

    # Ruleset covers both read and write access; no network flags
    [(fs_flags, net_flags)] = sandbox.create_ruleset_calls
    assert fs_flags & spack.sandbox.FSAccess.READ_FILE
    assert fs_flags & spack.sandbox.FSAccess.WRITE_FILE
    assert net_flags == 0

    # One rule per path, both using the same ruleset fd
    assert len(sandbox.add_rule_calls) == 2
    for ruleset_fd, _access, path_fd in sandbox.add_rule_calls:
        assert ruleset_fd == sandbox.ruleset_fd
        assert path_fd > 0

    # Read-only directory: has READ_DIR, no WRITE_FILE
    dir_access = next(
        a for _, a, _ in sandbox.add_rule_calls if a & spack.sandbox.FSAccess.READ_DIR
    )
    assert not (dir_access & spack.sandbox.FSAccess.WRITE_FILE)

    # Write file: has WRITE_FILE, no READ_DIR (dir flags stripped for non-dirs)
    file_access = next(
        a for _, a, _ in sandbox.add_rule_calls if a & spack.sandbox.FSAccess.WRITE_FILE
    )
    assert not (file_access & spack.sandbox.FSAccess.READ_DIR)

    # RESTRICT_SELF gets the correct ruleset fd
    [(restrict_fd, tsync)] = sandbox.restrict_self_calls
    assert restrict_fd == sandbox.ruleset_fd
    assert tsync == 0  # ABI v3: no tsync flag

    assert sandbox.prctl_called


def test_landlock_sandbox_network_args():
    """Test that block_network=True sets the correct net flags in the ruleset."""
    sandbox = SpyLandlockSandbox(abi_version=4)
    sandbox.apply(block_network=True)

    [(_, net_flags)] = sandbox.create_ruleset_calls
    assert net_flags & spack.sandbox.LANDLOCK_ACCESS_NET_CONNECT_TCP
    assert net_flags & spack.sandbox.LANDLOCK_ACCESS_NET_BIND_TCP
    assert sandbox.prctl_called


def test_sandbox_network_blocking_requires_abi_v4():
    """Test that blocking network access on an older kernel raises a RuntimeError."""
    sandbox = SpyLandlockSandbox(abi_version=3)

    with pytest.raises(
        spack.sandbox.SandboxError, match="Blocking network access requires Landlock ABI v4\\+"
    ):
        sandbox.apply(block_network=True)
