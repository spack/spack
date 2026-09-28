# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Namespace unit tests never modify the test runner's namespaces or /proc."""

import errno
import io
import os
import subprocess
import sys
from types import SimpleNamespace

import pytest

import spack.error
import spack.installer.build as build
import spack.sandbox
import spack.sandbox_namespaces as ns
import spack.util.tty


@pytest.fixture(autouse=True)
def reset_namespace_probe_result(monkeypatch):
    monkeypatch.setattr(ns, "_namespace_probe_result", None)


class FakeLibc:
    def __init__(self):
        self.unshare_calls = []
        self.mount_calls = []

    def unshare(self, flags):
        self.unshare_calls.append(flags.value)
        return 0

    def mount(self, source, target, filesystemtype, flags, data):
        self.mount_calls.append((source, target, flags.value))
        return 0

    def capset(self, header, capabilities):
        return 0


@pytest.fixture
def namespace_setup(monkeypatch):
    libc = FakeLibc()
    writes = {}

    class Mapping(io.StringIO):
        def __init__(self, path):
            super().__init__()
            self.path = path

        def close(self):
            writes[self.path] = self.getvalue()
            super().close()

    monkeypatch.setattr(ns, "_namespace_entered_pids", set())
    monkeypatch.setattr(ns.platform, "system", lambda: "Linux")
    monkeypatch.setattr(ns.os, "getuid", lambda: 1234, raising=False)
    monkeypatch.setattr(ns.os, "getgid", lambda: 5678, raising=False)
    monkeypatch.setattr(ns, "open", lambda path, *a, **kw: Mapping(path), raising=False)
    monkeypatch.setattr(
        ns, "_probe_namespace_capability", lambda libc: ns.NamespaceCapability(True, None, None)
    )
    return libc, writes


# ---------------------------------------------------------------------------
# Phase 1: capability probe and fallback
#
# Process-lifecycle cases live in test_namespace_probe_lifecycle.py.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path", ["/proc/self/setgroups", "/proc/self/uid_map", "/proc/self/gid_map"]
)
def test_namespace_mapping_write_failure(namespace_setup, monkeypatch, path):
    libc, _ = namespace_setup
    mapping_open = ns.open

    def fail_mapping(filename, *args, **kwargs):
        if filename == path:
            raise OSError(errno.EACCES, "mapping denied")
        return mapping_open(filename, *args, **kwargs)

    monkeypatch.setattr(ns, "open", fail_mapping)
    with pytest.raises(ns.NamespaceSetupError, match="mapping denied") as error:
        ns._enter_user_mount_namespace(libc)
    assert error.value.operation == "write " + path
    assert os.getpid() not in ns._namespace_entered_pids


def test_namespace_mapping_and_reentry(namespace_setup):
    libc, writes = namespace_setup
    ns._enter_user_mount_namespace(libc)
    ns._enter_user_mount_namespace(libc)
    assert libc.unshare_calls == [ns.CLONE_NEWUSER | ns.CLONE_NEWNS]
    assert writes == {
        "/proc/self/setgroups": "deny",
        "/proc/self/uid_map": "1234 1234 1",
        "/proc/self/gid_map": "5678 5678 1",
    }
    assert libc.mount_calls == [(None, b"/", ns.MS_REC | ns.MS_PRIVATE)]


def test_probe_bypasses_reentry_guard(namespace_setup):
    libc, _ = namespace_setup
    ns._namespace_entered_pids.add(os.getpid())
    ns._enter_user_mount_namespace(libc, _probe_child=True)
    assert len(libc.unshare_calls) == 1


# ---------------------------------------------------------------------------
# Phase 2: mount-tree setup
# ---------------------------------------------------------------------------


def test_empty_mount_tree_enters_namespace(namespace_setup, tmp_path):
    libc, _ = namespace_setup
    sandbox = ns.NamespaceSandbox(libc)
    assert sandbox.prepare_mount_tree([], str(tmp_path))
    assert sandbox.namespace_ready
    assert libc.unshare_calls == [ns.CLONE_NEWUSER | ns.CLONE_NEWNS]
    assert sandbox.prepare_mount_tree([], str(tmp_path))
    assert len(libc.unshare_calls) == 1


