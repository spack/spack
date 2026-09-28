# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Platform-agnostic unit tests for the abstract Sandbox interface and installer wiring."""

import copy
import io
import os
import pathlib
import sys
import tempfile
from typing import Any, List, Tuple, cast

import pytest

import spack.concretize
import spack.error
import spack.paths
import spack.repo
import spack.sandbox
import spack.sandbox_namespaces
import spack.store
import spack.util.spack_yaml as syaml
from spack.installer.build import _enable_sandbox


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


def _write_yaml(path: pathlib.Path, data: dict) -> None:
    stream = io.StringIO()
    syaml.dump(data, stream)
    path.write_text(stream.getvalue(), encoding="utf-8")


def test_namespace_policy_data_is_loaded_from_yaml():
    if sys.platform != "linux":
        pytest.skip("Linux namespace filesystem policy")

    from spack.installer import build

    policy = build._load_sandbox_policy(build.SANDBOX_POLICY_PATH)
    header_policy = build._load_linux_header_policy(build.LINUX_HEADER_POLICY_PATH)

    assert "commands" not in policy
    assert policy["hidden_roots"]
    assert policy["replacement_roots"] == ["/tmp", "/var/tmp"]
    assert "/dev/urandom" in policy["device_nodes"]
    assert "tar" in policy["stage_programs"]
    assert header_policy["version"] == 1
    assert header_policy["system_include_root"] == "/usr/include"


@pytest.mark.parametrize(
    "mutation, expected_key",
    [
        (lambda policy: policy.update(version=2), "version"),
        (lambda policy: policy.update(hidden_roots="/usr/bin"), "hidden_roots"),
        (
            lambda policy: policy["compiler_driver_aliases"].update(cxx="g++"),
            "compiler_driver_aliases",
        ),
    ],
)
def test_namespace_policy_rejects_malformed_data(tmp_path: pathlib.Path, mutation, expected_key):
    if sys.platform != "linux":
        pytest.skip("Linux namespace filesystem policy")

    from spack.installer import build

    policy = copy.deepcopy(build._load_sandbox_policy(build.SANDBOX_POLICY_PATH))
    mutation(policy)
    policy_path = tmp_path / "sandbox.yaml"
    _write_yaml(policy_path, policy)

    with pytest.raises(spack.error.InstallError, match=str(policy_path)) as error:
        build._load_sandbox_policy(str(policy_path))
    assert expected_key in str(error.value)


@pytest.mark.parametrize("unsafe_path", ["../stdio.h", "/etc/passwd", "foo\\..\\bar.h"])
def test_linux_header_policy_rejects_unsafe_relative_paths(
    tmp_path: pathlib.Path, unsafe_path: str
):
    if sys.platform != "linux":
        pytest.skip("Linux namespace filesystem policy")

    from spack.installer import build

    policy = copy.deepcopy(build._load_linux_header_policy(build.LINUX_HEADER_POLICY_PATH))
    policy["glibc"]["files"][0] = unsafe_path
    policy_path = tmp_path / "linux-header-policy.yaml"
    _write_yaml(policy_path, policy)

    with pytest.raises(spack.error.InstallError, match=str(policy_path)) as error:
        build._load_linux_header_policy(str(policy_path))
    assert "glibc.files" in str(error.value)


def test_allow_read_reports_both_the_requested_and_resolved_path(tmp_path: pathlib.Path):
    """Backends need the resolved path to apply a rule, and the original to report on it.

    Rules are keyed by resolved path so that two names for one directory collapse to a single
    rule instead of racing each other.
    """
    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "link"
    try:
        link.symlink_to(target)
    except OSError as e:
        # Windows only permits this under Developer Mode or with elevation.
        pytest.skip(f"cannot create symlinks on this host: {e}")

    sandbox = MockSandbox()
    sandbox.allow_read(link)

    assert sandbox.read_calls == [(link.absolute(), target.resolve())]


@pytest.mark.parametrize(
    "entrypoint", ["_prepare_namespace_sandbox_before_threads", "_enable_sandbox"]
)
def test_sandbox_creation_error_is_install_error(monkeypatch, entrypoint):
    import spack.error
    import spack.installer.build as build

    monkeypatch.setattr(
        spack.sandbox_namespaces, "freeze_namespace_sandbox_capability", lambda: None
    )

    def unavailable():
        raise spack.sandbox.SandboxError("backend unavailable")

    monkeypatch.setattr(spack.sandbox, "get_sandbox", unavailable)
    with pytest.raises(
        spack.error.InstallError, match="Cannot enable build sandbox: backend unavailable"
    ):
        getattr(build, entrypoint)({"enable": True}, None, "unused-stage")


