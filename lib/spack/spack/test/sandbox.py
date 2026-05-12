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
import tempfile
from typing import List, Tuple

import spack.concretize
import spack.sandbox
import spack.store
from spack.new_installer import _enable_sandbox


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


class MockSandbox(spack.sandbox.Sandbox):
    def __init__(self):
        self.read_calls: List[Tuple[pathlib.Path, pathlib.Path]] = []
        self.write_calls: List[Tuple[pathlib.Path, pathlib.Path]] = []
        self.apply_calls: List[bool] = []

    def _allow_read(self, original: pathlib.Path, resolved: pathlib.Path):
        self.read_calls.append((original, resolved))

    def _allow_write(self, original: pathlib.Path, resolved: pathlib.Path):
        self.write_calls.append((original, resolved))

    def apply(self, block_network=False):
        self.apply_calls.append(block_network)


def test_enable_sandbox_paths(
    monkeypatch, mock_packages, temporary_store: spack.store.Store, tmp_path: pathlib.Path
):
    """Test that _enable_sandbox in new_installer calls allow_read/allow_write correctly."""
    mock_sandbox = MockSandbox()
    monkeypatch.setattr(spack.sandbox, "get_sandbox", lambda: mock_sandbox)

    spec = spack.concretize.concretize_one("dependent-install")

    # Create prefix directories so resolved.exists() passes
    pathlib.Path(spec.prefix).mkdir(parents=True, exist_ok=True)
    for dep in spec.traverse(root=False):
        pathlib.Path(dep.prefix).mkdir(parents=True, exist_ok=True)

    stage_path = tmp_path / "stage"
    stage_path.mkdir()

    custom_write = tmp_path / "custom_write"
    custom_write.mkdir()

    # Create a symlink to verify original vs resolved path logic
    custom_read_target = tmp_path / "custom_read_target"
    custom_read_target.mkdir()
    custom_read_link = tmp_path / "custom_read_link"
    custom_read_link.symlink_to(custom_read_target)

    # Ensure the sbang exists
    temporary_store.install_sbang()
    sbang_file = pathlib.Path(temporary_store.unpadded_root) / "bin" / "sbang"

    config = {
        "enable": True,
        "allow_read": [str(custom_read_link)],
        "allow_write": [str(custom_write)],
        "allow_network": True,
    }

    _enable_sandbox(config, spec, str(stage_path))

    allow_read_resolved = [c[1] for c in mock_sandbox.read_calls]
    for dep in spec.traverse(root=False):
        assert pathlib.Path(dep.prefix).resolve() in allow_read_resolved

    # Verify symlink resolution in read_calls
    assert custom_read_target.resolve() in allow_read_resolved
    assert (custom_read_link.absolute(), custom_read_target.resolve()) in mock_sandbox.read_calls

    # Verify sbang read
    assert sbang_file.resolve() in allow_read_resolved

    allow_write_resolved = [c[1] for c in mock_sandbox.write_calls]
    assert stage_path.resolve() in allow_write_resolved
    assert pathlib.Path(spec.prefix).resolve() in allow_write_resolved
    assert custom_write.resolve() in allow_write_resolved
    assert pathlib.Path(tempfile.gettempdir()).resolve() in allow_write_resolved

    assert mock_sandbox.apply_calls == [False]


def test_sandbox_network_blocking_requires_abi_v4():
    """Test that blocking network access on an older kernel raises a RuntimeError."""
    sandbox = SpyLandlockSandbox(abi_version=3)

    with pytest.raises(
        spack.sandbox.SandboxError, match="Blocking network access requires Landlock ABI v4\\+"
    ):
        sandbox.apply(block_network=True)
