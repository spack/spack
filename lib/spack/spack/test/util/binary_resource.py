# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

import pytest

import spack.util.binary_resource as br
import spack.util.executable
from spack.paths import spack_root

datadir = os.path.join(spack_root, "lib", "spack", "spack", "test", "data", "binary_resource")
file_file = os.path.join(datadir, "file.bat")
tar = spack.util.executable.which("tar")


@pytest.fixture
def mock_binary_resource_root(monkeypatch, tmpdir):
    resource_root = tmpdir.mkdir("binary-resources")

    def _binary_resource_root():
        return resource_root

    monkeypatch.setattr(spack.util.binary_resource, "binary_resource_root", _binary_resource_root)


@pytest.fixture
def no_system(working_env):
    """Fixture preventing system binaries from being detected"""
    os.environ["PATH"] = ""


@pytest.fixture
def add_tar_to_path(no_system):
    os.environ["PATH"] = os.path.dirname(tar.path)


@pytest.fixture
def add_resource_to_system(working_env):
    """Fixture explicitly adding binary resource to PATH"""

    def _add_file():
        env = spack.util.environment.EnvironmentModifications()
        env.append_path("PATH", datadir)
        env.apply_modifications()

    return _add_file


@pytest.mark.skipif(not tar, reason="tar required; not available")
def test_ensure_or_acquire_acquire_resource(mock_binary_resource_root, config, add_tar_to_path):
    # establish that file is unavailable prior to resource acquisition
    file = spack.util.executable.which("file")
    assert not file
    br.win_ensure_or_acquire_resource("file")
    file = spack.util.executable.which("file")
    assert file
    assert "file-5.4.1 magicfile from /usr/share/bin" in file(output=str)


def test_ensure_or_acquire_disabled_no_system(
    mock_binary_resource_root, mutable_config, no_system, add_resource_to_system
):
    mutable_config.set("bootstrap_resource:enable", False)
    with pytest.raises(
        RuntimeError, match=r"Cannot fetch bootstrap resource .* as it is disabled"
    ):
        br.win_ensure_or_acquire_resource("file")
    add_resource_to_system()
    br.win_ensure_or_acquire_resource("file")
