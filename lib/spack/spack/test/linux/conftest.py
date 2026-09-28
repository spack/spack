# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Shared fixtures for the Linux sandbox tests."""

import io

import pytest

import spack.sandbox_namespaces as ns


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
