# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for Visual Studio discovery in ``operating_systems/windows_os.py``."""

import os
import subprocess
import sys

import pytest

import spack.operating_systems.windows_os as windows_os
from spack.version import Version


pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="Windows OS tests only relevant on Windows")


@pytest.fixture(autouse=True)
def fake_windows_version(monkeypatch):
    """Let ``WindowsOs()`` be constructed on any host."""
    monkeypatch.setattr(windows_os, "windows_version", lambda: Version("10.0.26100"))


@pytest.fixture(autouse=True)
def no_oneapi(monkeypatch):
    """Keep a oneAPI installation on the test host out of the search paths."""
    monkeypatch.setattr(windows_os.WindowsOs, "oneapi_root", property(lambda self: None))


@pytest.fixture
def no_vswhere(monkeypatch):
    monkeypatch.setattr(windows_os.WindowsOs, "_vswhere_install_paths", lambda self: [])


@pytest.fixture
def no_registry(monkeypatch):
    monkeypatch.setattr(windows_os.WindowsOs, "_registry_install_paths", lambda self: [])


def vs_layout(root, *, toolset_versions=("14.44.35207",)):
    """Create the parts of a Visual Studio install tree that Spack looks for."""
    for version in toolset_versions:
        (root / "VC" / "Tools" / "MSVC" / version / "bin" / "Hostx64" / "x64").mkdir(
            parents=True, exist_ok=True
        )
    return str(root)


def test_stale_registry_entry_is_not_reported(monkeypatch, tmp_path, no_vswhere):
    """A registry key left behind by an uninstall must not yield an install path.

    This is the phantom-detection case: Visual Studio records itself in the registry
    and does not always clean up on uninstall, so the recorded root can outlive the
    files it points at.
    """
    live = vs_layout(tmp_path / "live")
    dead = str(tmp_path / "dead")

    monkeypatch.setattr(windows_os.WindowsOs, "_registry_install_paths", lambda self: [live, dead])

    os_ = windows_os.WindowsOs()
    assert os_.vs_install_paths == [live]
    assert not any(dead in path for path in os_.compiler_search_paths)


def test_registry_roots_yield_compiler_search_paths(monkeypatch, tmp_path, no_vswhere):
    """Registry-derived roots must go through the MSVC toolset glob.

    Registry lookup is the fallback for hosts without ``vswhere.exe``. The roots it
    reports contain no compiler themselves, so they are only useful once expanded to
    the toolset ``bin`` directories.
    """
    versions = ("14.44.35207", "14.29.30133")
    root = vs_layout(tmp_path / "vs", toolset_versions=versions)
    monkeypatch.setattr(windows_os.WindowsOs, "_registry_install_paths", lambda self: [root])

    search_paths = windows_os.WindowsOs().compiler_search_paths
    assert sorted(search_paths) == sorted(
        os.path.join(root, "VC", "Tools", "MSVC", version, "bin", "Hostx64", "x64")
        for version in versions
    )
    # the root itself holds no compiler and must not be searched directly
    assert root not in search_paths


def test_install_paths_are_deduped_across_sources(monkeypatch, tmp_path):
    """vswhere and the registry describe the same installations on most hosts."""
    root = vs_layout(tmp_path / "vs")

    monkeypatch.setattr(windows_os.WindowsOs, "_vswhere_install_paths", lambda self: [root])
    # the registry resolves paths, so casing and separators need not match exactly
    duplicate = root.upper() if os.name == "nt" else root
    monkeypatch.setattr(windows_os.WindowsOs, "_registry_install_paths", lambda self: [duplicate])

    assert windows_os.WindowsOs().vs_install_paths == [root]


def test_empty_vswhere_output_yields_no_paths(monkeypatch, no_registry):
    """vswhere prints nothing when it matches no instance.

    Splitting that on newlines produces a single empty string, which would become a
    relative ``VC\\Tools\\MSVC`` glob rooted at the current working directory.
    """
    monkeypatch.setenv("ProgramFiles(x86)", "C:\\Program Files (x86)")
    monkeypatch.setattr(subprocess, "check_output", lambda *args, **kwargs: "")

    os_ = windows_os.WindowsOs()
    assert os_.vs_install_paths == []
    assert os_.msvc_paths == []


def test_vswhere_failure_is_not_fatal(monkeypatch, no_registry):
    """A missing or broken vswhere must leave detection able to continue."""

    def boom(*args, **kwargs):
        raise OSError("vswhere.exe not found")

    monkeypatch.setenv("ProgramFiles(x86)", "C:\\Program Files (x86)")
    monkeypatch.setattr(subprocess, "check_output", boom)

    assert windows_os.WindowsOs().vs_install_paths == []


def test_vswhere_reports_multiple_instances(monkeypatch, tmp_path, no_registry):
    """Every live instance is reported; a stale one is dropped."""
    first = vs_layout(tmp_path / "2022")
    second = vs_layout(tmp_path / "2019")
    gone = str(tmp_path / "removed")

    monkeypatch.setenv("ProgramFiles(x86)", "C:\\Program Files (x86)")
    monkeypatch.setattr(
        subprocess, "check_output", lambda *args, **kwargs: f"{first}\n{gone}\n{second}\n"
    )

    assert windows_os.WindowsOs().vs_install_paths == [first, second]