def test_prepare_reuses_active_namespace(namespace_setup, monkeypatch):
    libc, _ = namespace_setup
    ns._enter_user_mount_namespace(libc)
    monkeypatch.setattr(
        ns, "_probe_namespace_capability", lambda libc: pytest.fail("unexpected probe")
    )
    assert ns.prepare_empty_directory_masking(["/unused"], libc)
    assert len(libc.unshare_calls) == 1


def test_unavailable_namespace_is_not_ready(monkeypatch, tmp_path):
    monkeypatch.setattr(
        ns,
        "namespace_sandbox_capability",
        lambda libc=None: ns.NamespaceCapability(False, "unshare", "not permitted"),
    )
    sandbox = ns.NamespaceSandbox(FakeLibc())
    assert not sandbox.prepare_mount_tree([], str(tmp_path))
    assert not sandbox.namespace_ready


def test_mask_existing_directories(tmp_path):
    libc = FakeLibc()
    target = tmp_path / "host"
    target.mkdir()
    assert ns.hide_directories_as_empty(
        [str(target), str(tmp_path / "missing")], str(tmp_path), True, libc
    )
    assert libc.mount_calls == [
        (os.fsencode(tmp_path / "spack-empty-host-dirs/0"), os.fsencode(target), ns.MS_BIND)
    ]


def test_mount_failure_is_fatal(namespace_setup, monkeypatch, tmp_path):
    libc, _ = namespace_setup
    target = tmp_path / "host"
    target.mkdir()

    def fail(*args):
        raise OSError(errno.EPERM, "mount denied")

    # Fail after namespace entry, not the harmless availability probe.
    ns._enter_user_mount_namespace(libc)
    monkeypatch.setattr(libc, "mount", fail)
    sandbox = ns.NamespaceSandbox(libc)
    with pytest.raises(OSError, match="mount denied"):
        sandbox.prepare_mount_tree([str(target)], str(tmp_path))
    assert not sandbox.namespace_ready


@pytest.mark.parametrize("directory", [False, True])
def test_bind_mount_flags(tmp_path, directory):
    source = tmp_path / "source"
    source.mkdir() if directory else source.touch()
    libc = FakeLibc()
    sandbox = ns.NamespaceSandbox(libc)
    assert not sandbox.bind_mount(str(source))
    sandbox._namespace_ready = True
    assert sandbox.bind_mount(str(source))
    assert libc.mount_calls == [
        (os.fsencode(source), os.fsencode(source), ns.MS_BIND | (ns.MS_REC if directory else 0))
    ]


def test_dropped_mount_authority_rejects_later_mounts(namespace_setup, tmp_path):
    libc, _ = namespace_setup
    sandbox = ns.NamespaceSandbox(libc)
    assert sandbox.prepare_mount_tree([], str(tmp_path))
    assert sandbox.drop_mount_authority()
    assert sandbox.drop_mount_authority()

    source = tmp_path / "source"
    source.mkdir()
    with pytest.raises(spack.sandbox.SandboxError, match="mount authority was already dropped"):
        sandbox.bind_mount(str(source))


@pytest.mark.parametrize(
    "operation, reason",
    [
        ("write /proc/self/setgroups", "Permission denied"),
        ("unshare(CLONE_NEWUSER | CLONE_NEWNS)", "Operation not permitted"),
    ],
)
def test_live_mask_skips_unavailable_namespaces(monkeypatch, tmp_path, operation, reason):
    monkeypatch.setattr(
        ns,
        "namespace_sandbox_capability",
        lambda: ns.NamespaceCapability(False, operation, reason),
    )

    with pytest.raises(pytest.skip.Exception) as skipped:
        test_live_mask_is_private(tmp_path)

    assert str(skipped.value) == "namespace sandbox unavailable at {0}: {1}".format(
        operation, reason
    )
    assert not list(tmp_path.iterdir())


def test_live_mask_reports_setup_failure(monkeypatch, tmp_path):
    monkeypatch.setattr(
        ns, "namespace_sandbox_capability", lambda: ns.NamespaceCapability(True, None, None)
    )
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=1, stderr="mask failed"),
    )

    with pytest.raises(AssertionError, match="mask failed"):
        test_live_mask_is_private(tmp_path)


