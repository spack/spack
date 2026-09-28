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
from types import SimpleNamespace
from typing import Any, List, Tuple, cast

import pytest

import spack.compilers.config
import spack.concretize
import spack.error
import spack.paths
import spack.repo
import spack.sandbox
import spack.sandbox_namespaces
import spack.spec
import spack.store
import spack.util.ld_so_conf
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


@pytest.mark.parametrize("failure", ["allocation", "compilation"])
def test_prepare_namespace_activation_releases_scratch_on_failure(monkeypatch, tmp_path, failure):
    from spack.installer import build

    spec = SimpleNamespace(prefix=tmp_path, traverse=lambda root=False: iter(()))
    host_paths = SimpleNamespace(
        hidden_roots=(),
        replacement_roots=(),
        host_runtime_paths=(),
        device_paths=(),
        read_only_paths=(),
        writable_paths=(),
    )
    policy = spack.sandbox_namespaces.NamespaceFilesystemPolicy(())
    cleaned = []
    scratch = SimpleNamespace(path=str(tmp_path), cleanup=lambda: cleaned.append(True))
    failure_error = OSError("scratch " + failure + " failed")

    def allocate(*args, **kwargs):
        if failure == "allocation":
            raise failure_error
        return scratch

    def compile_plan(*args, **kwargs):
        raise failure_error

    monkeypatch.setattr(
        build, "select_namespace_host_device_worker_paths", lambda *args, **kwargs: host_paths
    )
    monkeypatch.setattr(build, "compiler_driver_paths", lambda spec: [])
    monkeypatch.setattr(build, "_selected_compilers", lambda spec: [])
    monkeypatch.setattr(build, "stage_tool_paths", lambda: [])
    monkeypatch.setattr(build, "install_tool_paths", lambda: [], raising=False)
    monkeypatch.setattr(build, "tool_runtime_paths", lambda *args: [])
    monkeypatch.setattr(build, "system_compiler_header_paths", lambda spec: ())
    monkeypatch.setattr(build, "compiler_alias_symlink_paths", lambda spec: [])
    monkeypatch.setattr(
        build, "namespace_selected_filesystem_policy_from_inputs", lambda *args: policy
    )
    monkeypatch.setattr(
        spack.sandbox_namespaces, "allocate_namespace_mount_plan_scratch", allocate
    )
    monkeypatch.setattr(build, "namespace_filesystem_policy_and_plan_from_inputs", compile_plan)

    with pytest.raises(OSError) as error:
        build.prepare_namespace_activation(
            {}, spec, str(tmp_path), "", (), str(tmp_path), str(tmp_path / "cache")
        )
    assert error.value is failure_error
    assert cleaned == ([] if failure == "allocation" else [True])


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
    assert policy["tmpfs_paths"] == ["/dev/shm"]
    assert policy["mount_plan_scratch_paths"] == ["/run/lock", "/var", "/opt"]
    assert policy["device_symlinks"]["/dev/fd"] == "/proc/self/fd"
    assert "tar" in policy["stage_programs"]
    assert header_policy["version"] == 1
    assert header_policy["system_include_root"] == "/usr/include"
    assert header_policy["compiler_roots"] == ["/usr/lib/gcc", "/usr/lib64/gcc"]


