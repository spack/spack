# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Namespace unit tests never modify the test runner's namespaces or /proc."""

import errno
import io
import os
import select
import shutil
import subprocess
import sys
import tarfile
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from typing import cast

import pytest

import spack.build_environment
import spack.error
import spack.installer.build as build
import spack.sandbox
import spack.sandbox_namespaces as ns
import spack.spec
import spack.util.tty


@pytest.fixture(autouse=True)
def reset_namespace_probe_result(monkeypatch):
    monkeypatch.setattr(ns, "_namespace_probe_result", None)


class FakeLibc:
    def __init__(self):
        self.unshare_calls = []
        self.mount_calls = []
        self.mount_setattr_calls = []
        self.mount_setattr_attributes = []

    def unshare(self, flags):
        self.unshare_calls.append(flags.value)
        return 0

    def mount(self, source, target, filesystemtype, flags, data):
        self.mount_calls.append((source, target, flags.value))
        return 0

    def mount_setattr(self, directory_fd, path, flags, attributes, size):
        self.mount_setattr_calls.append((directory_fd.value, path, flags.value))
        self.mount_setattr_attributes.append((attributes._obj.attr_set, attributes._obj.attr_clr))
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


def test_network_namespace_requires_mount_namespace_and_initializes_loopback(
    namespace_setup, monkeypatch
):
    libc, _ = namespace_setup
    monkeypatch.setattr(ns, "_network_namespace_entered_pids", set())
    configured = []
    monkeypatch.setattr(ns, "_configure_loopback", lambda: configured.append("loopback"))

    with pytest.raises(ns.NamespaceSetupError, match="mount namespace is required"):
        ns._enter_network_namespace(libc)

    ns._enter_user_mount_namespace(libc)
    ns._enter_network_namespace(libc)
    ns._enter_network_namespace(libc)
    assert libc.unshare_calls == [ns.CLONE_NEWUSER | ns.CLONE_NEWNS, ns.CLONE_NEWNET]
    assert configured == ["loopback"]


@pytest.mark.skipif(sys.platform != "linux", reason="Linux network namespace setup")
@pytest.mark.parametrize("failure", ["ipv4", "ipv6", "unix"])
def test_loopback_configuration_reports_socket_failure(monkeypatch, failure):
    import fcntl
    import socket

    class Endpoint:
        def __init__(self, family):
            self.family = family

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def fileno(self):
            return 1

        def bind(self, address):
            self.address = address

        def getsockname(self):
            if (failure == "ipv4" and self.family == socket.AF_INET) or (
                failure == "ipv6" and self.family == socket.AF_INET6
            ):
                return ("invalid", 0)
            return self.address

        def sendall(self, data):
            pass

        def recv(self, size):
            return b"invalid"

        def close(self):
            pass

    monkeypatch.setattr(fcntl, "ioctl", lambda *args: None)
    monkeypatch.setattr(socket, "socket", lambda family, kind: Endpoint(family))
    monkeypatch.setattr(socket, "has_ipv6", True)
    monkeypatch.setattr(
        socket, "socketpair", lambda *args: (Endpoint(socket.AF_UNIX), Endpoint(socket.AF_UNIX))
    )
    with pytest.raises(ns.NamespaceSetupError) as error:
        ns._configure_loopback()
    assert error.value.operation == "configure network namespace loopback"
    assert error.value.errno == (errno.EIO if failure == "unix" else errno.EADDRNOTAVAIL)


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


