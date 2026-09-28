# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Unit tests for the Linux installer build sandbox."""

import errno
import pathlib
import tempfile
from types import SimpleNamespace
from typing import List, Tuple

import pytest

import spack.concretize
import spack.error
import spack.installer.build as build
import spack.sandbox
import spack.sandbox_base
import spack.sandbox_namespaces as ns
import spack.store

pytestmark = [
    pytest.mark.skipif(
        not spack.sandbox_base.installer_sandbox_supported(),
        reason="the installer sandbox is not supported on this platform",
    ),
    # CPython 3.12+ warns when fork() runs while another thread is alive. The probe only
    # forks a child that unshares namespaces and exits; os.fork is not scheduled for removal.
    pytest.mark.filterwarnings("ignore:This process .* is multi-threaded:DeprecationWarning"),
]


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


@pytest.mark.parametrize(
    "entrypoint", ["_prepare_namespace_sandbox_before_threads", "_enable_sandbox"]
)
def test_sandbox_creation_error_is_install_error(monkeypatch, entrypoint):

    monkeypatch.setattr(ns, "freeze_namespace_sandbox_capability", lambda: None)

    def unavailable():
        raise spack.sandbox.SandboxError("backend unavailable")

    monkeypatch.setattr(spack.sandbox, "get_sandbox", unavailable)
    with pytest.raises(
        spack.error.InstallError, match="Cannot enable build sandbox: backend unavailable"
    ):
        getattr(build, entrypoint)({"enable": True}, None, "unused-stage")


@pytest.mark.parametrize("prepared, dropped", [(False, True), (True, False)])
def test_namespace_preparation_reports_failure(monkeypatch, prepared, dropped, capsys):

    class FailedNamespace(ns.NamespaceSandbox):
        filesystem_policy_active = False

        def __init__(self):
            pass

        def prepare_mount_tree(self, paths, stage_path):
            assert paths == ["/usr/share/aclocal"]
            assert stage_path == "unused-stage"
            return prepared

        def drop_mount_authority(self):
            assert prepared
            return dropped

    sandbox = FailedNamespace()
    monkeypatch.setattr(ns, "freeze_namespace_sandbox_capability", lambda: None)
    monkeypatch.setattr(spack.sandbox, "get_sandbox", lambda: sandbox)
    spec = type("Spec", (), {"traverse": lambda self, **kwargs: []})()
    if prepared:
        with pytest.raises(
            spack.error.InstallError, match="Cannot drop namespace mount authority"
        ):
            build._enable_sandbox({"enable": True, "allow_network": True}, spec, "unused-stage")
    else:
        assert (
            build._prepare_namespace_sandbox_before_threads({"enable": True}, spec, "unused-stage")
            is sandbox
        )
        assert "kernel namespaces unavailable" in capsys.readouterr().err


def test_worker_setup_reports_error_when_log_cannot_be_written(monkeypatch, tmp_path, capsys):

    class StateStream:
        closed = False

        def close(self):
            self.closed = True

    stream = StateStream()
    monkeypatch.setattr(build, "make_state_stream", lambda state: stream)

    def fail_setup(*args, **kwargs):
        raise spack.sandbox.SandboxError("namespace setup failed")

    monkeypatch.setattr(build, "_start_tee_after_namespace", fail_setup)
    with pytest.raises(SystemExit) as exited:
        build._start_worker_output({}, None, None, None, None, str(tmp_path / "missing" / "log"))
    assert exited.value.code == build.ExitCode.BUILD_ERROR
    assert stream.closed
    assert "namespace setup failed" in capsys.readouterr().err


