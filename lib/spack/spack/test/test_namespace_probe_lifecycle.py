# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Process-lifecycle regressions for the disposable namespace probe."""

import builtins
import ctypes
import errno
import os
import subprocess
import sys

import pytest

import spack.sandbox_namespaces as ns


@pytest.fixture(autouse=True)
def reset_namespace_probe_result(monkeypatch):
    monkeypatch.setattr(ns, "_namespace_probe_result", None)
    monkeypatch.setattr(ns, "_network_namespace_entered_pids", set())
    monkeypatch.setattr(ns, "_enter_network_namespace", lambda libc: None)


@pytest.mark.skipif(not hasattr(os, "fork"), reason="requires fork")
def test_probe_child_cannot_return_to_caller_on_unexpected_error():
    # Run out of process: a broken probe must not duplicate the pytest runner.
    code = """
import spack.sandbox_namespaces as ns

def fail(*args, **kwargs):
    raise RuntimeError("unexpected setup failure")

ns._enter_user_mount_namespace = fail
try:
    result = ns._probe_namespace_capability(None)
except RuntimeError:
    print("escaped child", flush=True)
else:
    print("available=" + str(result.available), flush=True)
"""
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(sys.path))
    result = subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == "available=False\n"


def test_fork_failure_closes_pipe(monkeypatch):
    descriptors = os.pipe()
    monkeypatch.setattr(ns.os, "pipe", lambda: descriptors)

    def fail():
        raise OSError(errno.EAGAIN, "fork denied")

    monkeypatch.setattr(ns.os, "fork", fail, raising=False)
    try:
        with pytest.raises(OSError, match="fork denied"):
            ns._probe_namespace_capability(None)
        for fd in descriptors:
            with pytest.raises(OSError) as error:
                os.fstat(fd)
            assert error.value.errno == errno.EBADF
    finally:
        for fd in descriptors:
            try:
                os.close(fd)
            except OSError:
                pass


def test_read_failure_still_reaps_child(monkeypatch):
    reaped = []
    monkeypatch.setattr(ns.os, "fork", lambda: 12345, raising=False)
    monkeypatch.setattr(ns.os, "waitpid", lambda pid, options: reaped.append(pid), raising=False)

    def fail(*args):
        raise OSError(errno.EIO, "read failed")

    monkeypatch.setattr(ns.os, "read", fail)
    with pytest.raises(OSError, match="read failed"):
        ns._probe_namespace_capability(None)
    assert reaped == [12345]


def test_libc_failure_is_unavailable(monkeypatch):
    monkeypatch.setattr(ns.platform, "system", lambda: "Linux")
    attempts = []

    def fail(*args, **kwargs):
        attempts.append(None)
        raise OSError(errno.ENOENT, "libc unavailable")

    monkeypatch.setattr(ns.ctypes, "CDLL", fail)
    capability = ns.namespace_sandbox_capability()
    assert capability == ns.NamespaceCapability(False, "load libc", "libc unavailable")
    assert not ns.namespace_sandbox_available()
    assert len(attempts) == 2


def test_probe_without_fork(monkeypatch):
    monkeypatch.setattr(ns.os, "fork", None, raising=False)
    assert ns._probe_namespace_capability(None) == ns.NamespaceCapability(
        False, "fork", "os.fork is unavailable"
    )


def test_probe_off_linux(monkeypatch):
    monkeypatch.setattr(ns.platform, "system", lambda: "Windows")
    assert not ns.namespace_sandbox_available()


def test_capability_reports_failed_operation(monkeypatch):
    monkeypatch.setattr(ns.platform, "system", lambda: "Linux")
    monkeypatch.setattr(ns.ctypes, "CDLL", lambda *args, **kwargs: object())
    monkeypatch.setattr(
        ns,
        "_probe_namespace_capability",
        lambda libc: ns.NamespaceCapability(False, "write uid_map", "operation not permitted"),
    )

    capability = ns.namespace_sandbox_capability()
    assert not capability.available
    assert capability.operation == "write uid_map"
    assert capability.reason == "operation not permitted"


def test_capability_failure_reason_is_cached(monkeypatch):
    probes = []
    capability = ns.NamespaceCapability(False, "mount(MS_PRIVATE)", "permission denied")
    monkeypatch.setattr(ns.platform, "system", lambda: "Linux")
    monkeypatch.setattr(ns.ctypes, "CDLL", lambda *args, **kwargs: object())
    monkeypatch.setattr(
        ns, "_probe_namespace_capability", lambda libc: probes.append(libc) or capability
    )

    assert ns.namespace_sandbox_capability() == capability
    assert ns.namespace_sandbox_capability() == capability
    assert len(probes) == 1


@pytest.mark.skipif(not hasattr(os, "fork"), reason="requires fork")
def test_probe_transports_syscall_failure(monkeypatch):
    class FailingLibc:
        def unshare(self, flags):
            ctypes.set_errno(errno.EPERM)
            return -1

    capability = ns._probe_namespace_capability(FailingLibc())
    assert capability == ns.NamespaceCapability(
        False, "unshare(CLONE_NEWUSER | CLONE_NEWNS)", "Operation not permitted"
    )