@pytest.mark.parametrize("prepared, dropped", [(False, True), (True, False)])
def test_namespace_preparation_reports_failure(monkeypatch, prepared, dropped, capsys):
    import spack.error
    import spack.installer.build as build

    class FailedNamespace(spack.sandbox_namespaces.NamespaceSandbox):
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
    monkeypatch.setattr(
        spack.sandbox_namespaces, "freeze_namespace_sandbox_capability", lambda: None
    )
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
    import spack.installer.build as build

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

    # sbang (a shebang-length workaround) is a POSIX-only concept; install_sbang() is a no-op
    # on Windows, so there is nothing to grant read access to on that platform.
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

    _enable_sandbox(config, spec, str(stage_path))

    allow_read_resolved = [c[1] for c in mock_sandbox.read_calls]
    for dep in spec.traverse(root=False):
        assert pathlib.Path(dep.prefix).resolve() in allow_read_resolved

    assert custom_read.resolve() in allow_read_resolved
    assert upstream_sbang.resolve() in allow_read_resolved

    # Verify sbang read (sbang doesn't exist on Windows; see comment above)
    if sys.platform != "win32":
        assert sbang_file.resolve() in allow_read_resolved

    allow_write_resolved = [c[1] for c in mock_sandbox.write_calls]
    assert stage_path.resolve() in allow_write_resolved
    assert pathlib.Path(spec.prefix).resolve() in allow_write_resolved
    assert custom_write.resolve() in allow_write_resolved
    assert pathlib.Path(tempfile.gettempdir()).resolve() in allow_write_resolved

    assert mock_sandbox.apply_calls == [False]


class MockNamespaceSandbox(spack.sandbox_namespaces.NamespaceSandbox):
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

    _enable_sandbox({"enable": True, "allow_network": True}, spec, str(stage_path))

    assert mock_sandbox.prepare_mount_tree_calls == [(["/usr/share/aclocal"], str(stage_path))]
    assert mock_sandbox.apply_calls == [False]


def test_default_hide_as_empty_dirs_skips_external_autoconf():
    """An external autoconf keeps access to its own host macro directory."""
    import types

    from spack.installer.build import default_hide_as_empty_dirs

    def fake_spec(dependencies):
        spec = types.SimpleNamespace()
        spec.traverse = lambda root=True: iter(dependencies)
        return cast(Any, spec)

    external = types.SimpleNamespace(name="autoconf", external=True)
    assert default_hide_as_empty_dirs(fake_spec([external])) == []

    not_external = types.SimpleNamespace(name="autoconf", external=False)
    assert default_hide_as_empty_dirs(fake_spec([not_external])) == ["/usr/share/aclocal"]


def test_namespace_filesystem_policy_from_installer_inputs(monkeypatch, tmp_path: pathlib.Path):
    if sys.platform != "linux":
        pytest.skip("Linux namespace filesystem policy")

    from types import SimpleNamespace

    from spack.installer.build import namespace_filesystem_policy_from_inputs

    dependency_prefix = tmp_path / "dependency"
    dependency_prefix.mkdir()
    external_prefix = tmp_path / "external"
    external_prefix.mkdir()
    install_prefix = tmp_path / "prefix"
    install_prefix.mkdir()
    stage_path = tmp_path / "stage"
    stage_path.mkdir()
    temporary_path = tmp_path / "temporary"
    temporary_path.mkdir()
    custom_read = tmp_path / "custom-read"
    custom_read.mkdir()
    custom_write = tmp_path / "custom-write"
    custom_write.mkdir()
    store_root = tmp_path / "store"
    sbang = store_root / "bin" / "sbang"
    sbang.parent.mkdir(parents=True)
    sbang.touch()

    dependencies = [
        SimpleNamespace(name="dependency", external=False, prefix=dependency_prefix),
        SimpleNamespace(name="external", external=True, prefix=external_prefix),
    ]
    spec = cast(
        Any, SimpleNamespace(prefix=install_prefix, traverse=lambda root=True: iter(dependencies))
    )
    monkeypatch.setattr(spack.store.STORE, "unpadded_root", str(store_root))
    monkeypatch.setattr(spack.store.STORE, "upstreams", None)
    monkeypatch.setattr(tempfile, "gettempdir", lambda: str(temporary_path))

    policy = namespace_filesystem_policy_from_inputs(
        {"allow_read": [str(custom_read)], "allow_write": [str(custom_write)]},
        spec,
        str(stage_path),
    )

    read_only_targets = {pathlib.Path(mount.target) for mount in policy.read_only_mounts}
    assert read_only_targets == {
        dependency_prefix.resolve(),
        custom_read.resolve(),
        sbang.resolve(),
    }
    read_write_targets = {pathlib.Path(mount.target) for mount in policy.read_write_mounts}
    assert read_write_targets == {
        stage_path.resolve(),
        install_prefix.resolve(),
        temporary_path.resolve(),
        custom_write.resolve(),
        pathlib.Path(os.devnull).resolve(),
    }
    assert external_prefix.resolve() not in read_only_targets


