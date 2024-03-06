# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

import spack.config
import spack.extensions


class MockConfigEntryPoint:
    def __init__(self, tmp_path):
        self.dir = tmp_path
        self.name = "mypackage_config"

    def load(self):
        etc_path = self.dir.joinpath("spack/etc")
        etc_path.mkdir(exist_ok=True, parents=True)
        f = self.dir / "spack/etc/config.yaml"
        with open(f, "w") as fh:
            fh.write("config:\n  install_tree:\n    root: /spam/opt\n")

        def ep():
            return self.dir / "spack/etc"

        return ep


class MockExtensionsEntryPoint:
    def __init__(self, tmp_path):
        self.dir = tmp_path
        self.name = "mypackage_extensions"

    def load(self):
        cmd_path = self.dir.joinpath("spack/spack-myext/myext/cmd")
        cmd_path.mkdir(exist_ok=True, parents=True)
        f = self.dir / "spack/spack-myext/myext/cmd/spam.py"
        with open(f, "w") as fh:
            fh.write("description = 'hello world extension command'\n")
            fh.write("section = 'test command'\n")
            fh.write("level = 'long'\n")
            fh.write("def setup_parser(subparser):\n    pass\n")
            fh.write("def spam(parser, args):\n    print('spam for all!')\n")

        def ep():
            return self.dir / "spack/spack-myext"

        return ep


def entry_points_factory(tmp_path):
    def entry_points(group=None):
        if group == "spack.config":
            return (MockConfigEntryPoint(tmp_path),)
        elif group == "spack.extensions":
            return (MockExtensionsEntryPoint(tmp_path),)
        return ()

    return entry_points


@pytest.fixture()
def mock_entry_points(tmp_path, monkeypatch):
    entry_points = entry_points_factory(tmp_path)
    try:
        try:
            import importlib.metadata as importlib_metadata  # type: ignore # novermin
        except ImportError:
            import importlib_metadata
        monkeypatch.setattr(importlib_metadata, "entry_points", entry_points)
    except ImportError:
        try:
            import pkg_resources  # type: ignore
        except ImportError:
            return
        monkeypatch.setattr(pkg_resources, "iter_entry_points", entry_points)


@pytest.mark.skipif(sys.version_info[:2] < (3, 8), reason="Python>=3.8 required")
def test_spack_entry_point_config(tmp_path, mock_entry_points):
    """Test config scope entry point"""
    config_paths = dict(spack.config.config_paths_from_entry_points())
    config_path = config_paths.get("plugin-mypackage_config")
    my_config_path = tmp_path / "spack/etc"
    if config_path is None:
        raise ValueError("Did not find entry point config in %s" % str(config_paths))
    else:
        assert os.path.samefile(config_path, my_config_path)
    config = spack.config.create()
    assert config.get("config:install_tree:root", scope="plugin-mypackage_config") == "/spam/opt"


@pytest.mark.skipif(sys.version_info[:2] < (3, 8), reason="Python>=3.8 required")
def test_spack_entry_point_extension(tmp_path, mock_entry_points):
    """Test config scope entry point"""
    my_ext = tmp_path / "spack/spack-myext"
    extensions = spack.extensions.get_extension_paths()
    found = bool([ext for ext in extensions if os.path.samefile(ext, my_ext)])
    if not found:
        raise ValueError("Did not find extension in %s" % ", ".join(extensions))
    extensions = spack.extensions.extension_paths_from_entry_points()
    found = bool([ext for ext in extensions if os.path.samefile(ext, my_ext)])
    if not found:
        raise ValueError("Did not find extension in %s" % ", ".join(extensions))
    root = spack.extensions.load_extension("myext")
    assert os.path.samefile(root, my_ext)
    module = spack.extensions.get_module("spam")
    assert module is not None