def test_enable_sandbox_paths(
    config, mock_packages, monkeypatch, temporary_store: spack.store.Store, tmp_path: pathlib.Path
):
    """Test that _enable_sandbox in the installer calls allow_read/allow_write correctly."""
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

    custom_read = tmp_path / "custom_read"
    custom_read.mkdir()

    temporary_store.install_sbang()
    sbang_file = pathlib.Path(temporary_store.unpadded_root) / "bin" / "sbang"
    upstream_root = tmp_path / "upstream"
    upstream_sbang = upstream_root / "bin" / "sbang"
    upstream_sbang.parent.mkdir(parents=True)
    upstream_sbang.write_text("upstream sbang", encoding="utf-8")
    upstream = type("Upstream", (), {"root": str(upstream_root)})()
    monkeypatch.setattr(temporary_store, "upstreams", [upstream])

    config = {
        "enable": True,
        "allow_read": [str(custom_read)],
        "allow_write": [str(custom_write)],
        "allow_network": True,
    }

    build._enable_sandbox(config, spec, str(stage_path))

    allow_read_resolved = [c[1] for c in mock_sandbox.read_calls]
    for dep in spec.traverse(root=False):
        assert pathlib.Path(dep.prefix).resolve() in allow_read_resolved

    assert custom_read.resolve() in allow_read_resolved
    assert upstream_sbang.resolve() in allow_read_resolved

    assert sbang_file.resolve() in allow_read_resolved

    allow_write_resolved = [c[1] for c in mock_sandbox.write_calls]
    assert stage_path.resolve() in allow_write_resolved
    assert pathlib.Path(spec.prefix).resolve() in allow_write_resolved
    assert custom_write.resolve() in allow_write_resolved
    assert pathlib.Path(tempfile.gettempdir()).resolve() in allow_write_resolved

    assert mock_sandbox.apply_calls == [False]


class MockNamespaceSandbox(ns.NamespaceSandbox):
    """NamespaceSandbox that records mount-tree preparation instead of mounting."""

    def __init__(self):
        super().__init__()
        self.prepare_mount_tree_calls = []
        self.apply_calls: List[bool] = []

    def _allow_read(self, original: pathlib.Path, resolved: pathlib.Path):
        pass

    def _allow_write(self, original: pathlib.Path, resolved: pathlib.Path):
        pass

    def prepare_mount_tree(self, hidden_dirs, stage_path):
        self.prepare_mount_tree_calls.append((list(hidden_dirs), stage_path))
        return True

    def drop_mount_authority(self):
        return True

    def apply(self, block_network=False):
        self.apply_calls.append(block_network)


def test_enable_sandbox_prepares_namespace_mount_tree(
    config, mock_packages, monkeypatch, temporary_store: spack.store.Store, tmp_path: pathlib.Path
):
    """The namespace backend hides host directories before Landlock is applied.

    ``_enable_sandbox`` must call ``prepare_mount_tree`` on the selected
    NamespaceSandbox with the default hidden directories, and the returned
    Landlock-visible tree is what ``apply`` then confines.
    """
    mock_sandbox = MockNamespaceSandbox()
    monkeypatch.setattr(spack.sandbox, "get_sandbox", lambda: mock_sandbox)

    spec = spack.concretize.concretize_one("dependent-install")
    pathlib.Path(spec.prefix).mkdir(parents=True, exist_ok=True)
    for dep in spec.traverse(root=False):
        pathlib.Path(dep.prefix).mkdir(parents=True, exist_ok=True)

    stage_path = tmp_path / "stage"
    stage_path.mkdir()

    build._enable_sandbox({"enable": True, "allow_network": True}, spec, str(stage_path))

    assert mock_sandbox.prepare_mount_tree_calls == [(["/usr/share/aclocal"], str(stage_path))]
    assert mock_sandbox.apply_calls == [False]


def test_default_hide_as_empty_dirs_skips_external_autoconf():
    """An external autoconf keeps access to its own host macro directory."""

    def fake_spec(dependencies):
        spec = SimpleNamespace()
        spec.traverse = lambda root=True: iter(dependencies)
        return spec

    external = SimpleNamespace(name="autoconf", external=True)
    assert build.default_hide_as_empty_dirs(fake_spec([external])) == []

    not_external = SimpleNamespace(name="autoconf", external=False)
    assert build.default_hide_as_empty_dirs(fake_spec([not_external])) == ["/usr/share/aclocal"]


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


@pytest.mark.parametrize("external", [False, True])
def test_default_mask_does_not_hide_tools(external):
    spec = SimpleNamespace(
        traverse=lambda **kw: [SimpleNamespace(name="autoconf", external=external)]
    )
    assert build.default_hide_as_empty_dirs(spec) == ([] if external else ["/usr/share/aclocal"])