@pytest.mark.parametrize(
    "mutation, expected_key",
    [
        (lambda policy: policy.update(version=2), "version"),
        (lambda policy: policy.update(hidden_roots="/usr/bin"), "hidden_roots"),
        (lambda policy: policy.update(tmpfs_paths=["relative"]), "tmpfs_paths"),
        (lambda policy: policy.update(device_symlinks=[]), "device_symlinks"),
        (lambda policy: policy.update(device_symlinks={"/dev/fd": "relative"}), "device_symlinks"),
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


def test_linux_header_policy_rejects_relative_compiler_roots(tmp_path: pathlib.Path):
    from spack.installer import build

    policy = _minimal_header_policy(tmp_path)
    policy["compiler_roots"] = ["relative"]
    policy_path = tmp_path / "linux-header-policy.yaml"
    _write_yaml(policy_path, policy)

    with pytest.raises(spack.error.InstallError, match=str(policy_path)) as error:
        build._load_linux_header_policy(str(policy_path))
    assert "compiler_roots" in str(error.value)


def _minimal_header_policy(include_root: pathlib.Path, maximum_major: int = 15) -> dict:
    return {
        "version": 1,
        "system_include_root": str(include_root),
        "compiler_roots": [str(include_root / "gcc")],
        "glibc": {
            "files": ["stdio.h"],
            "directories": ["arpa"],
            "target_files": ["fpu_control.h"],
            "target_directories": ["bits", "sys"],
        },
        "linux": {"directories": ["linux"], "target_directories": ["asm"]},
        "libstdcxx": {"maximum_major_for_non_gcc": maximum_major},
    }


def _compiler_spec(name: str, compilers: dict) -> SimpleNamespace:
    return SimpleNamespace(name=name, extra_attributes={"compilers": compilers})


@pytest.mark.parametrize("result", [None, (1, "/usr/bin/cc1"), (0, "cc1"), (0, "/usr/bin/cc1\n")])
def test_compiler_query_failure_and_absolute_result(monkeypatch, result):
    from spack.installer import build

    def query(arguments, **kwargs):
        assert arguments == ["/usr/bin/gcc", "-print-prog-name=cc1"]
        if result is None:
            raise OSError("compiler unavailable")
        return SimpleNamespace(returncode=result[0], stdout=result[1])

    monkeypatch.setattr(build.subprocess, "run", query)
    expected = "/usr/bin/cc1" if result == (0, "/usr/bin/cc1\n") else None
    assert build._compiler_query("/usr/bin/gcc", "-print-prog-name=cc1") == expected


def test_selected_compilers_uses_language_edges_and_deduplicates(monkeypatch):
    from spack.installer import build

    compiler = _compiler_spec(
        "llvm", {"c": "/usr/bin/clang", "cxx": "/usr/bin/clang++", "fortran": "/usr/bin/flang"}
    )
    edge = SimpleNamespace(spec=compiler, virtuals=("c",))
    root = SimpleNamespace(
        name="root", extra_attributes={}, edges_to_dependencies=lambda: [edge, edge]
    )
    spec = cast(spack.spec.Spec, SimpleNamespace(traverse=lambda: [root]))
    monkeypatch.setattr(spack.compilers.config, "supported_compilers", lambda *, repo: ["gcc"])

    selected = build._selected_compilers(spec)

    assert [(language, path) for language, path, _ in selected] == [("c", "/usr/bin/clang")]


def test_selected_compilers_includes_supported_compiler_nodes(monkeypatch):
    from spack.installer import build

    compiler = _compiler_spec(
        "gcc", {"c": "/usr/bin/gcc", "cxx": "/usr/bin/g++", "fortran": "/usr/bin/gfortran"}
    )
    compiler.edges_to_dependencies = lambda: []
    spec = SimpleNamespace(traverse=lambda: [compiler])
    monkeypatch.setattr(spack.compilers.config, "supported_compilers", lambda *, repo: ["gcc"])

    selected = build._selected_compilers(spec)

    assert [(language, path) for language, path, _ in selected] == [
        ("c", "/usr/bin/gcc"),
        ("cxx", "/usr/bin/g++"),
        ("fortran", "/usr/bin/gfortran"),
    ]


def test_compiler_support_paths_ignores_bare_names_and_spack_binutils(monkeypatch):
    from spack.installer import build

    policy = {
        "compiler_programs": ["cc1", "cc1plus"],
        "binutils_programs": ["as", "ld"],
        "compiler_files": ["liblto_plugin.so"],
    }
    responses = {
        "-print-prog-name=cc1": "/usr/libexec/cc1\n",
        "-print-prog-name=cc1plus": "cc1plus\n",
        "-print-prog-name=as": "/opt/libexec/spack/as\n",
        "-print-prog-name=ld": "/usr/bin/ld\n",
        "-print-file-name=liblto_plugin.so": "/usr/lib/liblto_plugin.so\n",
    }
    queries = []

    def run(command, **kwargs):
        queries.append(command[1])
        return SimpleNamespace(returncode=0, stdout=responses[command[1]])

    monkeypatch.setattr(build.subprocess, "run", run)

    paths = build.compiler_support_paths("/usr/bin/cc", policy)

    assert queries == list(responses)
    assert paths == [
        build.ResolvedSandboxPath("cc1", "/usr/libexec/cc1"),
        build.ResolvedSandboxPath("ld", str(pathlib.Path("/usr/bin/ld").resolve())),
        build.ResolvedSandboxPath("liblto_plugin.so", "/usr/lib/liblto_plugin.so"),
    ]


def test_gcc_installation_uses_configured_compiler_roots(tmp_path: pathlib.Path, monkeypatch):
    from spack.installer import build

    installation = tmp_path / "usr" / "lib" / "gcc" / "x86_64-linux-gnu" / "14"
    library = installation / "libgcc.a"
    library.parent.mkdir(parents=True)
    library.touch()
    monkeypatch.setattr(
        build.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout=f"{library}\n"),
    )

    policy = {"compiler_roots": [str(tmp_path / "usr" / "lib" / "gcc")]}

    assert build._gcc_installation("cc", policy) == installation


def test_compiler_driver_paths_preserve_alias_spellings(tmp_path: pathlib.Path, monkeypatch):
    from spack.installer import build

    compiler = tmp_path / "bin" / "clang"
    compiler.parent.mkdir()
    compiler.touch()
    compiler_spec = _compiler_spec("llvm", {"c": str(compiler)})
    edge = SimpleNamespace(spec=compiler_spec, virtuals=("c",))
    root = SimpleNamespace(name="root", edges_to_dependencies=lambda: [edge])
    spec = cast(spack.spec.Spec, SimpleNamespace(traverse=lambda: [root]))
    policy = {"compiler_languages": ["c"], "compiler_driver_aliases": {"c": ["cc", "gcc"]}}
    monkeypatch.setattr(spack.compilers.config, "supported_compilers", lambda *, repo: [])

    assert build.compiler_driver_paths(spec, policy) == [
        build.ResolvedSandboxPath(str(compiler), str(compiler)),
        build.ResolvedSandboxPath(str(compiler.parent / "cc"), str(compiler)),
        build.ResolvedSandboxPath(str(compiler.parent / "gcc"), str(compiler)),
    ]
    assert build.compiler_alias_symlink_paths(spec, policy) == [
        spack.sandbox_namespaces.NamespaceGeneratedSymlink(
            str(compiler.parent / "cc"), str(compiler)
        ),
        spack.sandbox_namespaces.NamespaceGeneratedSymlink(
            str(compiler.parent / "gcc"), str(compiler)
        ),
    ]


def test_compiler_driver_paths_give_generic_aliases_to_first_compiler(monkeypatch, tmp_path):
    from spack.installer import build

    compiler_bin = tmp_path / "bin"
    compiler_bin.mkdir()
    primary = compiler_bin / "g++-16"
    secondary = compiler_bin / "g++-15"
    primary.touch()
    secondary.touch()
    selected = [
        ("cxx", str(primary), SimpleNamespace()),
        ("cxx", str(secondary), SimpleNamespace()),
    ]
    monkeypatch.setattr(build, "_selected_compilers", lambda spec, policy: selected)
    policy = {"compiler_driver_aliases": {"cxx": ["c++", "g++"]}}

    assert build.compiler_driver_paths(cast(spack.spec.Spec, object()), policy) == [
        build.ResolvedSandboxPath(str(primary), str(primary)),
        build.ResolvedSandboxPath(str(compiler_bin / "c++"), str(primary)),
        build.ResolvedSandboxPath(str(compiler_bin / "g++"), str(primary)),
        build.ResolvedSandboxPath(str(secondary), str(secondary)),
    ]


def test_executable_support_paths_select_file_magic_and_cpp_cc1(
    tmp_path: pathlib.Path, monkeypatch
):
    from spack.installer import build

    magic = tmp_path / "magic.mgc"
    magic.touch()
    policy = {"file_runtime_read_paths": [str(magic)]}
    monkeypatch.setattr(
        build.subprocess,
        "run",
        lambda command, **kwargs: SimpleNamespace(returncode=0, stdout="/usr/lib/cc1\n"),
    )

    assert build.executable_support_paths("/usr/bin/file", policy) == [
        build.ResolvedSandboxPath(str(magic), str(magic))
    ]
    assert build.executable_support_paths("/usr/bin/cpp", policy) == [
        build.ResolvedSandboxPath("cc1", "/usr/lib/cc1")
    ]


def test_stage_tool_paths_include_helper_chain_and_git_exec_path(monkeypatch):
    from spack.installer import build

    policy = {"stage_programs": ["gunzip", "git"]}
    tools = {
        "gunzip": "/tools/gunzip",
        "gzip": "/tools/gzip",
        "sh": "/tools/sh",
        "git": "/tools/git",
    }
    monkeypatch.setattr(build, "which_string", tools.get)
    monkeypatch.setattr(
        build.subprocess,
        "run",
        lambda command, **kwargs: SimpleNamespace(returncode=0, stdout="/tools/git-core\n"),
    )

    assert build.stage_tool_paths(policy) == [
        build.ResolvedSandboxPath("gunzip", "/tools/gunzip"),
        build.ResolvedSandboxPath("git", "/tools/git"),
        build.ResolvedSandboxPath("/tools/git --exec-path", "/tools/git-core"),
        build.ResolvedSandboxPath("gzip", "/tools/gzip"),
        build.ResolvedSandboxPath("sh", "/tools/sh"),
    ]


def test_tool_runtime_paths_include_owner_and_link_run_dependencies(tmp_path: pathlib.Path):
    from spack.installer import build

    tool_prefix = tmp_path / "tar"
    tool = tool_prefix / "bin" / "tar"
    tool.parent.mkdir(parents=True)
    tool.touch()
    dependency = SimpleNamespace(prefix=tmp_path / "libiconv")
    owner = SimpleNamespace(prefix=tool_prefix, traverse=lambda **kwargs: [dependency])
    unrelated = SimpleNamespace(prefix=tmp_path / "unrelated")
    spec = cast(spack.spec.Spec, SimpleNamespace(traverse=lambda: [owner, unrelated]))

    assert build.tool_runtime_paths(spec, [build.ResolvedSandboxPath("tar", str(tool))]) == [
        str(tool_prefix),
        str(dependency.prefix),
    ]


def _system_gcc_layout(tmp_path: pathlib.Path):
    install_root = tmp_path / "lib" / "gcc"
    target = install_root / "test-linux-gnu"
    (target / "15").mkdir(parents=True)
    (target / "16").mkdir()
    include_root = tmp_path / "include"
    (include_root / "c++" / "15").mkdir(parents=True)
    (include_root / "c++" / "16").mkdir()
    return target, include_root


@pytest.mark.parametrize("compiler_name, expected_version", [("llvm", "15"), ("gcc", "16")])
def test_system_compiler_headers_select_libstdcxx_policy_version(
    tmp_path: pathlib.Path, monkeypatch, compiler_name: str, expected_version: str
):
    from spack.installer import build

    target, include_root = _system_gcc_layout(tmp_path)
    compiler = _compiler_spec(compiler_name, {"cxx": "/usr/bin/clang++"})
    edge = SimpleNamespace(spec=compiler, virtuals=("cxx",))
    root = SimpleNamespace(name="root", extra_attributes={}, edges_to_dependencies=lambda: [edge])
    spec = cast(spack.spec.Spec, SimpleNamespace(traverse=lambda: [root]))
    policy = _minimal_header_policy(include_root)
    monkeypatch.setattr(build, "_gcc_installation", lambda compiler_path, policy: target / "16")

    paths = build.system_compiler_header_paths(spec, policy)

    assert str(include_root / "stdio.h") in paths
    assert str(include_root / "linux") in paths
    assert str(include_root / "c++" / expected_version) in paths
    assert str(include_root / "c++" / ("16" if expected_version == "15" else "15")) not in paths


def test_system_compiler_headers_ignore_non_system_compilers(tmp_path: pathlib.Path):
    from spack.installer import build

    compiler = _compiler_spec("llvm", {"cxx": str(tmp_path / "clang++")})
    edge = SimpleNamespace(spec=compiler, virtuals=("cxx",))
    root = SimpleNamespace(name="root", extra_attributes={}, edges_to_dependencies=lambda: [edge])
    spec = cast(spack.spec.Spec, SimpleNamespace(traverse=lambda: [root]))

    assert build.system_compiler_header_paths(spec, _minimal_header_policy(tmp_path)) == []


def test_gcc_installation_mask_excludes_permitted_cxx_installation(
    tmp_path: pathlib.Path, monkeypatch
):
    from spack.installer import build

    target, include_root = _system_gcc_layout(tmp_path)
    compiler = _compiler_spec("llvm", {"cxx": "/usr/bin/clang++"})
    edge = SimpleNamespace(spec=compiler, virtuals=("cxx",))
    root = SimpleNamespace(name="root", extra_attributes={}, edges_to_dependencies=lambda: [edge])
    spec = cast(spack.spec.Spec, SimpleNamespace(traverse=lambda: [root]))
    monkeypatch.setattr(build, "_gcc_installation", lambda compiler_path, policy: target / "16")

    assert build.gcc_installation_dirs_to_mask(spec, _minimal_header_policy(include_root)) == [
        str(target / "16")
    ]


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
        hidden_roots=(
            str(hidden_host_state),
            str(host / "usr"),
            str(host / "repos-python"),
            str(host / "store"),
            str(host / "build"),
            str(spack_prefix),
            str(pathlib.Path(os.devnull).parent),
        ),
        compiler_paths=(str(compiler),),
        tool_paths=(str(tool),),
        header_paths=(str(headers), str(compiler_headers)),
        runtime_paths=(str(runtime),),
        temporary_paths=(str(temporary_path),),
    )

    policy, plan = namespace_filesystem_policy_and_plan_from_inputs(
        {}, spec, str(stage_path), str(mount_plan_stage), selected_paths
    )

    assert policy.read_only_view
    assert plan.read_only_view
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
        str(repository_python_path.resolve()),
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