def test_complete_namespace_policy_from_installer_inputs(monkeypatch, tmp_path: pathlib.Path):
    if sys.platform != "linux":
        pytest.skip("Linux namespace filesystem policy")

    from types import SimpleNamespace

    from spack.installer.build import (
        NamespacePolicyInputPaths,
        namespace_filesystem_policy_and_plan_from_inputs,
    )

    host = tmp_path / "host"

    def directory(path):
        path.mkdir(parents=True)
        return path

    def file(path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        return path

    compiler = file(host / "usr" / "bin" / "cc")
    tool = file(host / "usr" / "bin" / "make")
    headers = directory(host / "usr" / "include")
    compiler_headers = directory(headers / "compiler")
    runtime = directory(host / "usr" / "lib")
    repository_python_path = directory(host / "repos-python")
    repository_composition_root = directory(repository_python_path / "spack_repo")
    repository = directory(repository_composition_root / "builtin")
    hidden_host_state = directory(host / "home")
    dependency_prefix = directory(host / "store" / "dependency")
    external_prefix = directory(host / "external")
    install_prefix = directory(host / "store" / "install")
    stage_path = directory(host / "build" / "stage")
    temporary_path = directory(host / "build" / "tmp")
    mount_plan_stage = directory(tmp_path / "mount-plan")
    sbang = file(host / "store" / "bin" / "sbang")

    spack_prefix = host / "spack"
    spack_source_paths = (
        directory(spack_prefix / "bin"),
        directory(spack_prefix / "lib"),
        directory(spack_prefix / "share" / "spack"),
        directory(spack_prefix / "etc" / "spack"),
    )
    monkeypatch.setattr(spack.paths, "bin_path", str(spack_source_paths[0]))
    monkeypatch.setattr(spack.paths, "lib_path", str(spack_source_paths[1]))
    monkeypatch.setattr(spack.paths, "share_path", str(spack_source_paths[2]))
    monkeypatch.setattr(spack.paths, "etc_path", str(spack_source_paths[3]))
    monkeypatch.setattr(
        spack.repo,
        "PATH",
        SimpleNamespace(
            repos=[SimpleNamespace(root=str(repository), python_path=str(repository_python_path))]
        ),
    )
    monkeypatch.setattr(spack.store.STORE, "unpadded_root", str(host / "store"))
    monkeypatch.setattr(spack.store.STORE, "upstreams", None)

    dependencies = (
        SimpleNamespace(name="dependency", external=False, prefix=dependency_prefix),
        SimpleNamespace(name="external", external=True, prefix=external_prefix),
    )
    spec = cast(
        Any, SimpleNamespace(prefix=install_prefix, traverse=lambda root=True: iter(dependencies))
    )
    selected_paths = NamespacePolicyInputPaths(
        hidden_roots=(str(hidden_host_state),),
        compiler_paths=(str(compiler),),
        tool_paths=(str(tool),),
        header_paths=(str(headers), str(compiler_headers)),
        runtime_paths=(str(runtime),),
        temporary_paths=(str(temporary_path),),
    )

    policy, plan = namespace_filesystem_policy_and_plan_from_inputs(
        {}, spec, str(stage_path), str(mount_plan_stage), selected_paths
    )

    read_only_targets = {pathlib.Path(mount.target) for mount in policy.read_only_mounts}
    assert read_only_targets == {
        compiler.resolve(),
        tool.resolve(),
        headers.resolve(),
        runtime.resolve(),
        repository.resolve(),
        dependency_prefix.resolve(),
        sbang.resolve(),
        *(path.resolve() for path in spack_source_paths),
    }
    read_write_targets = {pathlib.Path(mount.target) for mount in policy.read_write_mounts}
    assert read_write_targets == {
        stage_path.resolve(),
        install_prefix.resolve(),
        temporary_path.resolve(),
        pathlib.Path(os.devnull).resolve(),
    }
    assert external_prefix.resolve() not in read_only_targets
    assert compiler_headers.resolve() not in read_only_targets
    assert set(policy.hidden_roots) == {
        str(pathlib.Path(os.devnull).resolve().parent),
        str((host / "build").resolve()),
        str(hidden_host_state.resolve()),
        str(repository_composition_root.resolve()),
        str(spack_prefix.resolve()),
        str((host / "store").resolve()),
        str((host / "usr").resolve()),
    }
    assert all(
        pathlib.Path(root) != mount_plan_stage.resolve()
        and pathlib.Path(root) not in mount_plan_stage.resolve().parents
        for root in policy.hidden_roots
    )
    assert plan.stage_path == str(mount_plan_stage.resolve())
    assert {mount.target for mount in plan.restoration_mounts} == {
        str(path) for path in read_only_targets | read_write_targets
    }


def test_complete_namespace_policy_rejects_missing_selected_path(
    monkeypatch, tmp_path: pathlib.Path
):
    if sys.platform != "linux":
        pytest.skip("Linux namespace filesystem policy")

    from types import SimpleNamespace

    from spack.installer.build import (
        NamespacePolicyInputPaths,
        namespace_filesystem_policy_and_plan_from_inputs,
    )

    existing = tmp_path / "existing"
    existing.mkdir()
    missing = tmp_path / "missing-compiler"
    spec = cast(Any, SimpleNamespace(prefix=existing, traverse=lambda root=True: iter(())))
    selected_paths = NamespacePolicyInputPaths(
        hidden_roots=(str(existing),),
        compiler_paths=(str(missing),),
        tool_paths=(str(existing),),
        header_paths=(str(existing),),
        runtime_paths=(str(existing),),
        temporary_paths=(str(existing),),
    )
    monkeypatch.setattr(
        spack.repo,
        "PATH",
        SimpleNamespace(repos=[SimpleNamespace(root=str(existing), python_path=None)]),
    )
    monkeypatch.setattr(spack.paths, "bin_path", str(existing))
    monkeypatch.setattr(spack.paths, "lib_path", str(existing))
    monkeypatch.setattr(spack.paths, "share_path", str(existing))
    monkeypatch.setattr(spack.paths, "etc_path", str(existing))
    sbang = tmp_path / "store" / "bin" / "sbang"
    sbang.parent.mkdir(parents=True)
    sbang.touch()
    monkeypatch.setattr(spack.store.STORE, "unpadded_root", str(tmp_path / "store"))
    monkeypatch.setattr(spack.store.STORE, "upstreams", None)

    with pytest.raises(spack.sandbox_namespaces.NamespaceSetupError, match=str(missing)):
        namespace_filesystem_policy_and_plan_from_inputs(
            {}, spec, str(existing), str(tmp_path / "mount-plan"), selected_paths
        )

    compiler = tmp_path / "compiler"
    compiler.touch()
    compiler_link = tmp_path / "compiler-link"
    compiler_link.symlink_to(compiler)
    with pytest.raises(
        spack.sandbox_namespaces.NamespaceSetupError, match="required path is not canonical"
    ):
        namespace_filesystem_policy_and_plan_from_inputs(
            {},
            spec,
            str(existing),
            str(tmp_path / "mount-plan"),
            selected_paths._replace(compiler_paths=(str(compiler_link),)),
        )

    with pytest.raises(
        spack.sandbox_namespaces.NamespaceSetupError, match="without hiding the filesystem root"
    ):
        namespace_filesystem_policy_and_plan_from_inputs(
            {},
            spec,
            str(existing),
            str(tmp_path / "mount-plan"),
            selected_paths._replace(
                compiler_paths=(str(compiler),), temporary_paths=(tempfile.gettempdir(),)
            ),
        )
