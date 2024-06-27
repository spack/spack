# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import shutil

import pytest

import spack.util.binary_resource as br
import spack.util.executable
from spack.paths import spack_root

datadir = os.path.join(spack_root, "lib", "spack", "spack", "test", "data", "binary_resource")
file_file = os.path.join(datadir, "file.bat")


@pytest.fixture
def mock_binary_resource_root(monkeypatch, tmpdir):
    def _binary_resource_root():
        return tmpdir.mkdir("binary-resources")

    monkeypatch.setattr(spack.util.binary_resource, "binary_resource_root", _binary_resource_root)


@pytest.fixture
def no_system(working_env):
    """Fixture preventing system binaries from being detected"""
    os.environ["PATH"] = ""


@pytest.fixture
def on_system(working_env):
    """Fixture explicityly adding binary resource to PATH"""
    env = spack.util.environment.EnvironmentModifications()
    env.append_path("PATH", datadir)
    env.apply_modifications()


def test_ensure_or_acquire_no_acquire(mock_binary_resource_root, config, no_system, monkeypatch):
    def _fake_acquire(self):
        os.makedirs(br.binary_resource_root() / "bin")
        shutil.copy(file_file, br.binary_resource_root() / "bin")

    monkeypatch.setattr(
        spack.util.binary_resource.BinaryResource, "acquire_resource", _fake_acquire
    )
    br.win_ensure_or_acquire_resource("file")
    file = spack.util.executable.which("file")
    assert file
    assert "file-5.4.1 magicfile from /usr/share/bin" in file(output=str)


def test_ensure_or_acquire_acquire_resource(mock_binary_resource_root, config, no_system):
    br.win_ensure_or_acquire_resource("file")
    file = spack.util.executable.which("file")
    assert file
    assert "file-5.4.1 magicfile from /usr/share/bin" in file(output=str)


def test_ensure_or_acquire_resource_on_system(
    mock_binary_resource_root, mutable_config, on_system
):
    # if resource not on system, ensure the resource acquisition fails with an exception
    mutable_config.set("bootstrap_resource:enable", False)
    br.win_ensure_or_acquire_resource("file")


def test_ensure_or_acquire_disabled_no_system(
    mock_binary_resource_root, mutable_config, no_system
):
    mutable_config.set("bootstrap_resource:enable", False)
    with pytest.raises(
        RuntimeError, match=r"Cannot fetch bootstrap resource \w as it is disabled"
    ):
        br.win_ensure_or_acquire_resource("file")