@pytest.mark.skipif(not hasattr(os, "fork"), reason="requires fork")
@pytest.mark.parametrize(
    "failing_call, operation",
    [
        (1, "mount(tmpfs probe)"),
        (2, "mount(MS_REMOUNT, MS_RDONLY probe)"),
        (3, "mount(MS_BIND probe)"),
        (4, "mount(tmpfs shared memory)"),
        (5, "mount(MS_BIND device probe)"),
    ],
)
def test_probe_transports_mount_failure(monkeypatch, failing_call, operation):
    class FailingLibc:
        def __init__(self):
            self.mount_calls = 0

        def mount(self, source, target, filesystemtype, flags, data):
            self.mount_calls += 1
            if self.mount_calls == failing_call:
                ctypes.set_errno(errno.EPERM)
                return -1
            return 0

        def mount_setattr(self, directory_fd, path, flags, attributes, size):
            return 0

    monkeypatch.setattr(ns, "_enter_user_mount_namespace", lambda *args, **kwargs: None)
    capability = ns._probe_namespace_capability(FailingLibc())
    assert capability == ns.NamespaceCapability(False, operation, "Operation not permitted")


def test_probe_transports_network_namespace_failure(monkeypatch):
    class SuccessfulLibc:
        def mount(self, source, target, filesystemtype, flags, data):
            return 0

        def mount_setattr(self, directory_fd, path, flags, attributes, size):
            return 0

    monkeypatch.setattr(ns, "_enter_user_mount_namespace", lambda *args, **kwargs: None)

    def fail_network_namespace(libc):
        raise ns.NamespaceSetupError(
            errno.EPERM, "unshare(CLONE_NEWNET)", "Operation not permitted"
        )

    monkeypatch.setattr(ns, "_enter_network_namespace", fail_network_namespace)
    capability = ns._probe_namespace_capability(SuccessfulLibc())
    assert capability == ns.NamespaceCapability(
        False, "unshare(CLONE_NEWNET)", "Operation not permitted"
    )


@pytest.mark.skipif(not hasattr(os, "fork"), reason="requires fork")
def test_probe_transports_read_only_mount_failure(monkeypatch):
    class FailingLibc:
        def mount(self, source, target, filesystemtype, flags, data):
            return 0

        def mount_setattr(self, directory_fd, path, flags, attributes, size):
            ctypes.set_errno(errno.EOPNOTSUPP)
            return -1

    monkeypatch.setattr(ns, "_enter_user_mount_namespace", lambda *args, **kwargs: None)
    capability = ns._probe_namespace_capability(FailingLibc())
    assert capability == ns.NamespaceCapability(
        False, "mount_setattr(MOUNT_ATTR_RDONLY)", os.strerror(errno.EOPNOTSUPP)
    )


@pytest.mark.skipif(not hasattr(os, "fork"), reason="requires fork")
def test_probe_transports_capability_drop_failure(monkeypatch):
    class FailingLibc:
        def mount(self, source, target, filesystemtype, flags, data):
            return 0

        def mount_setattr(self, directory_fd, path, flags, attributes, size):
            return 0

        def capset(self, header, capabilities):
            ctypes.set_errno(errno.EPERM)
            return -1

    monkeypatch.setattr(ns, "_enter_user_mount_namespace", lambda *args, **kwargs: None)
    capability = ns._probe_namespace_capability(FailingLibc())
    assert capability == ns.NamespaceCapability(
        False, "capset(drop namespace capabilities)", "Operation not permitted"
    )


@pytest.mark.skipif(not hasattr(os, "fork"), reason="requires fork")
def test_probe_removes_bind_mount_directories(monkeypatch, tmp_path):
    probe_root = tmp_path / "probe"

    class SuccessfulLibc:
        def mount(self, source, target, filesystemtype, flags, data):
            return 0

        def mount_setattr(self, directory_fd, path, flags, attributes, size):
            return 0

        def capset(self, header, capabilities):
            return 0

    def make_probe_root(**kwargs):
        probe_root.mkdir()
        return str(probe_root)

    monkeypatch.setattr(ns.tempfile, "mkdtemp", make_probe_root)
    monkeypatch.setattr(ns, "_enter_user_mount_namespace", lambda *args, **kwargs: None)
    real_open = open

    def open_probe_file(path, *args, **kwargs):
        if os.path.dirname(path) == str(probe_root / "shm" / "fd"):
            path = str(probe_root / "shm" / "probe")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", open_probe_file)

    assert ns._probe_namespace_capability(SuccessfulLibc()).available
    assert not probe_root.exists()


@pytest.mark.parametrize("available", [False, True])
def test_default_libc_probe_result_is_cached(monkeypatch, available):
    probes = []
    monkeypatch.setattr(ns.platform, "system", lambda: "Linux")
    monkeypatch.setattr(ns.ctypes, "CDLL", lambda *args, **kwargs: object())
    capability = ns.NamespaceCapability(available, None if available else "probe", None)
    monkeypatch.setattr(
        ns, "_probe_namespace_capability", lambda libc: probes.append(libc) or capability
    )

    assert ns.namespace_sandbox_available() is available
    assert ns.namespace_sandbox_available() is available
    assert len(probes) == 1


def test_worker_freezes_unavailable_result_after_retry(monkeypatch):
    attempts = []
    monkeypatch.setattr(ns.platform, "system", lambda: "Linux")

    def fail(*args, **kwargs):
        attempts.append(None)
        raise OSError(errno.EAGAIN, "temporary probe failure")

    monkeypatch.setattr(ns.ctypes, "CDLL", fail)
    assert not ns.namespace_sandbox_available()
    assert ns._namespace_probe_result is None
    assert not ns.freeze_namespace_sandbox_capability().available
    assert ns._namespace_probe_result == ns.NamespaceCapability(
        False, "load libc", "temporary probe failure"
    )
    assert not ns.namespace_sandbox_available()
    assert len(attempts) == 2
