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
        self.mount_setattr_calls = []

    def unshare(self, flags):
        self.unshare_calls.append(flags.value)
        return 0

    def mount(self, source, target, filesystemtype, flags, data):
        self.mount_calls.append((source, target, flags.value))
        return 0

    def mount_setattr(self, directory_fd, path, flags, attributes, size):
        self.mount_setattr_calls.append((directory_fd.value, path, flags.value))
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


def test_filesystem_policy_is_immutable_and_deterministic(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    read_only_source = tmp_path / "read-only-source"
    read_only_source.touch()
    read_write_source = tmp_path / "read-write-source"
    read_write_source.mkdir()

    policy = ns.build_namespace_filesystem_policy(
        [str(hidden)],
        [(str(read_only_source), str(hidden / "z-read-only"))],
        [(str(read_write_source), str(hidden / "a-read-write"))],
        [ns.NamespaceGeneratedPath(str(hidden / "generated"), True)],
    )

    assert policy == ns.NamespaceFilesystemPolicy(
        (str(hidden),),
        (
            ns.NamespaceMountRequest(
                str(read_only_source),
                str(hidden / "z-read-only"),
                ns.NamespaceMountAccess.READ_ONLY,
            ),
        ),
        (
            ns.NamespaceMountRequest(
                str(read_write_source),
                str(hidden / "a-read-write"),
                ns.NamespaceMountAccess.READ_WRITE,
            ),
        ),
        (ns.NamespaceGeneratedPath(str(hidden / "generated"), True),),
    )
    with pytest.raises(AttributeError):
        setattr(policy, "hidden_roots", ())


def test_filesystem_policy_rejects_hidden_root_overlap(tmp_path):
    hidden = tmp_path / "hidden"
    child = hidden / "child"
    child.mkdir(parents=True)

    with pytest.raises(ns.NamespaceSetupError, match="hidden roots.*overlapping"):
        ns.build_namespace_filesystem_policy([str(hidden), str(child)])


def test_filesystem_policy_rejects_interleaved_hidden_root_overlap(tmp_path):
    ancestor = tmp_path / "a"
    descendant = ancestor / "child"
    descendant.mkdir(parents=True)
    interloper = tmp_path / "a-between"
    interloper.mkdir()

    with pytest.raises(ns.NamespaceSetupError, match="hidden roots.*overlapping"):
        ns.build_namespace_filesystem_policy([str(ancestor), str(interloper), str(descendant)])


def test_filesystem_policy_rejects_missing_hidden_root(tmp_path):
    with pytest.raises(ns.NamespaceSetupError, match="hidden root does not exist"):
        ns.build_namespace_filesystem_policy([str(tmp_path / "missing")])


@pytest.mark.parametrize(
    "invalid_input, operation, message, error_number",
    [
        ("file-root", "hidden root", "hidden root is not a directory", errno.ENOTDIR),
        ("missing-source", "mount source", "mount source does not exist", errno.ENOENT),
        ("outside-generated", "generated path", "not below a hidden root", errno.EINVAL),
        ("invalid-generated", "generated path", "invalid generated path", errno.EINVAL),
        ("root-target", "categories", "duplicate hidden root", errno.EINVAL),
    ],
)
def test_filesystem_policy_rejects_invalid_inputs(
    tmp_path, invalid_input, operation, message, error_number
):
    hidden = tmp_path / "hidden"
    source = tmp_path / "source"
    source.touch()
    read_only = []
    generated = []
    if invalid_input == "file-root":
        hidden.touch()
    else:
        hidden.mkdir()
    if invalid_input == "missing-source":
        read_only = [(str(tmp_path / "missing"), str(hidden / "target"))]
    elif invalid_input == "outside-generated":
        generated = [ns.NamespaceGeneratedPath(str(tmp_path / "outside"), True)]
    elif invalid_input == "invalid-generated":
        generated = [ns.NamespaceGeneratedPath(str(hidden / "generated"), "directory")]
    elif invalid_input == "root-target":
        read_only = [(str(source), str(hidden))]

    with pytest.raises(ns.NamespaceSetupError, match=message) as caught:
        ns.build_namespace_filesystem_policy([str(hidden)], read_only, generated_paths=generated)
    assert caught.value.operation == "validate namespace policy " + operation
    assert caught.value.errno == error_number


def test_filesystem_policy_rejects_forged_read_write_access(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    source = tmp_path / "source"
    source.touch()
    policy = ns.NamespaceFilesystemPolicy(
        (str(hidden),),
        (),
        (
            ns.NamespaceMountRequest(
                str(source), str(hidden / "target"), ns.NamespaceMountAccess.READ_ONLY
            ),
        ),
    )

    with pytest.raises(ns.NamespaceSetupError, match="invalid read-write mount") as caught:
        ns.build_namespace_mount_plan_from_policy(policy, str(tmp_path / "stage"))
    assert caught.value.operation == "validate namespace policy access"


def test_filesystem_policy_rejects_classified_path_containing_hidden_root(tmp_path):
    parent = tmp_path / "parent"
    hidden = parent / "hidden"
    hidden.mkdir(parents=True)
    source = tmp_path / "source"
    source.mkdir()

    with pytest.raises(ns.NamespaceSetupError, match="policy categories.*overlapping"):
        ns.build_namespace_filesystem_policy([str(hidden)], [(str(source), str(parent))])


@pytest.mark.parametrize("conflict", ["duplicate", "access", "overlap", "generated"])
def test_filesystem_policy_rejects_classification_conflicts(tmp_path, conflict):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    first_source = tmp_path / "first-source"
    second_source = tmp_path / "second-source"
    first_source.mkdir()
    second_source.mkdir()
    first_target = hidden / "target"
    second_target = first_target if conflict != "overlap" else first_target / "child"
    read_only = [(str(first_source), str(first_target))]
    read_write = []
    generated = []
    if conflict == "duplicate":
        read_only.append((str(second_source), str(first_target)))
    elif conflict in ("access", "overlap"):
        read_write.append((str(second_source), str(second_target)))
    else:
        generated.append(ns.NamespaceGeneratedPath(str(first_target), False))

    with pytest.raises(ns.NamespaceSetupError, match="classified paths"):
        ns.build_namespace_filesystem_policy([str(hidden)], read_only, read_write, generated)


def test_filesystem_policy_rejects_interleaved_classified_overlap(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    sources = []
    for index in range(3):
        source = tmp_path / f"source-{index}"
        source.mkdir()
        sources.append(source)

    with pytest.raises(ns.NamespaceSetupError, match="classified paths.*overlapping"):
        ns.build_namespace_filesystem_policy(
            [str(hidden)],
            [
                (str(sources[0]), str(hidden / "a")),
                (str(sources[1]), str(hidden / "a-between")),
                (str(sources[2]), str(hidden / "a" / "child")),
            ],
        )


def test_filesystem_policy_rejects_wrong_access_category(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    source = tmp_path / "source"
    source.mkdir()
    policy = ns.NamespaceFilesystemPolicy(
        (str(hidden),),
        (
            ns.NamespaceMountRequest(
                str(source), str(hidden / "target"), ns.NamespaceMountAccess.READ_WRITE
            ),
        ),
    )

    with pytest.raises(ns.NamespaceSetupError, match="policy access.*read-only"):
        ns.build_namespace_mount_plan_from_policy(policy, str(tmp_path / "stage"))


def test_filesystem_policy_rejects_stage_below_hidden_root_before_namespace_entry(
    namespace_setup, tmp_path
):
    libc, _ = namespace_setup
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    policy = ns.build_namespace_filesystem_policy([str(hidden)])

    with pytest.raises(ns.NamespaceSetupError, match="stage must be outside hidden roots"):
        ns.NamespaceSandbox(libc).prepare_filesystem_policy(policy, str(hidden / "mount-stage"))
    assert libc.unshare_calls == []


def test_filesystem_policy_rejects_hidden_root_in_reserved_scratch(tmp_path):
    stage = tmp_path / "stage"
    hidden = stage / "spack-preserved-host-paths" / "nested"
    hidden.mkdir(parents=True)
    policy = ns.build_namespace_filesystem_policy([str(hidden)])

    with pytest.raises(ns.NamespaceSetupError, match="hidden root overlaps mount-plan scratch"):
        ns.build_namespace_mount_plan_from_policy(policy, str(stage))


def test_filesystem_policy_compiles_generated_paths(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    generated_dir = hidden / "generated-dir"
    generated_file = hidden / "generated-file"
    stage = tmp_path / "stage"
    policy = ns.build_namespace_filesystem_policy(
        [str(hidden)],
        generated_paths=[
            ns.NamespaceGeneratedPath(str(generated_file), False),
            ns.NamespaceGeneratedPath(str(generated_dir), True),
        ],
    )

    plan = ns.build_namespace_mount_plan_from_policy(policy, str(stage))
    assert plan.generated_paths == (
        ns.NamespaceGeneratedPath(str(generated_dir), True),
        ns.NamespaceGeneratedPath(str(generated_file), False),
    )
    assert ns._apply_namespace_mount_plan(plan, FakeLibc())
    assert (stage / "spack-empty-host-dirs/0/generated-dir").is_dir()
    assert (stage / "spack-empty-host-dirs/0/generated-file").is_file()


def test_mount_plan_does_not_recreate_disappeared_preserved_source(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    source = tmp_path / "source"
    source.mkdir()
    plan = ns.build_namespace_mount_plan(
        [str(hidden)],
        str(tmp_path / "stage"),
        [
            ns.NamespaceMountRequest(
                str(source), str(hidden / "target"), ns.NamespaceMountAccess.READ_ONLY
            )
        ],
    )
    source.rmdir()

    with pytest.raises(ns.NamespaceSetupError, match="mount source disappeared"):
        ns._apply_namespace_mount_plan(plan, FakeLibc())
    assert not source.exists()


def test_filesystem_policy_validation_precedes_namespace_entry(namespace_setup, tmp_path):
    libc, _ = namespace_setup
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    source = tmp_path / "source"
    source.mkdir()
    policy = ns.build_namespace_filesystem_policy(
        [str(hidden)], [(str(source), str(tmp_path / "outside"))]
    )

    with pytest.raises(ns.NamespaceSetupError, match="not below a hidden root"):
        ns.NamespaceSandbox(libc).prepare_filesystem_policy(policy, str(tmp_path / "stage"))
    assert libc.unshare_calls == []


def test_empty_mount_tree_enters_namespace(namespace_setup, tmp_path):
    libc, _ = namespace_setup
    sandbox = ns.NamespaceSandbox(libc)
    assert sandbox.prepare_mount_tree([], str(tmp_path))
    assert sandbox.namespace_ready
    assert libc.unshare_calls == [ns.CLONE_NEWUSER | ns.CLONE_NEWNS]
    assert sandbox.prepare_mount_tree([], str(tmp_path))
    assert len(libc.unshare_calls) == 1


def test_mount_plan_is_immutable_and_deterministic(tmp_path):
    first = tmp_path / "z-target"
    second = tmp_path / "a-target"
    first.mkdir()
    second.mkdir()

    plan = ns.build_namespace_mount_plan([str(first), str(second)], str(tmp_path / "stage"))

    assert plan.stage_path == str((tmp_path / "stage").resolve())
    assert plan.mounts == (
        ns.NamespaceMount(str(tmp_path / "stage/spack-empty-host-dirs/0"), str(second)),
        ns.NamespaceMount(str(tmp_path / "stage/spack-empty-host-dirs/1"), str(first)),
    )
    with pytest.raises(AttributeError):
        setattr(plan, "mounts", ())


@pytest.mark.parametrize("conflict", ["duplicate", "nested"])
def test_mount_plan_rejects_conflicting_targets(tmp_path, conflict):
    parent = tmp_path / "parent"
    child = parent / "child"
    parent.mkdir()
    child.mkdir()
    paths = [str(parent), str(parent)] if conflict == "duplicate" else [str(parent), str(child)]

    with pytest.raises(ns.NamespaceSetupError, match="mount plan targets"):
        ns.build_namespace_mount_plan(paths, str(tmp_path / "stage"))


def test_mount_plan_rejects_invalid_types(tmp_path):
    target_file = tmp_path / "target-file"
    stage_file = tmp_path / "stage-file"
    target_file.touch()
    stage_file.touch()

    with pytest.raises(ns.NamespaceSetupError, match="target is not a directory"):
        ns.build_namespace_mount_plan([str(target_file)], str(tmp_path / "stage"))
    with pytest.raises(ns.NamespaceSetupError, match="stage path is not a directory"):
        ns.build_namespace_mount_plan([], str(stage_file))


def test_mount_plan_preserves_sources_before_hiding_and_restores_aliases(tmp_path):
    hidden = tmp_path / "usr" / "bin"
    hidden.mkdir(parents=True)
    merged_alias = tmp_path / "bin"
    merged_alias.symlink_to(tmp_path / "usr" / "bin", target_is_directory=True)
    source = tmp_path / "selected-tool"
    source.touch()
    stage = tmp_path / "stage"

    plan = ns.build_namespace_mount_plan(
        [str(hidden)],
        str(stage),
        [
            ns.NamespaceMountRequest(
                str(source), str(merged_alias / "tool"), ns.NamespaceMountAccess.READ_ONLY
            )
        ],
    )

    assert plan.preserved_mounts == (
        ns.NamespacePreservedMount(
            str(source.resolve()),
            str(stage / "spack-preserved-host-paths/0"),
            False,
            ns.NamespaceMountAccess.READ_ONLY,
        ),
    )
    assert plan.restoration_mounts == (
        ns.NamespacePreservedMount(
            str(stage / "spack-preserved-host-paths/0"),
            str(hidden / "tool"),
            False,
            ns.NamespaceMountAccess.READ_ONLY,
        ),
    )

    libc = FakeLibc()
    assert ns._apply_namespace_mount_plan(plan, libc)
    assert libc.mount_calls == [
        (os.fsencode(source), os.fsencode(stage / "spack-preserved-host-paths/0"), ns.MS_BIND),
        (b"tmpfs", os.fsencode(stage / "spack-empty-host-dirs"), ns._EMPTY_SOURCE_FLAGS),
        (
            None,
            os.fsencode(stage / "spack-empty-host-dirs"),
            ns.MS_REMOUNT | ns.MS_RDONLY | ns._EMPTY_SOURCE_FLAGS,
        ),
        (os.fsencode(stage / "spack-empty-host-dirs/0"), os.fsencode(hidden), ns.MS_BIND),
        (
            os.fsencode(stage / "spack-preserved-host-paths/0"),
            os.fsencode(hidden / "tool"),
            ns.MS_BIND,
        ),
    ]
    assert libc.mount_setattr_calls == [
        (ns.AT_FDCWD, os.fsencode(stage / "spack-preserved-host-paths/0"), 0),
        (ns.AT_FDCWD, os.fsencode(hidden / "tool"), 0),
    ]


def test_mount_plan_preserves_directory_trees_recursively(tmp_path):
    hidden = tmp_path / "usr" / "include"
    hidden.mkdir(parents=True)
    source = tmp_path / "headers"
    source.mkdir()
    plan = ns.build_namespace_mount_plan(
        [str(hidden)],
        str(tmp_path / "stage"),
        [
            ns.NamespaceMountRequest(
                str(source), str(hidden / "selected"), ns.NamespaceMountAccess.READ_ONLY
            )
        ],
    )

    libc = FakeLibc()
    assert ns._apply_namespace_mount_plan(plan, libc)
    assert libc.mount_calls[0][2] == ns.MS_BIND | ns.MS_REC
    assert libc.mount_calls[1][2] == ns._EMPTY_SOURCE_FLAGS
    assert libc.mount_calls[2][2] == ns.MS_REMOUNT | ns.MS_RDONLY | ns._EMPTY_SOURCE_FLAGS
    assert libc.mount_calls[3][2] == ns.MS_BIND
    assert libc.mount_calls[4][2] == ns.MS_BIND | ns.MS_REC
    assert libc.mount_setattr_calls == [
        (
            ns.AT_FDCWD,
            os.fsencode(tmp_path / "stage/spack-preserved-host-paths/0"),
            ns.AT_RECURSIVE,
        ),
        (ns.AT_FDCWD, os.fsencode(hidden / "selected"), ns.AT_RECURSIVE),
    ]


def test_mount_plan_rejects_preserved_source_relationships(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    source = tmp_path / "source"
    source.mkdir()

    with pytest.raises(ns.NamespaceSetupError, match="preserved source does not exist"):
        ns.build_namespace_mount_plan(
            [str(hidden)],
            str(tmp_path / "stage"),
            [
                ns.NamespaceMountRequest(
                    str(tmp_path / "missing"), str(hidden / "x"), ns.NamespaceMountAccess.READ_ONLY
                )
            ],
        )
    with pytest.raises(ns.NamespaceSetupError, match="not below a hidden directory"):
        ns.build_namespace_mount_plan(
            [str(hidden)],
            str(tmp_path / "stage"),
            [
                ns.NamespaceMountRequest(
                    str(source), str(tmp_path / "other"), ns.NamespaceMountAccess.READ_ONLY
                )
            ],
        )


def test_mount_plan_rejects_invalid_preserved_access_before_namespace_entry(
    namespace_setup, tmp_path
):
    libc, _ = namespace_setup
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    source = tmp_path / "source"
    source.mkdir()
    sandbox = ns.NamespaceSandbox(libc)

    with pytest.raises(ns.NamespaceSetupError, match="invalid preserved mount access"):
        sandbox.prepare_mount_tree(
            [str(hidden)],
            str(tmp_path / "stage"),
            [ns.NamespaceMountRequest(str(source), str(hidden / "selected"), "read-only")],
        )
    assert libc.unshare_calls == []


def test_writable_preserved_mounts_remain_writable(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    source = tmp_path / "source"
    source.mkdir()
    plan = ns.build_namespace_mount_plan(
        [str(hidden)],
        str(tmp_path / "stage"),
        [
            ns.NamespaceMountRequest(
                str(source), str(hidden / "selected"), ns.NamespaceMountAccess.READ_WRITE
            )
        ],
    )

    libc = FakeLibc()
    assert ns._apply_namespace_mount_plan(plan, libc)
    assert libc.mount_setattr_calls == []


def test_mount_plan_validation_precedes_namespace_entry(namespace_setup, tmp_path):
    libc, _ = namespace_setup
    parent = tmp_path / "parent"
    child = parent / "child"
    parent.mkdir()
    child.mkdir()
    sandbox = ns.NamespaceSandbox(libc)

    with pytest.raises(ns.NamespaceSetupError, match="conflicting mount targets"):
        sandbox.prepare_mount_tree([str(parent), str(child)], str(tmp_path / "stage"))
    assert libc.unshare_calls == []


def test_preserved_source_validation_precedes_namespace_entry(namespace_setup, tmp_path):
    libc, _ = namespace_setup
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    sandbox = ns.NamespaceSandbox(libc)

    with pytest.raises(ns.NamespaceSetupError, match="preserved source does not exist"):
        sandbox.prepare_mount_tree(
            [str(hidden)],
            str(tmp_path / "stage"),
            [
                ns.NamespaceMountRequest(
                    str(tmp_path / "missing"), str(hidden / "x"), ns.NamespaceMountAccess.READ_ONLY
                )
            ],
        )
    assert libc.unshare_calls == []


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
        (b"tmpfs", os.fsencode(tmp_path / "spack-empty-host-dirs"), ns._EMPTY_SOURCE_FLAGS),
        (
            None,
            os.fsencode(tmp_path / "spack-empty-host-dirs"),
            ns.MS_REMOUNT | ns.MS_RDONLY | ns._EMPTY_SOURCE_FLAGS,
        ),
        (os.fsencode(tmp_path / "spack-empty-host-dirs/0"), os.fsencode(target), ns.MS_BIND),
    ]


@pytest.mark.skipif(sys.platform != "linux", reason="Linux namespaces")
def test_live_mask_sources_remain_empty_after_stage_write_grant(tmp_path):
    if not ns.namespace_sandbox_available():
        pytest.skip("unprivileged namespaces unavailable")
    target = tmp_path / "host"
    target.mkdir()
    stage = tmp_path / "stage"
    stage.mkdir()
    code = """
import errno
import os
import sys
from pathlib import Path
from spack.sandbox import LandlockSandbox
from spack.sandbox_namespaces import NamespaceSandbox

target = Path(sys.argv[1])
stage = Path(sys.argv[2])
sandbox = NamespaceSandbox(landlock_factory=LandlockSandbox)
assert sandbox.prepare_mount_tree([str(target)], str(stage))
source = stage / "spack-empty-host-dirs" / "0"
assert not list(source.iterdir())
assert not list(target.iterdir())
assert sandbox.drop_mount_authority()
sandbox.allow_write(stage)
sandbox.apply()
for path in (source / "source-write", target / "target-write"):
    try:
        path.write_text("must fail")
    except OSError as error:
        assert error.errno == errno.EROFS, error
    else:
        raise AssertionError("empty mask source is writable: {}".format(path))
assert not list(source.iterdir())
os._exit(0)
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(target), str(stage)],
        env=dict(os.environ, PYTHONPATH=os.pathsep.join(sys.path)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    assert not list(target.iterdir())


@pytest.mark.skipif(sys.platform != "linux", reason="Linux namespaces")
def test_live_preserved_directory_tree_is_read_only_without_landlock(tmp_path):
    if not ns.namespace_sandbox_available():
        pytest.skip("unprivileged namespaces unavailable")
    source = tmp_path / "source"
    source.mkdir()
    marker = source / "marker"
    marker.write_text("selected data")
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    stage = tmp_path / "stage"
    stage.mkdir()
    code = """
import errno
import os
import sys
from pathlib import Path
from spack.sandbox_namespaces import (
    NamespaceMountAccess,
    NamespaceMountRequest,
    NamespaceSandbox,
)

source = Path(sys.argv[1])
hidden = Path(sys.argv[2])
stage = Path(sys.argv[3])
sandbox = NamespaceSandbox()
request = NamespaceMountRequest(
    str(source), str(hidden / "selected"), NamespaceMountAccess.READ_ONLY
)
assert sandbox.prepare_mount_tree([str(hidden)], str(stage), [request])
assert sandbox.drop_mount_authority()
preserved = stage / "spack-preserved-host-paths" / "0"
restored = hidden / "selected"
assert (preserved / "marker").read_text() == "selected data"
assert (restored / "marker").read_text() == "selected data"
for path in (preserved / "write", restored / "write"):
    try:
        path.write_text("must fail")
    except OSError as error:
        assert error.errno == errno.EROFS, error
    else:
        raise AssertionError("read-only preserved mount is writable: {}".format(path))
os._exit(0)
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(source), str(hidden), str(stage)],
        env=dict(os.environ, PYTHONPATH=os.pathsep.join(sys.path)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    assert list(source.iterdir()) == [marker]
    assert not list(hidden.iterdir())


@pytest.mark.skipif(sys.platform != "linux", reason="Linux namespaces")
def test_live_preserved_file_is_read_only_without_landlock(tmp_path):
    if not ns.namespace_sandbox_available():
        pytest.skip("unprivileged namespaces unavailable")
    source = tmp_path / "source"
    source.write_text("selected data")
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    stage = tmp_path / "stage"
    stage.mkdir()
    code = """
import errno
import os
import sys
from pathlib import Path
from spack.sandbox_namespaces import (
    NamespaceMountAccess,
    NamespaceMountRequest,
    NamespaceSandbox,
)

source = Path(sys.argv[1])
hidden = Path(sys.argv[2])
stage = Path(sys.argv[3])
sandbox = NamespaceSandbox()
request = NamespaceMountRequest(
    str(source), str(hidden / "selected"), NamespaceMountAccess.READ_ONLY
)
assert sandbox.prepare_mount_tree([str(hidden)], str(stage), [request])
assert sandbox.drop_mount_authority()
preserved = stage / "spack-preserved-host-paths" / "0"
restored = hidden / "selected"
assert preserved.read_text() == "selected data"
assert restored.read_text() == "selected data"
for path in (preserved, restored):
    try:
        path.write_text("must fail")
    except OSError as error:
        assert error.errno == errno.EROFS, error
    else:
        raise AssertionError("read-only preserved file is writable: {}".format(path))
os._exit(0)
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(source), str(hidden), str(stage)],
        env=dict(os.environ, PYTHONPATH=os.pathsep.join(sys.path)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    assert source.read_text() == "selected data"
    assert not list(hidden.iterdir())


@pytest.mark.skipif(sys.platform != "linux", reason="Linux namespaces")
def test_live_writable_mount_remains_writable_without_landlock(tmp_path):
    if not ns.namespace_sandbox_available():
        pytest.skip("unprivileged namespaces unavailable")
    source = tmp_path / "source"
    source.mkdir()
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    stage = tmp_path / "stage"
    stage.mkdir()
    code = """
import os
import sys
from pathlib import Path
from spack.sandbox_namespaces import (
    NamespaceMountAccess,
    NamespaceMountRequest,
    NamespaceSandbox,
)

source = Path(sys.argv[1])
hidden = Path(sys.argv[2])
stage = Path(sys.argv[3])
sandbox = NamespaceSandbox()
request = NamespaceMountRequest(
    str(source), str(hidden / "selected"), NamespaceMountAccess.READ_WRITE
)
assert sandbox.prepare_mount_tree([str(hidden)], str(stage), [request])
assert sandbox.drop_mount_authority()
preserved = stage / "spack-preserved-host-paths" / "0"
restored = hidden / "selected"
(preserved / "preserved-write").write_text("preserved")
(restored / "restored-write").write_text("restored")
os._exit(0)
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(source), str(hidden), str(stage)],
        env=dict(os.environ, PYTHONPATH=os.pathsep.join(sys.path)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    assert (source / "preserved-write").read_text() == "preserved"
    assert (source / "restored-write").read_text() == "restored"
    assert not list(hidden.iterdir())


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