def test_namespace_selects_host_device_and_worker_inputs(monkeypatch, tmp_path: pathlib.Path):
    from spack.installer.build import select_namespace_host_device_worker_paths

    host = tmp_path / "host"
    for relative in ("bin", "lib", "share", "etc", "config", "repo", "store/bin"):
        (host / relative).mkdir(parents=True)
    runtime = host / "lib" / "libc.so"
    runtime.touch()
    dependency = host / "store" / "dependency"
    dependency.mkdir()
    install_prefix = host / "store" / "install"
    install_prefix.mkdir()
    stage = host / "stage"
    stage.mkdir()
    worker_root = host / "worker"
    worker_root.mkdir()
    fetch_cache = host / "fetch-cache"
    fetch_cache.mkdir()
    log_path = host / "worker.log"
    log_path.touch()
    jobserver = host / "jobserver_fifo"
    jobserver.touch()
    repository = host / "repo"
    device = pathlib.Path(os.devnull)

    monkeypatch.setattr(spack.paths, "bin_path", str(host / "bin"))
    monkeypatch.setattr(spack.paths, "lib_path", str(host / "lib"))
    monkeypatch.setattr(spack.paths, "share_path", str(host / "share"))
    monkeypatch.setattr(spack.paths, "etc_path", str(host / "etc"))
    monkeypatch.setattr(spack.paths, "user_config_path", str(host / "config"))
    monkeypatch.setattr(spack.paths, "system_config_path", str(host / "config"))
    monkeypatch.setattr(
        spack.repo, "PATH", SimpleNamespace(repos=[SimpleNamespace(root=str(repository))])
    )
    monkeypatch.setattr(spack.store.STORE, "unpadded_root", str(host / "store"))
    monkeypatch.setattr(spack.store.STORE, "upstreams", None)
    monkeypatch.setattr(
        spack.util.ld_so_conf, "host_dynamic_linker_search_paths", lambda: [str(runtime)]
    )

    spec = cast(
        Any,
        SimpleNamespace(
            prefix=install_prefix,
            traverse=lambda root=False: iter([SimpleNamespace(prefix=dependency, external=False)]),
        ),
    )
    policy = {
        "hidden_roots": [str(host / "store"), str(host / "stage")],
        "replacement_roots": [str(host / "stage")],
        "host_runtime_read_paths": [str(runtime), str(host / "missing-runtime")],
        "file_runtime_read_paths": [],
        "device_nodes": [str(device), str(host / "not-a-device")],
    }

    selected = select_namespace_host_device_worker_paths(
        {"allow_read": [str(repository)], "allow_write": [str(worker_root)]},
        spec,
        str(stage),
        log_path=str(log_path),
        jobserver_paths=(str(jobserver),),
        worker_root=str(worker_root),
        fetch_cache_path=str(fetch_cache),
        policy=policy,
    )

    assert selected.hidden_roots == tuple(
        sorted((str((host / "stage").resolve()), str((host / "store").resolve())))
    )
    assert selected.replacement_roots == (str((host / "stage").resolve()),)
    assert selected.host_runtime_paths == (str(runtime.resolve()),)
    assert selected.device_paths == (str(device.resolve()),)
    assert set(selected.read_only_paths) >= {
        str((host / "bin").resolve()),
        str((host / "lib").resolve()),
        str((host / "share").resolve()),
        str((host / "etc").resolve()),
        str(dependency.resolve()),
        str(repository.resolve()),
    }
    assert set(selected.writable_paths) >= {
        str(stage.resolve()),
        str(install_prefix.resolve()),
        str(worker_root.resolve()),
        str(fetch_cache.resolve()),
        str(log_path.resolve()),
        str(jobserver.resolve()),
    }

    with pytest.raises(spack.sandbox_namespaces.NamespaceSetupError, match="does not exist"):
        select_namespace_host_device_worker_paths(
            {},
            spec,
            str(stage),
            log_path=None,
            jobserver_paths=(),
            worker_root=str(worker_root),
            fetch_cache_path=str(host / "missing-fetch-cache"),
            policy=policy,
        )


