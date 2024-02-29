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
    def __init__(self, tmpdir):
        self.dir = tmpdir
        self.name = "mypackage_config"

    def load(self):
        self.dir.ensure("spack/etc", dir=True)
        with open(os.path.join(self.dir, "spack/etc/config.yaml"), "w") as fh:
            fh.write("config:\n  install_tree:\n    root: /spam/opt\n")

        def ep():
            return os.path.join(self.dir, "spack/etc")

        return ep


class MockExtensionsEntryPoint:
    def __init__(self, tmpdir):
        self.dir = tmpdir
        self.name = "mypackage_extensions"

    def load(self):
        self.dir.ensure("spack/spack-ext/ext/cmd", dir=True)
        with open(os.path.join(self.dir, "spack/spack-ext/ext/cmd/spam.py"), "w") as fh:
            fh.write("description = 'hello world extension command'\n")
            fh.write("section = 'test command'\n")
            fh.write("level = 'long'\n")
            fh.write("def setup_parser(subparser):\n    pass\n")
            fh.write("def spam(parser, args):\n    print('spam for all!')\n")

        def ep():
            return os.path.join(self.dir, "spack/spack-ext")

        return ep


def entry_points_factory(tmpdir):
    def entry_points(group=None):
        if group == "spack.config":
            return (MockConfigEntryPoint(tmpdir),)
        elif group == "spack.extensions":
            return (MockExtensionsEntryPoint(tmpdir),)
        return ()

    return entry_points


@pytest.mark.skipif(sys.version_info[:2] < (3, 8), reason="Python>=3.8 required")
def test_spack_entry_points(monkeypatch, tmpdir):
    """Test config scope entry point"""
    entry_points = entry_points_factory(tmpdir)
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
    config = spack.config.create()
    assert config.get("config:install_tree:root") == "/spam/opt"
    extensions = spack.extensions.get_extension_paths()
    assert os.path.join(tmpdir, "spack/spack-ext") in extensions
