# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Unit tests for Windows AppContainer sandboxing in the new installer.

Most tests here spy on WindowsAppContainerSandbox's small overridable wrapper methods
(_create_app_container, _derive_capabilities, _grant, _revoke, _delete_profile) rather than
exercising the real Win32 APIs, mirroring how test/sandbox.py's SpyLandlockSandbox spies on
Landlock syscalls.

Spies alone cannot answer the only question that really matters -- whether the sandbox actually
denies anything -- so the tests at the bottom of this module drive the real
CreateAppContainerProfile/ACL/CreateProcessW path end to end and assert that reads, writes and
network connections outside the policy are refused by the OS. Those tests do mutate system
state (an AppContainer profile plus DACL entries under tmp_path), but they clean up after
themselves and need no elevation.
"""

import os
import pathlib
import sys
from typing import List, Set, Tuple

import pytest

if sys.platform != "win32":
    pytest.skip("Windows-only tests", allow_module_level=True)

import spack.sandbox
import spack.util.executable as executable
import spack.util.win_acl as win_acl
from spack.util.executable import Executable


class SpyWindowsAppContainerSandbox(spack.sandbox.WindowsAppContainerSandbox):
    """WindowsAppContainerSandbox that records calls instead of touching the real OS."""

    def __init__(self) -> None:
        super().__init__()
        self.create_app_container_calls = 0
        self.derive_capabilities_calls: List[List[str]] = []
        self.grant_calls: List[Tuple[pathlib.Path, int]] = []
        self.revoke_calls: List[Tuple[pathlib.Path, int]] = []
        self.delete_profile_calls = 0
        self.fail_grant_for: Set[pathlib.Path] = set()

    def _create_app_container(self):
        self.create_app_container_calls += 1
        return 0xDEAD

    def _derive_capabilities(self, names: List[str]):
        self.derive_capabilities_calls.append(list(names))
        return [0xCAFE + i for i in range(len(names))]

    def _grant(self, path: pathlib.Path, sid) -> None:
        if path in self.fail_grant_for:
            raise OSError(f"synthetic grant failure for {path}")
        self.grant_calls.append((path, sid))

    def _revoke(self, path: pathlib.Path, sid) -> None:
        self.revoke_calls.append((path, sid))

    def _delete_profile(self) -> None:
        self.delete_profile_calls += 1


@pytest.fixture(autouse=True)
def restore_process_globals():
    """Applying a sandbox mutates process-wide state in two modules.

    A test that fails between apply() and cleanup() would otherwise leak an installed spawner
    into every later test in the session, so snapshot and restore both unconditionally.
    """
    spawner = executable._spawner
    active = spack.sandbox.active_sandbox()
    yield
    executable.set_process_spawner(spawner)
    spack.sandbox._set_active_sandbox(active)


def test_rule_building_merges_overlapping_paths(tmp_path: pathlib.Path):
    sandbox = SpyWindowsAppContainerSandbox()

    d = tmp_path / "dir"
    d.mkdir()
    f = d / "file"
    f.touch()

    sandbox.allow_read(d)
    sandbox.allow_write(f)
    sandbox.allow_read(f)  # overlapping: merges with the write mask already set

    assert sandbox.path_rules[d.resolve()] == sandbox.read_mask
    merged = sandbox.path_rules[f.resolve()]
    assert merged & sandbox.write_mask
    assert merged & sandbox.read_mask


def test_reserved_device_names_are_not_granted():
    """os.devnull is requested by every build but has no DACL to attach an ACE to."""
    sandbox = SpyWindowsAppContainerSandbox()
    sandbox.allow_write(os.devnull)
    assert sandbox.path_rules == {}


def test_apply_grants_paths_and_registers_active_sandbox(tmp_path: pathlib.Path):
    sandbox = SpyWindowsAppContainerSandbox()
    d = tmp_path / "dir"
    d.mkdir()
    sandbox.allow_write(d)

    assert spack.sandbox.active_sandbox() is None
    sandbox.apply(block_network=False)
    try:
        assert spack.sandbox.active_sandbox() is sandbox
        assert sandbox.create_app_container_calls == 1
        assert sandbox.grant_calls == [(d.resolve(), sandbox.sid)]
    finally:
        sandbox.cleanup()
    assert spack.sandbox.active_sandbox() is None


def test_network_capability_mapping():
    """allow_network requests the configured capabilities; blocking requests none at all.

    An AppContainer is offline until a capability is granted, so blocking is the *absence* of
    a request rather than an added restriction; getting this backwards would silently leave
    builds online.
    """
    allow_net = SpyWindowsAppContainerSandbox()
    allow_net.apply(block_network=False)
    try:
        assert allow_net.derive_capabilities_calls == [spack.sandbox.NETWORK_CAPABILITIES]
    finally:
        allow_net.cleanup()

    block_net = SpyWindowsAppContainerSandbox()
    block_net.apply(block_network=True)
    try:
        assert block_net.derive_capabilities_calls == [[]]
        assert block_net.capabilities == []
    finally:
        block_net.cleanup()


def test_cleanup_is_idempotent(tmp_path: pathlib.Path):
    sandbox = SpyWindowsAppContainerSandbox()
    d = tmp_path / "dir"
    d.mkdir()
    sandbox.allow_write(d)
    sandbox.apply(block_network=True)

    sandbox.cleanup()
    sandbox.cleanup()  # must be a no-op the second time

    assert len(sandbox.revoke_calls) == 1
    assert sandbox.delete_profile_calls == 1
    assert spack.sandbox.active_sandbox() is None


def test_partial_grant_failure_does_not_raise(tmp_path: pathlib.Path):
    sandbox = SpyWindowsAppContainerSandbox()
    ok_dir = tmp_path / "ok"
    ok_dir.mkdir()
    bad_dir = tmp_path / "bad"
    bad_dir.mkdir()
    sandbox.allow_write(ok_dir)
    sandbox.allow_write(bad_dir)
    sandbox.fail_grant_for.add(bad_dir.resolve())

    with pytest.warns(UserWarning, match="Cannot allow sandbox access"):
        sandbox.apply(block_network=True)

    try:
        granted = {p for p, _ in sandbox.grant_calls}
        assert ok_dir.resolve() in granted
        assert bad_dir.resolve() not in granted
        assert bad_dir.resolve() not in sandbox._granted_paths
    finally:
        sandbox.cleanup()

    revoked = {p for p, _ in sandbox.revoke_calls}
    assert bad_dir.resolve() not in revoked


def test_apply_installs_spawner_and_cleanup_restores_it():
    """The sandbox takes over process creation only for as long as it is applied.

    Leaving the spawner installed past cleanup() would send later commands into a container
    whose grants have already been revoked and whose profile is gone.
    """
    default_spawner = executable._spawner

    sandbox = SpyWindowsAppContainerSandbox()
    sandbox.apply(block_network=True)
    try:
        # Bound methods compare equal but are not identical, so `is` would never hold here.
        assert executable._spawner == sandbox._spawn_in_container
    finally:
        sandbox.cleanup()

    assert executable._spawner is default_spawner


def test_executable_passes_resolved_command_and_environment_to_spawner(monkeypatch):
    """Executable routes through the seam, handing over the fully assembled command and env."""
    calls = []

    class FakeProc:
        returncode = 0

        def communicate(self, timeout=None):
            return b"", b""

    def fake_spawner(cmd, *, env, stdin, stdout, stderr):
        calls.append((cmd, env))
        return FakeProc()

    monkeypatch.setattr(executable, "_spawner", fake_spawner)

    exe = Executable("cmd")
    exe.add_default_arg("/c")
    exe.add_default_env("FROM_DEFAULT", "default-value")
    exe("echo hi", extra_env={"FROM_EXTRA": "extra-value"})

    [(cmd, env)] = calls
    assert cmd == ["cmd", "/c", "echo hi"]
    # Default and per-call environment modifications are resolved before the spawner sees them,
    # rather than being left for the child to inherit from os.environ.
    assert env["FROM_DEFAULT"] == "default-value"
    assert env["FROM_EXTRA"] == "extra-value"


#
# End-to-end tests against the real Win32 APIs.
#

CMD = "C:\\Windows\\System32\\cmd.exe"
POWERSHELL = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"

#: Prints NET-OK if an outbound TCP connection succeeds, NET-BLOCKED if the OS refuses it.
_CONNECT_SNIPPET = (
    "$c = New-Object Net.Sockets.TcpClient; "
    "try { $c.Connect('example.com', 80); 'NET-OK' } catch { 'NET-BLOCKED' }"
)


@pytest.fixture
def live_sandbox(tmp_path: pathlib.Path):
    """A real AppContainer sandbox with `tmp_path/allowed` writable and nothing else.

    Yields ``(sandbox, allowed_dir, denied_dir)`` un-applied, so each test can choose whether
    the network is blocked.
    """
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    denied = tmp_path / "denied"
    denied.mkdir()
    (allowed / "readable.txt").write_text("ALLOWED-CONTENT", encoding="utf-8")
    (denied / "secret.txt").write_text("DENIED-CONTENT", encoding="utf-8")

    sandbox = spack.sandbox.WindowsAppContainerSandbox()
    sandbox.allow_write(allowed)
    try:
        yield sandbox, allowed, denied
    finally:
        sandbox.cleanup()
    assert spack.sandbox.active_sandbox() is None


def _run(exe: str, *args: str) -> Tuple[int, str]:
    cmd = Executable(exe)
    out = cmd(*args, output=str, error=str, fail_on_error=False)
    return cmd.returncode, out


def test_live_sandbox_enforces_filesystem_policy(live_sandbox):
    """The OS must actually refuse reads and writes outside the granted paths."""
    sandbox, allowed, denied = live_sandbox
    sandbox.apply(block_network=True)

    rc, out = _run(CMD, "/c", "type", str(allowed / "readable.txt"))
    assert rc == 0 and "ALLOWED-CONTENT" in out

    rc, out = _run(CMD, "/c", "type", str(denied / "secret.txt"))
    assert rc != 0, "reading outside the sandbox policy must fail"
    assert "DENIED-CONTENT" not in out

    rc, _ = _run(CMD, "/c", f"echo written > {allowed / 'new.txt'}")
    assert rc == 0 and (allowed / "new.txt").exists()

    rc, _ = _run(CMD, "/c", f"echo written > {denied / 'new.txt'}")
    assert rc != 0, "writing outside the sandbox policy must fail"
    assert not (denied / "new.txt").exists()


def test_live_sandbox_restores_the_dacl_it_found(live_sandbox):
    """Granting access edits real on-disk ACLs, so cleanup must put them back.

    Compares ACE lists rather than raw SDDL: writing a DACL at all makes Windows set the
    SE_DACL_AUTO_INHERITED (``AI``) control flag, which happens even for a no-op write and
    conveys no access.
    """
    sandbox, allowed, _ = live_sandbox
    nested = allowed / "child" / "nested.txt"
    nested.parent.mkdir()
    nested.write_text("nested", encoding="utf-8")
    targets = [allowed, nested.parent, nested]

    def ace_lists():
        return [
            [str(a) for a in win_acl.SecurityDescriptor.from_file(str(p)).dacl] for p in targets
        ]

    before = ace_lists()
    sandbox.apply(block_network=True)
    granted = ace_lists()
    sandbox.cleanup()

    # The grant has to actually reach the root and be inherited by pre-existing children,
    # or the comparison after cleanup would pass vacuously.
    assert granted != before
    assert all(len(g) == len(b) + 1 for g, b in zip(granted, before))

    assert ace_lists() == before


def test_live_sandbox_blocks_network(live_sandbox):
    sandbox, _, _ = live_sandbox
    sandbox.apply(block_network=True)
    assert sandbox.capabilities == []

    # A zero-capability AppContainer is the case that regressed before: CreateProcessW rejects
    # a non-NULL SECURITY_CAPABILITIES.Capabilities with CapabilityCount == 0, which failed
    # every spawn rather than merely blocking the network.
    rc, out = _run(POWERSHELL, "-NoProfile", "-Command", _CONNECT_SNIPPET)
    assert rc == 0, f"the build tool itself must still launch: {out}"
    assert "NET-OK" not in out


def test_live_sandbox_allows_network_when_configured(live_sandbox):
    sandbox, _, _ = live_sandbox
    sandbox.apply(block_network=False)

    rc, out = _run(POWERSHELL, "-NoProfile", "-Command", _CONNECT_SNIPPET)
    assert rc == 0
    if "NET-OK" not in out:
        pytest.skip(f"host has no outbound network access: {out.strip()}")


def test_live_sandbox_preserves_parent_std_handles(live_sandbox, capfd):
    """Spawning must not close the parent's own stdio.

    Redirecting only some streams used to hand the child the parent's real std handles and
    then close them as if they were ours, silently destroying Spack's own console output.
    """
    sandbox, allowed, _ = live_sandbox
    sandbox.apply(block_network=True)

    # output is a pipe, error is left inherited: the mixed case that triggered the bug.
    Executable(CMD)("/c", "type", str(allowed / "readable.txt"), output=str)

    print("PARENT-STDOUT-ALIVE")
    sys.stderr.write("PARENT-STDERR-ALIVE\n")
    captured = capfd.readouterr()
    assert "PARENT-STDOUT-ALIVE" in captured.out
    assert "PARENT-STDERR-ALIVE" in captured.err