def test_prepare_namespace_activation_compiles_selected_production_policy(
    monkeypatch, tmp_path: pathlib.Path
):
    from spack.installer import build

    host = tmp_path / "host"

    def directory(path):
        path.mkdir(parents=True)
        return path

    def file(path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        return path

    hidden_bin = directory(host / "usr" / "bin")
    hidden_include = directory(host / "usr" / "include")
    selected_hidden_runtime = directory(host / "usr" / "lib")
    compiler = file(hidden_bin / "cc")
    tool = file(hidden_bin / "tar")
    headers = directory(hidden_include / "compiler")
    runtime = file(host / "etc" / "passwd")
    repository = directory(host / "repository")
    repository_python = directory(host / "repository-python")
    hidden_home = directory(host / "home")
    dependency = directory(host / "store" / "dependency")
    prefix = directory(host / "store" / "install")
    stage = directory(host / "stage")
    worker_root = directory(host / "worker")
    user_cache = directory(hidden_home / ".spack")
    fetch_cache = directory(user_cache / "source-cache")
    misc_cache = directory(user_cache / "misc-cache")
    log_path = file(host / "build.log")
    jobserver = file(host / "jobserver")

    spack_source_paths = tuple(
        directory(path)
        for path in (
            host / "spack" / "bin",
            host / "spack" / "lib",
            host / "spack" / "share" / "spack",
            host / "spack" / "etc" / "spack",
        )
    )
    sbang = file(host / "store" / "bin" / "sbang")
    spec = cast(
        Any,
        SimpleNamespace(
            prefix=prefix,
            traverse=lambda root=False: iter([SimpleNamespace(prefix=dependency, external=False)]),
        ),
    )
    selected_host_paths = build.NamespaceHostDeviceWorkerPaths(
        hidden_roots=(
            str(hidden_bin),
            str(hidden_include),
            str(selected_hidden_runtime),
            str(hidden_home),
            str(pathlib.Path("/dev")),
        ),
        replacement_roots=(),
        host_runtime_paths=(str(runtime), str(selected_hidden_runtime), os.devnull),
        device_paths=(os.devnull,),
        read_only_paths=(
            str(repository),
            str(repository_python),
            str(user_cache),
            str(misc_cache),
        ),
        writable_paths=(
            str(stage),
            str(prefix),
            str(worker_root),
            str(fetch_cache),
            str(log_path),
            str(jobserver),
        ),
    )

    monkeypatch.setattr(
        build,
        "select_namespace_host_device_worker_paths",
        lambda *args, **kwargs: selected_host_paths,
    )
    monkeypatch.setattr(
        build,
        "compiler_driver_paths",
        lambda spec: [build.ResolvedSandboxPath(str(compiler), str(compiler))],
    )
    monkeypatch.setattr(build, "_selected_compilers", lambda spec: ())
    monkeypatch.setattr(
        build, "stage_tool_paths", lambda: [build.ResolvedSandboxPath(str(tool), str(tool))]
    )
    monkeypatch.setattr(build, "tool_runtime_paths", lambda spec, tools: [])
    monkeypatch.setattr(build, "system_compiler_header_paths", lambda spec: (str(headers),))
    monkeypatch.setattr(build, "compiler_alias_symlink_paths", lambda spec: ())
    monkeypatch.setattr(
        spack.repo,
        "PATH",
        SimpleNamespace(
            repos=[SimpleNamespace(root=str(repository), python_path=str(repository_python))]
        ),
    )
    monkeypatch.setattr(spack.paths, "bin_path", str(spack_source_paths[0]))
    monkeypatch.setattr(spack.paths, "lib_path", str(spack_source_paths[1]))
    monkeypatch.setattr(spack.paths, "share_path", str(spack_source_paths[2]))
    monkeypatch.setattr(spack.paths, "etc_path", str(spack_source_paths[3]))
    monkeypatch.setattr(spack.store.STORE, "unpadded_root", str(host / "store"))
    monkeypatch.setattr(spack.store.STORE, "upstreams", None)

    inherited_environment = dict(os.environ)
    inherited_tempdir = build.tempfile.tempdir
    activation, scratch = build.prepare_namespace_activation(
        {}, spec, str(stage), str(log_path), (str(jobserver),), str(worker_root), str(fetch_cache)
    )
    try:
        assert activation.worker_root == str(worker_root)
        assert activation.policy.tmpfs_paths == ("/dev/shm",)
        assert set(activation.policy.generated_symlinks) == {
            spack.sandbox_namespaces.NamespaceGeneratedSymlink("/dev/" + name, target)
            for name, target in (
                ("fd", "/proc/self/fd"),
                ("stdin", "/proc/self/fd/0"),
                ("stdout", "/proc/self/fd/1"),
                ("stderr", "/proc/self/fd/2"),
            )
        }
        assert os.environ == inherited_environment
        assert build.tempfile.tempdir == inherited_tempdir
        assert not list(worker_root.iterdir())
        read_only_targets = {mount.target for mount in activation.policy.read_only_mounts}
        read_write_targets = {mount.target for mount in activation.policy.read_write_mounts}
        assert read_only_targets == {str(compiler), str(tool), str(headers), str(user_cache)}
        assert read_write_targets == {
            os.devnull,
            str(stage),
            str(prefix),
            str(worker_root),
            str(fetch_cache),
            str(log_path),
            str(jobserver),
        }
        assert str(runtime) not in read_only_targets
        assert str(selected_hidden_runtime) not in activation.policy.hidden_roots
        assert str(selected_hidden_runtime) not in read_only_targets
        assert str(misc_cache) not in read_only_targets
        assert str(repository) not in read_only_targets
        assert str(dependency) not in read_only_targets
        assert str(sbang) not in read_only_targets
        assert sbang.exists()
        spack.sandbox_namespaces.build_namespace_mount_plan_from_policy(
            activation.policy, activation.mount_plan_stage
        )
    finally:
        scratch.cleanup()


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
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    source_root = tmp_path / "source"
    source_root.mkdir()
    missing = tmp_path / "missing-compiler"
    spec = cast(Any, SimpleNamespace(prefix=existing, traverse=lambda root=True: iter(())))
    selected_paths = NamespacePolicyInputPaths(
        hidden_roots=(str(hidden),),
        compiler_paths=(str(missing),),
        tool_paths=(str(source_root),),
        header_paths=(str(source_root),),
        runtime_paths=(str(source_root),),
        temporary_paths=(str(existing),),
    )
    monkeypatch.setattr(
        spack.repo,
        "PATH",
        SimpleNamespace(repos=[SimpleNamespace(root=str(source_root), python_path=None)]),
    )
    monkeypatch.setattr(spack.paths, "bin_path", str(source_root))
    monkeypatch.setattr(spack.paths, "lib_path", str(source_root))
    monkeypatch.setattr(spack.paths, "share_path", str(source_root))
    monkeypatch.setattr(spack.paths, "etc_path", str(source_root))
    sbang = source_root / "store" / "bin" / "sbang"
    sbang.parent.mkdir(parents=True)
    sbang.touch()
    monkeypatch.setattr(spack.store.STORE, "unpadded_root", str(source_root / "store"))
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

    uncovered_temporary = tmp_path / "uncovered-temporary"
    uncovered_temporary.mkdir()
    policy, plan = namespace_filesystem_policy_and_plan_from_inputs(
        {},
        spec,
        str(existing),
        str(tmp_path / "mount-plan"),
        selected_paths._replace(
            compiler_paths=(str(compiler),), temporary_paths=(str(uncovered_temporary),)
        ),
    )
    assert str(uncovered_temporary) in {mount.target for mount in policy.read_write_mounts}
    assert str(uncovered_temporary) in {mount.target for mount in plan.restoration_mounts}
