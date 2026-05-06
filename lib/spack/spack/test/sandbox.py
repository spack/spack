# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Unit tests for Linux Landlock sandboxing in the new installer."""

import os
import pathlib
import sys
import tempfile
from typing import List, Tuple

import pytest

import spack.concretize
import spack.sandbox
import spack.store
from spack.new_installer import _enable_sandbox


class MockLibc:
    def __init__(self, abi_version: int = 3) -> None:
        self.abi_version = abi_version
        self.syscall_calls: List[tuple] = []
        self.prctl_calls: List[tuple] = []
        self.dummy_fd = os.open(os.devnull, os.O_RDONLY)

    def syscall(self, syscall_num, *args):
        self.syscall_calls.append((syscall_num, *args))
        if syscall_num.value == spack.sandbox.SYSCALL_LANDLOCK_CREATE_RULESET and args[0] is None:
            return self.abi_version
        if syscall_num.value == spack.sandbox.SYSCALL_LANDLOCK_CREATE_RULESET:
            return os.dup(self.dummy_fd)
        return 0  # Return success for add_rule and restrict_self

    def prctl(self, *args):
        self.prctl_calls.append(tuple(x.value for x in args))
        return 0


@pytest.mark.skipif(sys.platform != "linux", reason="Landlock is Linux only")
def test_landlock_sandbox(tmp_path: pathlib.Path):
    """Test LandlockSandbox properly configures and applies rules via mocked libc."""
    mock_libc = MockLibc()

    sandbox = spack.sandbox.LandlockSandbox(libc=mock_libc)
    assert isinstance(sandbox, spack.sandbox.LandlockSandbox)

    test_dir = tmp_path / "somedir"
    test_dir.mkdir()
    test_file = test_dir / "somefile"
    test_file.touch()

    sandbox.allow_read(test_dir)
    sandbox.allow_write(test_file)

    sandbox.apply(block_network=False)

    assert mock_libc.prctl_calls == [(spack.sandbox.PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)]

    syscall_calls = mock_libc.syscall_calls
    create_ruleset_calls = [
        call
        for call in syscall_calls
        if call[0].value == spack.sandbox.SYSCALL_LANDLOCK_CREATE_RULESET
    ]
    assert len(create_ruleset_calls) == 2  # 1 for ABI version check, 1 for ruleset creation

    add_rule_calls = [
        call for call in syscall_calls if call[0].value == spack.sandbox.SYSCALL_LANDLOCK_ADD_RULE
    ]
    assert len(add_rule_calls) == 2  # 1 for dir, 1 for file

    restrict_self_calls = [
        call
        for call in syscall_calls
        if call[0].value == spack.sandbox.SYSCALL_LANDLOCK_RESTRICT_SELF
    ]
    assert len(restrict_self_calls) == 1
    assert restrict_self_calls[0][1].value > 0  # Valid fd returned by mock_syscall


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


@pytest.mark.skipif(sys.platform != "linux", reason="Landlock is Linux only")
def test_sandbox_network_blocking_requires_abi_v4():
    """Test that blocking network access on an older kernel raises a RuntimeError."""
    mock_libc = MockLibc(abi_version=3)
    sandbox = spack.sandbox.LandlockSandbox(libc=mock_libc)

    with pytest.raises(RuntimeError, match="Blocking network access requires Landlock ABI v4\\+"):
        sandbox.apply(block_network=True)


@pytest.mark.skipif(sys.platform != "linux", reason="Landlock is Linux only")
def test_sandbox_network_blocking_allows_abi_v4(tmp_path: pathlib.Path):
    """Test that blocking network access on a supported kernel works."""
    mock_libc = MockLibc(abi_version=4)
    sandbox = spack.sandbox.LandlockSandbox(libc=mock_libc)
    sandbox.apply(block_network=True)
    assert mock_libc.prctl_calls == [(spack.sandbox.PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)]