def test_read_only_view_allows_writable_descendant(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    (hidden / "cache").mkdir()
    read_only_source = tmp_path / "read-only-source"
    writable_source = read_only_source / "writable"
    writable_source.mkdir(parents=True)

    policy = ns.build_namespace_filesystem_policy(
        [str(hidden)],
        read_only_mounts=[(str(read_only_source), str(hidden / "cache"))],
        read_write_mounts=[(str(writable_source), str(hidden / "cache" / "writable"))],
        read_only_view=True,
    )
    plan = ns.build_namespace_mount_plan_from_policy(policy, str(tmp_path / "stage"))

    assert [mount.target for mount in plan.restoration_mounts] == [
        str(hidden / "cache"),
        str(hidden / "cache" / "writable"),
    ]


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


def test_filesystem_policy_compiles_private_shared_memory(tmp_path):
    hidden = tmp_path / "dev"
    hidden.mkdir()
    shared_memory = str(hidden / "shm")
    descriptor_link = ns.NamespaceGeneratedSymlink(str(hidden / "fd"), "/proc/self/fd")
    policy = ns.build_namespace_filesystem_policy(
        [str(hidden)],
        generated_symlinks=[descriptor_link],
        tmpfs_paths=[shared_memory],
        read_only_view=True,
    )
    plan = ns.build_namespace_mount_plan_from_policy(policy, str(tmp_path / "scratch"))
    assert plan.tmpfs_paths == (shared_memory,)
    assert plan.generated_symlinks == (descriptor_link,)
    libc = FakeLibc()
    assert ns._apply_namespace_mount_plan(plan, libc)
    assert os.readlink(tmp_path / "scratch/spack-empty-host-dirs/0/fd") == "/proc/self/fd"
    assert (tmp_path / "scratch/spack-empty-host-dirs/0/shm").is_dir()
    assert libc.mount_calls[-1] == (
        b"tmpfs",
        os.fsencode(shared_memory),
        ns.MS_NOSUID | ns.MS_NODEV,
    )
    assert libc.mount_setattr_calls[0] == (ns.AT_FDCWD, b"/", ns.AT_RECURSIVE)


@pytest.mark.parametrize(
    "invalid",
    [
        "relative",
        "dotdot",
        "outside",
        "root",
        "duplicate",
        "nested",
        "restored",
        "generated",
        "symlink",
        "replacement",
    ],
)
def test_private_tmpfs_policy_rejects_conflicts(tmp_path, invalid):
    hidden = tmp_path / "dev"
    hidden.mkdir()
    shared_memory = str(hidden / "shm")
    options = {}
    paths = [shared_memory]
    if invalid == "relative":
        paths = ["dev/shm"]
    elif invalid == "dotdot":
        paths = [str(hidden / ".." / "shm")]
    elif invalid == "outside":
        paths = [str(tmp_path / "outside")]
    elif invalid == "root":
        paths = [str(hidden)]
    elif invalid == "duplicate":
        paths *= 2
    elif invalid == "nested":
        paths.append(shared_memory + "/child")
    elif invalid == "restored":
        options["read_write_mounts"] = [(str(tmp_path), shared_memory)]
    elif invalid == "generated":
        options["generated_paths"] = [ns.NamespaceGeneratedPath(shared_memory, True)]
    elif invalid == "symlink":
        options["generated_symlinks"] = [
            ns.NamespaceGeneratedSymlink(shared_memory, "/proc/self/fd")
        ]
    elif invalid == "replacement":
        options["replacement_mounts"] = [(str(tmp_path), str(hidden))]
    with pytest.raises(ns.NamespaceSetupError):
        ns.build_namespace_filesystem_policy([str(hidden)], tmpfs_paths=paths, **options)


def test_private_tmpfs_handbuilt_policy_revalidated_before_entry(tmp_path, monkeypatch):
    hidden = tmp_path / "dev"
    hidden.mkdir()
    policy = ns.NamespaceFilesystemPolicy((str(hidden),), tmpfs_paths=("relative",))
    monkeypatch.setattr(ns, "_enter_user_mount_namespace", lambda *args: pytest.fail("entered"))
    with pytest.raises(ns.NamespaceSetupError, match="invalid tmpfs path"):
        ns.NamespaceSandbox().prepare_filesystem_policy(policy, str(tmp_path / "scratch"))


def test_filesystem_policy_compiles_replacement_and_generated_alias(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    replacement = tmp_path / "replacement"
    replacement.mkdir()
    compiler = tmp_path / "compiler"
    compiler.touch()
    alias = hidden / "cc"
    alias.symlink_to(compiler)
    stage = tmp_path / "stage"
    policy = ns.build_namespace_filesystem_policy(
        [str(hidden)],
        replacement_mounts=[(str(replacement), str(hidden))],
        generated_symlinks=[ns.NamespaceGeneratedSymlink(str(alias), str(compiler))],
    )

    plan = ns.build_namespace_mount_plan_from_policy(policy, str(stage))

    preserved_source = str(stage / "spack-preserved-host-paths" / "replacement-0")
    assert plan.preserved_mounts == (
        ns.NamespacePreservedMount(
            str(replacement), preserved_source, True, ns.NamespaceMountAccess.READ_WRITE
        ),
    )
    assert plan.replacement_mounts == (
        ns.NamespacePreservedMount(
            preserved_source, str(hidden), True, ns.NamespaceMountAccess.READ_WRITE
        ),
    )
    assert plan.generated_symlinks == (
        ns.NamespaceGeneratedSymlink(str(alias), str(compiler.resolve())),
    )
    assert ns._apply_namespace_mount_plan(plan, FakeLibc())
    generated_alias = stage / "spack-empty-host-dirs/0/cc"
    assert generated_alias.is_symlink()
    assert os.readlink(str(generated_alias)) == str(compiler.resolve())


@pytest.mark.parametrize(
    "invalid, message, error_number",
    [
        ("missing-replacement", "replacement source does not exist", errno.ENOENT),
        ("file-replacement", "replacement source is not a directory", errno.ENOTDIR),
        ("relative-alias", "invalid generated symlink", errno.EINVAL),
        ("outside-alias", "generated symlink is not below a hidden root", errno.EINVAL),
    ],
)
def test_filesystem_policy_rejects_invalid_replacements_and_aliases(
    tmp_path, invalid, message, error_number
):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    source = tmp_path / "source"
    replacements = []
    aliases = []
    if invalid.endswith("replacement"):
        if invalid == "file-replacement":
            source.touch()
        replacements = [(str(source), str(hidden))]
    elif invalid == "relative-alias":
        aliases = [ns.NamespaceGeneratedSymlink(str(hidden / "cc"), "relative-compiler")]
    else:
        source.touch()
        aliases = [ns.NamespaceGeneratedSymlink(str(tmp_path / "outside"), str(source))]

    with pytest.raises(ns.NamespaceSetupError, match=message) as caught:
        ns.build_namespace_filesystem_policy(
            [str(hidden)], replacement_mounts=replacements, generated_symlinks=aliases
        )
    assert caught.value.errno == error_number


def test_filesystem_policy_rejects_forged_replacement_access(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    source = tmp_path / "source"
    source.mkdir()
    policy = ns.NamespaceFilesystemPolicy(
        (str(hidden),),
        replacement_mounts=(
            ns.NamespaceMountRequest(str(source), str(hidden), ns.NamespaceMountAccess.READ_ONLY),
        ),
    )

    with pytest.raises(ns.NamespaceSetupError, match="invalid replacement mount") as caught:
        ns.build_namespace_mount_plan_from_policy(policy, str(tmp_path / "stage"))
    assert caught.value.operation == "validate namespace policy access"


def test_filesystem_policy_rejects_replacement_outside_hidden_root(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    replacement = tmp_path / "replacement"
    replacement.mkdir()

    with pytest.raises(ns.NamespaceSetupError, match="replacement target is not a hidden root"):
        ns.build_namespace_filesystem_policy(
            [str(hidden)], replacement_mounts=[(str(replacement), str(tmp_path))]
        )


@pytest.mark.parametrize("worker_pid", [0, -1, "invalid"])
def test_mount_scratch_rejects_invalid_worker(tmp_path, worker_pid):
    lease = ns.NamespaceMountPlanScratch(str(tmp_path))
    with pytest.raises(ns.NamespaceSetupError, match="invalid worker PID"):
        lease.attach_worker(worker_pid)
    assert lease.worker_pid is None


def test_mount_scratch_rejects_replacing_attached_worker(tmp_path):
    lease = ns.NamespaceMountPlanScratch(str(tmp_path))
    worker_pid = os.getpid() + 1
    lease.attach_worker(worker_pid)
    with pytest.raises(ns.NamespaceSetupError, match="worker already attached"):
        lease.attach_worker(worker_pid + 1)
    assert lease.worker_pid == worker_pid


def test_mount_plan_scratch_is_private_and_concurrent(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    source = tmp_path / "source"
    source.mkdir()
    replacement = tmp_path / "replacement"
    replacement.mkdir()
    stage = tmp_path / "stage"
    prefix = tmp_path / "prefix"
    writable = tmp_path / "writable"
    policy = ns.build_namespace_filesystem_policy(
        [str(hidden)],
        [(str(source), str(hidden / "selected"))],
        replacement_mounts=[(str(replacement), str(hidden))],
    )

    def allocate():
        return ns.allocate_namespace_mount_plan_scratch(
            policy, str(stage), [str(prefix), str(writable)], str(tmp_path)
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        scratches = list(executor.map(lambda _: allocate(), range(2)))

    assert scratches[0].path != scratches[1].path
    for scratch in scratches:
        assert scratch.path.startswith(str(tmp_path) + os.sep)
        assert os.stat(scratch.path).st_mode & 0o777 == 0o700
        for excluded in (hidden, source, replacement, stage, prefix, writable):
            assert os.path.commonpath((scratch.path, str(excluded))) not in (
                scratch.path,
                str(excluded),
            )
        scratch.cleanup()


def test_mount_plan_scratch_rejects_symlinked_base_and_collisions(tmp_path, monkeypatch):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    real_base = tmp_path / "real-base"
    real_base.mkdir()
    symlinked_base = tmp_path / "symlinked-base"
    symlinked_base.symlink_to(real_base, target_is_directory=True)
    policy = ns.build_namespace_filesystem_policy([str(hidden)])

    with pytest.raises(ns.NamespaceSetupError, match="scratch base is symlinked"):
        ns.allocate_namespace_mount_plan_scratch(
            policy, str(tmp_path / "stage"), base_path=str(symlinked_base)
        )

    scratch = ns.allocate_namespace_mount_plan_scratch(
        policy, str(tmp_path / "stage"), base_path=str(real_base)
    )
    monkeypatch.setattr(ns.tempfile, "mkdtemp", lambda **kwargs: scratch.path)
    with pytest.raises(ns.NamespaceSetupError, match="scratch allocation collision"):
        ns.allocate_namespace_mount_plan_scratch(
            policy, str(tmp_path / "stage"), base_path=str(real_base)
        )
    scratch.cleanup()


def test_mount_plan_scratch_cleanup_rejects_live_worker_and_replacement(tmp_path):
    (tmp_path / "hidden").mkdir()
    policy = ns.build_namespace_filesystem_policy([str(tmp_path / "hidden")])
    scratch = ns.allocate_namespace_mount_plan_scratch(
        policy, str(tmp_path / "stage"), base_path=str(tmp_path)
    )
    worker = subprocess.Popen(
        [sys.executable, "-c", "import os; os.read(0, 1)"], stdin=subprocess.PIPE
    )
    try:
        scratch.attach_worker(worker.pid)
        with pytest.raises(ns.NamespaceSetupError, match="worker is still alive"):
            scratch.cleanup()
    finally:
        worker.terminate()
        worker.wait()

    moved = tmp_path / "moved-scratch"
    os.rename(scratch.path, moved)
    os.symlink(moved, scratch.path)
    with pytest.raises(ns.NamespaceSetupError, match="scratch path changed type"):
        scratch.cleanup()
    os.unlink(scratch.path)
    os.rmdir(moved)
    scratch.cleanup()


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


def test_read_only_view_restores_explicit_writable_mounts(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    read_only_source = tmp_path / "read-only-source"
    read_only_source.mkdir()
    read_write_source = tmp_path / "read-write-source"
    read_write_source.mkdir()
    policy = ns.build_namespace_filesystem_policy(
        [str(hidden)],
        [(str(read_only_source), str(hidden / "read-only"))],
        [(str(read_write_source), str(hidden / "read-write"))],
        read_only_view=True,
    )

    plan = ns.build_namespace_mount_plan_from_policy(policy, str(tmp_path / "stage"))
    libc = FakeLibc()
    assert ns._apply_namespace_mount_plan(plan, libc)
    assert plan.read_only_view
    assert libc.mount_setattr_calls[0] == (ns.AT_FDCWD, b"/", ns.AT_RECURSIVE)
    assert libc.mount_setattr_attributes[0] == (ns.MOUNT_ATTR_RDONLY, 0)
    assert (0, ns.MOUNT_ATTR_RDONLY) in libc.mount_setattr_attributes


def test_read_only_view_restores_writable_mount_outside_hidden_roots(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    writable = tmp_path / "writable"
    writable.mkdir()
    policy = ns.build_namespace_filesystem_policy(
        [str(hidden)], read_write_mounts=[(str(writable), str(writable))], read_only_view=True
    )

    plan = ns.build_namespace_mount_plan_from_policy(policy, str(tmp_path / "stage"))
    libc = FakeLibc()
    assert ns._apply_namespace_mount_plan(plan, libc)
    assert plan.restoration_mounts[-1].target == str(writable)
    assert libc.mount_setattr_calls[0] == (ns.AT_FDCWD, b"/", ns.AT_RECURSIVE)
    assert (0, ns.MOUNT_ATTR_RDONLY) in libc.mount_setattr_attributes


def test_writable_mount_outside_hidden_roots_requires_read_only_view(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    writable = tmp_path / "writable"
    writable.mkdir()
    policy = ns.build_namespace_filesystem_policy(
        [str(hidden)], read_write_mounts=[(str(writable), str(writable))]
    )

    with pytest.raises(ns.NamespaceSetupError, match="not below a hidden root"):
        ns.build_namespace_mount_plan_from_policy(policy, str(tmp_path / "stage"))


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


@pytest.mark.skipif(sys.platform != "linux", reason="Linux namespaces")
def test_disposable_namespace_compiler_and_source_build_evidence(tmp_path):
    """Exercise a compiled read-only policy with real compiler and source-build tools."""
    if not ns.namespace_sandbox_available():
        pytest.skip("unprivileged namespaces unavailable")
    cc = shutil.which("cc")
    make = shutil.which("make")
    tar = shutil.which("tar")
    if cc is None or make is None or tar is None:
        pytest.skip("C compiler, make, and tar are required for namespace build evidence")
    cxx = shutil.which("c++")
    fortran = shutil.which("gfortran")
    git = shutil.which("git")
    clang = shutil.which("clang")
    clangxx = shutil.which("clang++")

    source = tmp_path / "source"
    source.mkdir()
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    mount_plan_stage = tmp_path / "mount-plan"
    mount_plan_stage.mkdir()
    archive_source = tmp_path / "archive-source"
    archive_source.mkdir()
    (archive_source / "hello.c").write_text(
        '#include <stdio.h>\nint main(void) { puts("namespace-build"); return 0; }\n'
    )
    (archive_source / "configure").write_text(
        "#!/bin/sh\n"
        "cat > Makefile <<'EOF'\n"
        "all: hello\n"
        "hello: hello.c\n"
        "\t$(CC) hello.c -o hello\n"
        "EOF\n"
    )
    (archive_source / "configure").chmod(0o755)
    archive = tmp_path / "hello.tar"
    with tarfile.open(archive, "w") as stream:
        stream.add(archive_source / "hello.c", arcname="hello.c")
        stream.add(archive_source / "configure", arcname="configure")

    policy = ns.build_namespace_filesystem_policy(
        [str(hidden)],
        read_write_mounts=[(str(source), str(hidden / "stage"))],
        read_only_view=True,
    )
    plan = ns.build_namespace_mount_plan_from_policy(policy, str(mount_plan_stage))
    assert plan.read_only_view

    code = """
import os
import subprocess
import sys
from pathlib import Path
from spack.sandbox_namespaces import NamespaceSandbox, build_namespace_filesystem_policy

hidden = Path(sys.argv[1])
archive = Path(sys.argv[2])
mount_plan_stage = sys.argv[3]
cc = sys.argv[4]
cxx = sys.argv[5]
fortran = sys.argv[6]
git = sys.argv[7]
tar = sys.argv[8]
make = sys.argv[9]
clang = sys.argv[10]
clangxx = sys.argv[11]
stage = hidden / "stage"
policy = build_namespace_filesystem_policy(
    [str(hidden)],
    read_write_mounts=[(str(Path(sys.argv[12])), str(stage))],
    read_only_view=True,
)
sandbox = NamespaceSandbox()
assert sandbox.prepare_filesystem_policy(policy, mount_plan_stage)
assert sandbox.drop_mount_authority()
environment = dict(os.environ)
environment.update(
    TMPDIR=str(stage),
    TMP=str(stage),
    TEMP=str(stage),
    HOME=str(stage),
    XDG_CACHE_HOME=str(stage / "cache"),
    CC=cc,
)
(stage / "cache").mkdir()
if git:
    subprocess.run([git, "--version"], check=True, env=environment)
subprocess.run([tar, "-xf", str(archive), "-C", str(stage)], check=True, env=environment)
subprocess.run(["/bin/sh", "configure"], check=True, cwd=str(stage), env=environment)
subprocess.run([make, "-C", str(stage)], check=True, env=environment)
subprocess.run([cc, "hello.c", "-o", "hello-cc"], check=True, cwd=str(stage), env=environment)
if cxx or clangxx:
    (stage / "hello.cpp").write_text("int main() { return 0; }" + chr(10))
if cxx:
    subprocess.run(
        [cxx, "hello.cpp", "-o", "hello-cxx"], check=True, cwd=str(stage), env=environment
    )
if fortran:
    (stage / "hello.f90").write_text("program hello" + chr(10) + "end program hello" + chr(10))
    subprocess.run(
        [fortran, "hello.f90", "-o", "hello-fortran"],
        check=True,
        cwd=str(stage),
        env=environment,
    )
if clang:
    subprocess.run(
        [clang, "hello.c", "-o", "hello-clang"], check=True, cwd=str(stage), env=environment
    )
if clangxx:
    subprocess.run(
        [clangxx, "hello.cpp", "-o", "hello-clangxx"],
        check=True,
        cwd=str(stage),
        env=environment,
    )
assert (stage / "hello").exists()
assert (stage / "hello-cc").exists()
if cxx:
    assert (stage / "hello-cxx").exists()
if fortran:
    assert (stage / "hello-fortran").exists()
if clang:
    assert (stage / "hello-clang").exists()
if clangxx:
    assert (stage / "hello-clangxx").exists()
os._exit(0)
"""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            code,
            str(hidden),
            str(archive),
            str(mount_plan_stage),
            cc,
            cxx or "",
            fortran or "",
            git or "",
            tar or "",
            make,
            clang or "",
            clangxx or "",
            str(source),
        ],
        env=dict(os.environ, PYTHONPATH=os.pathsep.join(sys.path)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert (source / "hello").exists()
    assert (source / "hello-cc").exists()
    if cxx:
        assert (source / "hello-cxx").exists()
    if fortran:
        assert (source / "hello-fortran").exists()
    if clang:
        assert (source / "hello-clang").exists()
    if clangxx:
        assert (source / "hello-clangxx").exists()


@pytest.mark.skipif(sys.platform != "linux", reason="Linux namespaces")
def test_live_read_only_view_rejects_passthrough_writes(tmp_path):
    if not ns.namespace_sandbox_available():
        pytest.skip("unprivileged namespaces unavailable")
    passthrough = tmp_path / "passthrough"
    passthrough.mkdir()
    writable_source = tmp_path / "writable-source"
    writable_source.mkdir()
    writable_passthrough = tmp_path / "writable-passthrough"
    writable_passthrough.mkdir()
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    stage = tmp_path / "stage"
    stage.mkdir()
    code = """
import errno
import os
import sys
from pathlib import Path
from spack.sandbox_namespaces import NamespaceSandbox, build_namespace_filesystem_policy

passthrough = Path(sys.argv[1])
writable_source = Path(sys.argv[2])
writable_passthrough = Path(sys.argv[3])
hidden = Path(sys.argv[4])
stage = Path(sys.argv[5])
policy = build_namespace_filesystem_policy(
    [str(hidden)],
    read_write_mounts=[
        (str(writable_source), str(hidden / "writable")),
        (str(writable_passthrough), str(writable_passthrough)),
    ],
    read_only_view=True,
)
sandbox = NamespaceSandbox()
assert sandbox.prepare_filesystem_policy(policy, str(stage))
assert sandbox.drop_mount_authority()
try:
    (passthrough / "must-fail").write_text("must fail")
except OSError as error:
    assert error.errno == errno.EROFS, error
else:
    raise AssertionError("inherited passthrough tree remained writable")
(hidden / "writable" / "must-work").write_text("writable")
(writable_passthrough / "must-also-work").write_text("writable passthrough")
os._exit(0)
"""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            code,
            str(passthrough),
            str(writable_source),
            str(writable_passthrough),
            str(hidden),
            str(stage),
        ],
        env=dict(os.environ, PYTHONPATH=os.pathsep.join(sys.path)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    assert not (passthrough / "must-fail").exists()
    assert (writable_source / "must-work").read_text() == "writable"
    assert (writable_passthrough / "must-also-work").read_text() == "writable passthrough"
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
    monkeypatch.setattr(sandbox, "prepare_network_namespace", lambda: True)
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


@pytest.mark.parametrize("failure", ["symlink", "tmpfs"])
def test_private_device_setup_failure_stops_before_tee(
    namespace_setup, monkeypatch, tmp_path, failure
):
    libc, _ = namespace_setup
    hidden = tmp_path / "dev"
    hidden.mkdir()
    worker = tmp_path / "worker"
    worker.mkdir()
    policy = ns.build_namespace_filesystem_policy(
        [str(hidden)],
        read_write_mounts=[(str(worker), str(worker))],
        generated_symlinks=[ns.NamespaceGeneratedSymlink(str(hidden / "fd"), "/proc/self/fd")],
        tmpfs_paths=[str(hidden / "shm")],
        read_only_view=True,
    )
    sandbox = ns.NamespaceSandbox(cast(ns.ctypes.CDLL, libc))
    acquisitions = []
    monkeypatch.setattr(
        spack.sandbox, "get_sandbox", lambda: acquisitions.append(sandbox) or sandbox
    )
    monkeypatch.setattr(
        sandbox, "drop_mount_authority", lambda: pytest.fail("drop after failed setup")
    )
    monkeypatch.setattr(build, "Tee", lambda *args: pytest.fail("Tee after failed setup"))

    def fail(*args, **kwargs):
        raise OSError(errno.EPERM, "D3 setup denied")

    if failure == "symlink":
        monkeypatch.setattr(ns.os, "symlink", fail)
    else:
        monkeypatch.setattr(ns, "_mount_private_tmpfs", fail)
    inherited_environment = dict(os.environ)
    inherited_tempdir = build.tempfile.tempdir
    activation = build.NamespaceActivation(policy, str(tmp_path / "scratch"), str(worker))
    channel = cast(build.IpcChannel, None)
    with pytest.raises(OSError, match="D3 setup denied"):
        build._start_tee_after_namespace(
            {"enable": True},
            channel,
            None,
            channel,
            "build.log",
            spack.spec.Spec(),
            str(tmp_path),
            activation,
        )
    assert acquisitions == [sandbox]
    assert not sandbox.filesystem_policy_active
    assert not sandbox.namespace_ready
    assert os.environ == inherited_environment
    assert build.tempfile.tempdir == inherited_tempdir
    assert not list(worker.iterdir())


@pytest.mark.parametrize("failure", [None, "policy", "authority"])
def test_active_namespace_policy_skips_landlock(monkeypatch, tmp_path, failure):
    calls = []
    worker_root = tmp_path / "worker with spaces"
    worker_root.mkdir()
    monkeypatch.setattr(os, "environ", dict(os.environ, JAVA_TOOL_OPTIONS="-Xmx256m"))
    monkeypatch.setattr(build.tempfile, "tempdir", "/inherited-temp")
    inherited_environment = dict(os.environ)

    class RecordingSandbox(ns.NamespaceSandbox):
        def prepare_filesystem_policy(self, policy, stage_path):
            calls.append(("prepare policy", policy, stage_path))
            self._filesystem_policy_active = True
            return failure != "policy"

        def drop_mount_authority(self):
            calls.append(("drop mount authority",))
            return failure != "authority"

        def prepare_network_namespace(self):
            calls.append(("prepare network namespace",))
            return True

        def allow_read(self, path):
            calls.append(("read", path))

        def allow_write(self, path):
            calls.append(("write", path))

        def apply(self, block_network=False):
            calls.append(("apply", block_network))

    sandbox = RecordingSandbox()
    monkeypatch.setattr(spack.sandbox, "get_sandbox", lambda: sandbox)
    monkeypatch.setattr(
        ns, "freeze_namespace_sandbox_capability", lambda: ns.NamespaceCapability(True, None, None)
    )
    spec = spack.spec.Spec()
    channel = cast(build.IpcChannel, None)
    policy = ns.build_namespace_filesystem_policy(
        [], read_write_mounts=[(str(worker_root), str(worker_root))], read_only_view=True
    )
    activation = build.NamespaceActivation(policy, str(tmp_path / "mount-plan"), str(worker_root))

    def start_tee(*args):
        spack.build_environment.clean_environment().apply_modifications()
        assert os.environ["HOME"] == str(worker_root / "home")
        assert os.environ["XDG_CACHE_HOME"] == str(worker_root / "cache")
        for variable in ("TMPDIR", "TMP", "TEMP"):
            assert os.environ[variable] == str(worker_root / "tmp")
        assert build.tempfile.gettempdir() == str(worker_root / "tmp")
        assert os.environ["JAVA_TOOL_OPTIONS"].startswith("-Xmx256m ")
        assert build.shlex.split(os.environ["JAVA_TOOL_OPTIONS"])[1:] == [
            f"-Duser.home={worker_root / 'home'}",
            f"-Djava.io.tmpdir={worker_root / 'tmp'}",
        ]
        for name in ("home", "cache", "tmp"):
            assert (worker_root / name).is_dir()
        calls.append(("tee",))
        return object()

    monkeypatch.setattr(build, "Tee", start_tee)

    if failure == "policy":
        with pytest.raises(spack.error.InstallError):
            build._start_tee_after_namespace(
                {"enable": True},
                channel,
                None,
                channel,
                "build.log",
                spec,
                str(tmp_path),
                activation,
            )
        assert os.environ == inherited_environment
        assert build.tempfile.tempdir == "/inherited-temp"
        assert not list(worker_root.iterdir())
        assert ("tee",) not in calls
        return

    _, prepared = build._start_tee_after_namespace(
        {"enable": True}, channel, None, channel, "build.log", spec, str(tmp_path), activation
    )
    assert prepared is sandbox
    assert not sandbox.network_namespace_active
    if failure == "authority":
        with pytest.raises(spack.error.InstallError):
            build._enable_sandbox({"enable": True}, spec, str(tmp_path), sandbox=sandbox)
        assert calls[-3:] == [("tee",), ("prepare network namespace",), ("drop mount authority",)]
        return

    build._enable_sandbox({"enable": True}, spec, str(tmp_path), sandbox=sandbox)
    assert calls == [
        ("prepare policy", activation.policy, activation.mount_plan_stage),
        ("tee",),
        ("prepare network namespace",),
        ("drop mount authority",),
    ]


@pytest.mark.parametrize(
    "invalid", ["missing", "file", "symlink", "relative", "dotdot", "unselected"]
)
def test_namespace_worker_root_validation(tmp_path, invalid):
    root = tmp_path / "worker"
    root.mkdir()
    policy = ns.build_namespace_filesystem_policy(
        [], read_write_mounts=[(str(root), str(root))], read_only_view=True
    )
    if invalid == "missing":
        root.rmdir()
    elif invalid == "file":
        root.rmdir()
        root.touch()
    elif invalid == "symlink":
        alias = tmp_path / "alias"
        alias.symlink_to(root)
        root = alias
    elif invalid == "relative":
        root = os.path.relpath(root)
    elif invalid == "dotdot":
        root = root / ".." / "worker"
    elif invalid == "unselected":
        root = tmp_path
    activation = build.NamespaceActivation(policy, str(tmp_path / "scratch"), str(root))
    with pytest.raises((spack.error.InstallError, ns.NamespaceSetupError)):
        build._validate_namespace_worker_root(activation)


@pytest.mark.parametrize("name", ["home", "cache", "tmp"])
@pytest.mark.parametrize("existing", ["directory", "file", "symlink"])
def test_namespace_worker_environment_rejects_existing_paths(
    tmp_path, monkeypatch, name, existing
):
    root = tmp_path / "worker"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    target = root / name
    if existing == "directory":
        target.mkdir()
    elif existing == "file":
        target.touch()
    else:
        target.symlink_to(outside)
    monkeypatch.setattr(os, "environ", dict(os.environ))
    monkeypatch.setattr(build.tempfile, "tempdir", "/inherited-temp")
    inherited_environment = dict(os.environ)
    with pytest.raises(FileExistsError):
        build._configure_namespace_worker_environment(str(root))
    assert os.environ == inherited_environment
    assert build.tempfile.tempdir == "/inherited-temp"
    assert not list(outside.iterdir())


@pytest.mark.parametrize("enabled", [False, True])
def test_namespace_worker_environment_unchanged_for_fallback(tmp_path, monkeypatch, enabled):
    fallback = object()
    monkeypatch.setattr(spack.sandbox, "get_sandbox", lambda: fallback)
    monkeypatch.setattr(ns, "freeze_namespace_sandbox_capability", lambda: None)
    monkeypatch.setattr(os, "environ", dict(os.environ))
    monkeypatch.setattr(build.tempfile, "tempdir", "/inherited-temp")
    inherited_environment = dict(os.environ)
    sandbox = build._prepare_namespace_sandbox_before_threads(
        {"enable": enabled}, spack.spec.Spec(), str(tmp_path)
    )
    assert sandbox is (fallback if enabled else None)
    assert os.environ == inherited_environment
    assert build.tempfile.tempdir == "/inherited-temp"
    assert not list(tmp_path.iterdir())


@pytest.mark.skipif(sys.platform != "linux", reason="Linux namespaces")
def test_live_private_devices_and_concurrent_shared_memory(tmp_path):
    if not ns.namespace_sandbox_available():
        pytest.skip("unprivileged namespaces unavailable")
    code = """
import errno
import os
import stat
import sys
from pathlib import Path
from spack.installer import build
import spack.spec
import spack.sandbox_namespaces as ns

worker, scratch, host_shm, token = sys.argv[1:]
data = build._load_sandbox_policy()
devices = [(path, path) for path in data['device_nodes'] if os.path.exists(path)]
device_ids = {path: os.stat(path).st_rdev for path, _ in devices}
policy = ns.build_namespace_filesystem_policy(
    ['/dev'], read_write_mounts=devices + [(worker, worker)],
    generated_symlinks=[ns.NamespaceGeneratedSymlink(path, target)
                        for path, target in data['device_symlinks'].items()],
    tmpfs_paths=data['tmpfs_paths'], read_only_view=True,
)
sandbox = build._prepare_namespace_sandbox_before_threads(
    {'enable': True}, spack.spec.Spec(), worker,
    namespace_activation=build.NamespaceActivation(policy, scratch, worker),
)
assert sandbox.filesystem_policy_active
assert set(os.listdir('/dev')) == {
    Path(path).name for path, _ in devices
} | {'shm', 'fd', 'stdin', 'stdout', 'stderr'}
for path, device_id in device_ids.items():
    assert stat.S_ISCHR(os.stat(path).st_mode)
    assert os.stat(path).st_rdev == device_id
assert stat.S_IMODE(os.stat('/dev/shm').st_mode) == 0o1777
assert not os.path.exists(host_shm)
for path, target in data['device_symlinks'].items():
    assert os.readlink(path) == target
with open('/dev/null', 'wb') as stream:
    stream.write(b'discard')
with open('/dev/null', 'rb') as stream:
    assert stream.read(1) == b''
with open('/dev/zero', 'rb') as stream:
    assert stream.read(16) == bytes(16)
for path in ('/dev/random', '/dev/urandom'):
    descriptor = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    try:
        assert len(os.read(descriptor, 16)) == 16
    finally:
        os.close(descriptor)
descriptor = os.open('/dev/full', os.O_WRONLY)
try:
    try:
        os.write(descriptor, b'full')
    except OSError as error:
        assert error.errno == errno.ENOSPC
    else:
        raise AssertionError('/dev/full accepted write')
finally:
    os.close(descriptor)
with open('/dev/shm/spack-concurrent', 'x+') as stream:
    stream.write(token)
    stream.flush()
    with open('/dev/fd/' + str(stream.fileno())) as alias:
        assert alias.read() == token
    with open('/dev/stdout', 'w') as output:
        output.write('ready\\n')
    with open('/dev/stderr', 'w') as output:
        output.write('descriptor stderr\\n')
    with open('/dev/stdin') as input_stream:
        assert input_stream.readline() == 'release\\n'
    stream.seek(0)
    assert stream.read() == token
build._enable_sandbox(
    {'enable': True, 'allow_network': True}, spack.spec.Spec(), worker, sandbox=sandbox
)
status = Path('/proc/self/status').read_text().splitlines()
assert all(int(line.split()[1], 16) == 0 for line in status
           if line.startswith(('CapEff:', 'CapPrm:', 'CapInh:')))
try:
    sandbox.bind_mount(worker)
except ns.SandboxError:
    pass
else:
    raise AssertionError('mount authority retained')
os._exit(0)
"""
    processes = []
    with build.tempfile.NamedTemporaryFile(prefix="spack-host-shm-", dir="/dev/shm") as host:
        host.write(b"host-private")
        host.flush()
        try:
            for index in range(2):
                worker = tmp_path / f"worker-{index}"
                worker.mkdir()
                scratch = tmp_path / f"scratch-{index}"
                scratch.mkdir()
                processes.append(
                    subprocess.Popen(
                        [
                            sys.executable,
                            "-c",
                            code,
                            str(worker),
                            str(scratch),
                            host.name,
                            str(index),
                        ],
                        env=dict(os.environ, PYTHONPATH=os.pathsep.join(sys.path)),
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                    )
                )
            for process in processes:
                assert select.select([process.stdout], [], [], 20)[0], "worker never became ready"
                ready = process.stdout.readline()
                if ready != "ready\n":
                    _, errors = process.communicate(timeout=10)
                    pytest.fail(errors)
            for process in processes:
                _, errors = process.communicate("release\n", timeout=20)
                assert process.returncode == 0, errors
                assert errors == "descriptor stderr\n"
            host.seek(0)
            assert host.read() == b"host-private"
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                process.communicate(timeout=10)


@pytest.mark.skipif(sys.platform != "linux", reason="Linux namespaces")
def test_live_namespace_worker_environment(tmp_path):
    if not ns.namespace_sandbox_available():
        pytest.skip("unprivileged namespaces unavailable")
    hidden = tmp_path / "hidden-home"
    hidden.mkdir()
    secret = hidden / "host-secret"
    secret.write_text("private")
    stage_parent = hidden / "stage-parent"
    stage_parent.mkdir()
    stage_configure = stage_parent / "spack-stage-gmake" / "spack-src" / "configure"
    stage_configure.parent.mkdir(parents=True)
    stage_configure.write_text("stage source")
    worker_root = stage_parent / "worker with 'single' and \"double\" quotes"
    worker_root.mkdir()
    replacement = hidden
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    inherited_environment = dict(os.environ)
    inherited_tempdir = build.tempfile.tempdir
    code = """
import errno
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from spack.installer import build
from spack.sandbox_namespaces import (
    build_namespace_filesystem_policy, freeze_namespace_sandbox_capability,
)

hidden, stage_parent, root, replacement, scratch = map(Path, sys.argv[1:6])
policy = build_namespace_filesystem_policy(
    [str(hidden)],
    read_write_mounts=[(str(stage_parent), str(stage_parent))],
    replacement_mounts=[(str(root), str(replacement))],
    read_only_view=True,
)
activation = build.NamespaceActivation(policy, str(scratch), str(root))
assert freeze_namespace_sandbox_capability().available
os.environ['JAVA_TOOL_OPTIONS'] = '-Xmx64m -Duser.home=/old -Djava.io.tmpdir=/old'
os.environ.pop('_JAVA_OPTIONS', None)
os.environ.pop('JDK_JAVA_OPTIONS', None)
tempfile.tempdir = '/stale-parent-cache'

def start_tee(*args):
    for variable, name in (
        ('HOME', 'home'), ('XDG_CACHE_HOME', 'cache'),
        ('TMPDIR', 'tmp'), ('TMP', 'tmp'), ('TEMP', 'tmp'),
    ):
        path = Path(os.environ[variable])
        assert path == root / name, (variable, path, root / name)
        assert path.resolve() == path
        assert path.stat().st_mode & 0o777 == 0o700
        (path / variable).write_text('worker')
    generated = Path(tempfile.mkdtemp())
    assert generated.parent == root / 'tmp'
    with tempfile.NamedTemporaryFile() as temporary:
        assert Path(temporary.name).parent == root / 'tmp'
        temporary.write(b'worker')
    assert not (hidden / 'host-secret').exists()
    assert (
        (stage_parent / 'spack-stage-gmake' / 'spack-src' / 'configure').read_text()
        == 'stage source'
    )
    (replacement / 'private-temp').write_text('replacement')
    try:
        (root.parent.parent.parent / 'must-fail').write_text('denied')
    except OSError as error:
        assert error.errno == errno.EROFS
    else:
        raise AssertionError('inherited view remained writable')
    if sys.argv[6]:
        result = subprocess.run(
            [sys.argv[6], '-XshowSettings:properties', '-version'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10,
        )
        assert result.returncode == 0, result.stderr
        for property_name, directory in (('user.home', 'home'), ('java.io.tmpdir', 'tmp')):
            assert f'{property_name} = {root / directory}' in result.stderr, result.stderr
    return object()

build.Tee = start_tee
_, sandbox = build._start_tee_after_namespace(
    {'enable': True}, None, None, None, 'build.log', SimpleNamespace(),
    str(stage_parent), activation,
)
assert sandbox.filesystem_policy_active
os._exit(0)
"""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            code,
            str(hidden),
            str(stage_parent),
            str(worker_root),
            str(replacement),
            str(scratch),
            shutil.which("java") or "",
        ],
        env=dict(os.environ, PYTHONPATH=os.pathsep.join(sys.path)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert os.environ == inherited_environment
    assert build.tempfile.tempdir == inherited_tempdir
    assert secret.read_text() == "private"
    assert (worker_root / "private-temp").read_text() == "replacement"
    assert stage_configure.read_text() == "stage source"
    for name, variable in (("home", "HOME"), ("cache", "XDG_CACHE_HOME"), ("tmp", "TMPDIR")):
        assert (worker_root / name / variable).read_text() == "worker"


@pytest.mark.skipif(sys.platform != "linux", reason="Linux namespaces")
def test_live_network_namespace_loopback_and_unix_sockets(tmp_path):
    if not ns.namespace_sandbox_available():
        pytest.skip("user, mount, or network namespaces unavailable")
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    (hidden / "host-only").write_text("private")
    stage = tmp_path / "stage"
    stage.mkdir()
    socket_path = tmp_path / "local.sock"
    code = """
import os
import socket
import sys
from spack.sandbox_namespaces import NamespaceSandbox

hidden, stage, socket_path = sys.argv[1:]
host_net_namespace = os.stat('/proc/self/ns/net').st_ino
sandbox = NamespaceSandbox()
assert sandbox.prepare_mount_tree([hidden], stage)
assert not os.path.exists(os.path.join(hidden, 'host-only'))
assert sandbox.prepare_network_namespace()
assert os.stat('/proc/self/ns/net').st_ino != host_net_namespace
assert sandbox.drop_mount_authority()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ipv4:
    ipv4.bind(('127.0.0.1', 0))
    assert ipv4.getsockname()[0] == '127.0.0.1'
if socket.has_ipv6:
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as ipv6:
        ipv6.bind(('::1', 0))
        assert ipv6.getsockname()[0] == '::1'

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    server.bind(socket_path)
    server.listen(1)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(socket_path)
        connection, _ = server.accept()
        with connection:
            client.sendall(b'local socket works')
            assert connection.recv(64) == b'local socket works'
finally:
    server.close()
    os.unlink(socket_path)
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(hidden), str(stage), str(socket_path)],
        env=dict(os.environ, PYTHONPATH=os.pathsep.join(sys.path)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr


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


def test_pre_thread_setup_prepares_namespace_without_dropping_authority(monkeypatch, tmp_path):
    calls = []

    class RecordingSandbox(ns.NamespaceSandbox):
        def prepare_mount_tree(self, hidden_dirs, stage_path):
            calls.append(("prepare", hidden_dirs, stage_path))
            return True

        def drop_mount_authority(self):
            calls.append(("drop mount authority",))
            return True

        def prepare_network_namespace(self):
            calls.append(("prepare network namespace",))
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
        build._prepare_namespace_sandbox_before_threads(
            {"enable": True, "allow_network": False}, spec, str(tmp_path)
        )
        is sandbox
    )
    assert calls == [("freeze",), ("prepare", ["/usr/share/aclocal"], str(tmp_path))]


def test_pre_thread_setup_keeps_network_namespace_when_allowed(monkeypatch, tmp_path):
    calls = []

    class RecordingSandbox(ns.NamespaceSandbox):
        def prepare_mount_tree(self, hidden_dirs, stage_path):
            calls.append(("prepare",))
            return True

        def prepare_network_namespace(self):
            calls.append(("prepare network namespace",))

        def drop_mount_authority(self):
            calls.append(("drop mount authority",))
            return True

    sandbox = RecordingSandbox()
    monkeypatch.setattr(ns, "freeze_namespace_sandbox_capability", lambda: None)
    monkeypatch.setattr(spack.sandbox, "get_sandbox", lambda: sandbox)
    spec = SimpleNamespace(traverse=lambda **kwargs: [], prefix=tmp_path / "prefix")

    build._prepare_namespace_sandbox_before_threads(
        {"enable": True, "allow_network": True}, spec, str(tmp_path)
    )
    assert calls == [("prepare",)]


def test_staging_rejects_active_network_namespace():
    sandbox = ns.NamespaceSandbox()
    build._require_staging_network(sandbox)

    sandbox._network_namespace_ready = True
    with pytest.raises(spack.error.InstallError, match="inactive while staging"):
        build._require_staging_network(sandbox)


def test_namespace_policy_validation_precedes_namespace_mutation(monkeypatch, tmp_path):
    calls = []

    class RecordingSandbox(ns.NamespaceSandbox):
        def prepare_mount_tree(self, hidden_dirs, stage_path):
            calls.append(("prepare", hidden_dirs, stage_path))
            return True

    sandbox = RecordingSandbox()
    for name in ("hidden", "tool", "header", "runtime", "temporary"):
        (tmp_path / name).mkdir()
    selected_paths = build.NamespacePolicyInputPaths(
        hidden_roots=(str(tmp_path / "hidden"),),
        compiler_paths=(str(tmp_path / "missing-compiler"),),
        tool_paths=(str(tmp_path / "tool"),),
        header_paths=(str(tmp_path / "header"),),
        runtime_paths=(str(tmp_path / "runtime"),),
        temporary_paths=(str(tmp_path / "temporary"),),
    )
    monkeypatch.setattr(
        ns, "freeze_namespace_sandbox_capability", lambda: calls.append(("freeze",))
    )
    monkeypatch.setattr(spack.sandbox, "get_sandbox", lambda: sandbox)

    with pytest.raises(ns.NamespaceSetupError, match="missing-compiler"):
        build._prepare_namespace_sandbox_before_threads(
            {"enable": True},
            SimpleNamespace(prefix=tmp_path / "prefix", traverse=lambda **kwargs: []),
            str(tmp_path / "stage"),
            mount_plan_stage=str(tmp_path / "mount-plan"),
            selected_paths=selected_paths,
        )
    assert calls == []


def test_namespace_policy_validation_is_unconditional(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(
        build,
        "namespace_filesystem_policy_and_plan_from_inputs",
        lambda *args, **kwargs: calls.append((args, kwargs)) or ("policy", "plan"),
    )
    selected_paths = build.NamespacePolicyInputPaths((), (), (), (), (), ())

    assert build.validate_namespace_policy_before_threads(
        {},
        SimpleNamespace(),
        str(tmp_path / "stage"),
        str(tmp_path / "mount-plan"),
        selected_paths,
    )
    assert calls


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

        def prepare_network_namespace(self):
            calls.append(("prepare network namespace",))
            return True

        def apply(self, block_network=False):
            calls.append(("apply", block_network))

    sandbox = RecordingSandbox()
    monkeypatch.setattr(spack.sandbox, "get_sandbox", lambda: sandbox)
    dependency = (
        spack.spec.Spec("autoconf", external_path=str(tmp_path / "autoconf"))
        if external
        else SimpleNamespace(name="autoconf", external=False, prefix=tmp_path / "autoconf")
    )
    spec = SimpleNamespace(traverse=lambda **kw: [dependency], prefix=tmp_path / "prefix")
    build._enable_sandbox({"enable": True, "allow_network": False}, spec, str(tmp_path))
    assert calls[0] == ("prepare", hidden_dirs, str(tmp_path))
    if available:
        assert calls[1] == ("prepare network namespace",)
        assert calls[2] == ("drop mount authority",)
    else:
        assert ("prepare network namespace",) not in calls
    assert ("write", str(tmp_path)) in calls
    assert calls[-1] == ("apply", True)


def test_namespace_authority_drops_after_recipe_setup(monkeypatch, tmp_path):
    calls = []

    class RecordingSandbox(ns.NamespaceSandbox):
        def __init__(self):
            super().__init__()
            self._filesystem_policy_active = True

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
        lambda config, spec, stage_path: (calls.append(("prepare", stage_path)), sandbox)[-1],
    )
    monkeypatch.setattr(build, "Tee", lambda *args: calls.append(("tee", args)) or object())
    spec = SimpleNamespace(traverse=lambda **kw: [], prefix=tmp_path / "prefix")

    _, prepared_sandbox = build._start_tee_after_namespace(
        {"enable": True, "allow_network": True},
        "control-r",
        "control-w",
        "parent",
        "build.log",
        spec,
        str(tmp_path),
    )
    calls.append(("recipe-controlled setup",))
    build._enable_sandbox(
        {"enable": True, "allow_network": True}, spec, str(tmp_path), sandbox=prepared_sandbox
    )

    assert calls == [
        ("prepare", str(tmp_path)),
        ("tee", ("control-r", "control-w", "parent", "build.log")),
        ("recipe-controlled setup",),
        ("drop mount authority",),
    ]
    assert calls.count(("drop mount authority",)) == 1


@pytest.mark.parametrize("external", [False, True])
def test_default_mask_does_not_hide_tools(external):
    dependency = (
        spack.spec.Spec("autoconf", external_path="/opt/autoconf")
        if external
        else SimpleNamespace(name="autoconf", external=False)
    )
    spec = SimpleNamespace(traverse=lambda **kw: [dependency])
    assert build.configured_empty_directory_paths(cast(spack.spec.Spec, spec)) == (
        [] if external else ["/usr/share/aclocal"]
    )


# Phases 4-6 have no implementation tests yet. They cover the policy-driven
# mount tree, build-phase confinement, and concretizer-worker evaluation.