@pytest.mark.skipif(sys.platform != "linux", reason="Linux namespaces")
def test_live_mask_is_private(tmp_path):
    capability = ns.namespace_sandbox_capability()
    if not capability.available:
        pytest.skip(
            "namespace sandbox unavailable at {0}: {1}".format(
                capability.operation, capability.reason
            )
        )
    target = tmp_path / "host"
    target.mkdir()
    marker = target / "marker"
    marker.write_text("host data")
    code = """
import sys
from pathlib import Path
from spack.sandbox_namespaces import NamespaceSandbox
sandbox = NamespaceSandbox()
assert sandbox.prepare_mount_tree([sys.argv[1]], sys.argv[2])
assert list(Path(sys.argv[1]).iterdir()) == []
try:
    (Path(sys.argv[1]) / 'marker').read_text()
except FileNotFoundError:
    pass
else:
    raise AssertionError('host file remains visible')
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(target), str(tmp_path)],
        env=dict(os.environ, PYTHONPATH=os.pathsep.join(sys.path)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    assert marker.read_text() == "host data"


# ---------------------------------------------------------------------------
# Phase 3: existing Linux install-child integration
# ---------------------------------------------------------------------------


def test_landlock_delegation(tmp_path):
    calls = []
    landlock = SimpleNamespace(
        _allow_read=lambda *args: calls.append(("read", args)),
        _allow_write=lambda *args: calls.append(("write", args)),
        apply=lambda **kw: calls.append(("apply", kw)),
    )
    sandbox = ns.NamespaceSandbox(landlock_factory=lambda libc: landlock)
    sandbox.allow_read(tmp_path)
    sandbox.allow_write(tmp_path)
    sandbox.apply(block_network=True)
    assert calls == [
        ("read", (tmp_path, tmp_path)),
        ("write", (tmp_path, tmp_path)),
        ("apply", {"block_network": True}),
    ]


def test_landlock_initialization_error_is_normalized(tmp_path):
    def fail(libc):
        raise OSError(errno.ENOSYS, "Landlock unavailable")

    sandbox = ns.NamespaceSandbox(landlock_factory=fail)
    with pytest.raises(spack.sandbox.SandboxError, match="Landlock is unavailable"):
        sandbox.allow_read(tmp_path)


def test_installer_normalizes_landlock_initialization_error(monkeypatch, tmp_path):
    def fail(libc):
        raise OSError(errno.ENOSYS, "Landlock unavailable")

    sandbox = ns.NamespaceSandbox(landlock_factory=fail)
    monkeypatch.setattr(sandbox, "prepare_mount_tree", lambda hidden_dirs, stage_path: True)
    monkeypatch.setattr(sandbox, "drop_mount_authority", lambda: True)
    monkeypatch.setattr(spack.sandbox, "get_sandbox", lambda: sandbox)
    spec = SimpleNamespace(traverse=lambda **kw: [], prefix=tmp_path / "prefix")

    with pytest.raises(spack.error.InstallError, match="Cannot enable build sandbox"):
        build._enable_sandbox({"enable": True}, spec, str(tmp_path))


def test_namespace_selection_does_not_preflight_landlock(monkeypatch):
    landlock = object()
    monkeypatch.setattr(spack.sandbox.platform, "system", lambda: "Linux")
    monkeypatch.setattr(
        ns,
        "namespace_sandbox_decision",
        lambda: ns.NamespaceSandboxDecision(
            ns.NamespaceSandboxBackend.NAMESPACE, ns.NamespaceCapability(True, None, None)
        ),
    )
    monkeypatch.setattr(spack.sandbox, "LandlockSandbox", lambda: landlock)

    sandbox = spack.sandbox.get_sandbox()
    assert isinstance(sandbox, ns.NamespaceSandbox)
    assert sandbox._landlock is None


def test_namespace_selection_uses_constrained_landlock_fallback(monkeypatch):
    capability = ns.NamespaceCapability(False, "write uid_map", "operation not permitted")
    decision = ns.NamespaceSandboxDecision(ns.NamespaceSandboxBackend.LANDLOCK, capability)
    landlock = object()
    messages = []
    monkeypatch.setattr(spack.sandbox.platform, "system", lambda: "Linux")
    monkeypatch.setattr(ns, "namespace_sandbox_decision", lambda: decision)
    monkeypatch.setattr(spack.sandbox, "LandlockSandbox", lambda: landlock)
    monkeypatch.setattr(spack.util.tty, "debug", messages.append)

    assert decision.is_fallback
    assert decision.is_constrained
    assert spack.sandbox.get_sandbox() is landlock
    assert messages == [
        "Namespace sandbox unavailable during write uid_map: operation not permitted; "
        "using Landlock-only sandbox"
    ]


def test_namespace_selection_rejects_unconstrained_fallback(monkeypatch):
    capability = ns.NamespaceCapability(False, "unshare", "operation not permitted")
    decision = ns.NamespaceSandboxDecision(ns.NamespaceSandboxBackend.UNCONSTRAINED, capability)
    monkeypatch.setattr(spack.sandbox.platform, "system", lambda: "Linux")
    monkeypatch.setattr(ns, "namespace_sandbox_decision", lambda: decision)

    assert decision.is_fallback
    assert not decision.is_constrained
    with pytest.raises(
        spack.sandbox.SandboxError, match="unconstrained fallback is not permitted"
    ):
        spack.sandbox.get_sandbox()


def test_worker_prepares_namespace_before_tee(monkeypatch):
    calls = []
    sandbox = SimpleNamespace()
    monkeypatch.setattr(
        ns,
        "freeze_namespace_sandbox_capability",
        lambda: calls.append(("freeze",)) or ns.NamespaceCapability(True, None, None),
    )
    monkeypatch.setattr(
        build,
        "_prepare_namespace_sandbox_before_threads",
        lambda config, spec, stage_path: calls.append(("prepare", spec, stage_path)) or sandbox,
    )
    monkeypatch.setattr(build, "Tee", lambda *args: calls.append(("tee", args)) or object())
    spec = SimpleNamespace()

    tee, returned_sandbox = build._start_tee_after_namespace(
        {"enable": True}, "control-r", "control-w", "parent", "build.log", spec, "stage"
    )
    assert tee is not None
    assert returned_sandbox is sandbox
    assert calls == [
        ("prepare", spec, "stage"),
        ("tee", ("control-r", "control-w", "parent", "build.log")),
    ]


def test_pre_thread_setup_prepares_and_drops_namespace_authority(monkeypatch, tmp_path):
    calls = []

    class RecordingSandbox(ns.NamespaceSandbox):
        def prepare_mount_tree(self, hidden_dirs, stage_path):
            calls.append(("prepare", hidden_dirs, stage_path))
            return True

        def drop_mount_authority(self):
            calls.append(("drop mount authority",))
            return True

    sandbox = RecordingSandbox()
    spec = SimpleNamespace(traverse=lambda **kwargs: [], prefix=tmp_path / "prefix")
    monkeypatch.setattr(
        ns,
        "freeze_namespace_sandbox_capability",
        lambda: calls.append(("freeze",)) or ns.NamespaceCapability(True, None, None),
    )
    monkeypatch.setattr(spack.sandbox, "get_sandbox", lambda: sandbox)

    assert (
        build._prepare_namespace_sandbox_before_threads({"enable": True}, spec, str(tmp_path))
        is sandbox
    )
    assert calls == [
        ("freeze",),
        ("prepare", ["/usr/share/aclocal"], str(tmp_path)),
        ("drop mount authority",),
    ]


def test_pre_thread_namespace_failure_is_reported(monkeypatch, tmp_path):
    class StateStream:
        closed = False

        def close(self):
            self.closed = True

    state_stream = StateStream()
    monkeypatch.setattr(build, "make_state_stream", lambda state: state_stream)

    def fail(*args):
        raise OSError(errno.EPERM, "namespace entry denied")

    monkeypatch.setattr(build, "_start_tee_after_namespace", fail)
    log_path = tmp_path / "build.log"

    with pytest.raises(SystemExit) as error:
        build._start_worker_output({}, object(), object(), None, object(), str(log_path))
    assert error.value.code == build.ExitCode.BUILD_ERROR
    assert state_stream.closed
    assert "namespace entry denied" in log_path.read_text()


@pytest.mark.parametrize("available", [False, True])
@pytest.mark.parametrize("external, hidden_dirs", [(False, ["/usr/share/aclocal"]), (True, [])])
def test_installer_mounts_before_landlock(monkeypatch, tmp_path, available, external, hidden_dirs):
    calls = []

    class RecordingSandbox(ns.NamespaceSandbox):
        def prepare_mount_tree(self, hidden_dirs, stage_path):
            calls.append(("prepare", hidden_dirs, stage_path))
            return available

        def allow_read(self, path):
            calls.append(("read", str(path)))

        def allow_write(self, path):
            calls.append(("write", str(path)))

        def drop_mount_authority(self):
            calls.append(("drop mount authority",))
            return True

        def apply(self, block_network=False):
            calls.append(("apply", block_network))

    sandbox = RecordingSandbox()
    monkeypatch.setattr(spack.sandbox, "get_sandbox", lambda: sandbox)
    spec = SimpleNamespace(
        traverse=lambda **kw: [
            SimpleNamespace(name="autoconf", external=external, prefix=tmp_path / "autoconf")
        ],
        prefix=tmp_path / "prefix",
    )
    build._enable_sandbox({"enable": True, "allow_network": False}, spec, str(tmp_path))
    assert calls[0] == ("prepare", hidden_dirs, str(tmp_path))
    assert ("write", str(tmp_path)) in calls
    assert calls[-1] == ("apply", True)


def test_recipe_setup_cannot_add_mounts_after_pre_thread_setup(monkeypatch, tmp_path):
    calls = []

    class RecordingSandbox(ns.NamespaceSandbox):
        def prepare_mount_tree(self, hidden_dirs, stage_path):
            calls.append(("prepare", hidden_dirs, stage_path))
            return True

        def allow_read(self, path):
            calls.append(("read", str(path)))

        def allow_write(self, path):
            calls.append(("write", str(path)))

        def drop_mount_authority(self):
            calls.append(("drop mount authority",))
            return True

        def apply(self, block_network=False):
            calls.append(("apply", block_network))

    sandbox = RecordingSandbox()
    monkeypatch.setattr(spack.sandbox, "get_sandbox", lambda: sandbox)
    monkeypatch.setattr(
        build,
        "_prepare_namespace_sandbox_before_threads",
        lambda config, spec, stage_path: (
            calls.append(("prepare", stage_path)),
            calls.append(("drop mount authority",)),
            sandbox,
        )[-1],
    )
    monkeypatch.setattr(build, "Tee", lambda *args: calls.append(("tee", args)) or object())
    spec = SimpleNamespace(traverse=lambda **kw: [], prefix=tmp_path / "prefix")

    _, prepared_sandbox = build._start_tee_after_namespace(
        {"enable": True}, "control-r", "control-w", "parent", "build.log", spec, str(tmp_path)
    )
    calls.append(("recipe-controlled setup",))
    build._enable_sandbox({"enable": True}, spec, str(tmp_path), sandbox=prepared_sandbox)

    assert calls[:4] == [
        ("prepare", str(tmp_path)),
        ("drop mount authority",),
        ("tee", ("control-r", "control-w", "parent", "build.log")),
        ("recipe-controlled setup",),
    ]
    assert not any(call[0] == "prepare" for call in calls[3:])
    assert calls.count(("drop mount authority",)) == 1
    assert calls[-1] == ("apply", False)


@pytest.mark.parametrize("external", [False, True])
def test_default_mask_does_not_hide_tools(external):
    spec = SimpleNamespace(
        traverse=lambda **kw: [SimpleNamespace(name="autoconf", external=external)]
    )
    assert build.default_hide_as_empty_dirs(spec) == ([] if external else ["/usr/share/aclocal"])


# Phases 4-6 have no implementation tests yet. They cover the policy-driven
# mount tree, build-phase confinement, and concretizer-worker evaluation.
