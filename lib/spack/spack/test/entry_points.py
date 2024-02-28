# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

import spack.paths
import spack.util.spack_yaml as syaml
from spack.util.executable import Executable


def package_creator(tmpdir):
    """Create a basic entry point directory structure"""

    root = tmpdir.ensure("myproject", dir=True)
    with open(os.path.join(root.strpath, "pyproject.toml"), "w") as fh:
        fh.write(
            """\
[project]
name = "myproject"
version = "1.0"
description = "Single file project"
requires-python = ">=3.8"
[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.build_meta"
[project.entry-points."spack.config"]
"myproject" = "myproject:get_spack_config_path"
[project.entry-points."spack.extensions"]
"myproject" = "myproject:get_spack_extension_path"
"""
        )
        # The config and extension point entry points are generated on the fly
        # for the test
        root.ensure("src/myproject", dir=True)
        with open(os.path.join(root.strpath, "src/myproject/__init__.py"), "w") as fh:
            fh.write(
                """\
import importlib.resources
def get_spack_config_path():
    root = importlib.resources.files("myproject")
    cfg = root.joinpath("spack/etc")
    if cfg.exists():
        return str(cfg)
    cfg.mkdir(parents=True, exist_ok=True)
    with open(cfg.joinpath("config.yaml"), "w") as fh:
        fh.write("config:\\n  install_tree:\\n    root: /spam/opt\\n")
    return str(cfg)
def get_spack_extension_path():
    root = importlib.resources.files("myproject")
    ext = root.joinpath("spack/spack-ext/ext/cmd")
    if ext.exists():
        return str(root.joinpath("spack/spack-ext"))
    ext.mkdir(parents=True, exist_ok=True)
    with open(ext.joinpath("spam.py"), "w") as fh:
        fh.write("description = 'hello world extension command'\\n")
        fh.write("section = 'test command'\\n")
        fh.write("level = 'long'\\n")
        fh.write("def setup_parser(subparser):\\n    pass\\n")
        fh.write("def spam(parser, args):\\n    print('spam for all!')\\n")
    return str(root.joinpath("spack/spack-ext"))
"""
            )
    return root


@pytest.mark.skipif(
    sys.version_info[:2] < (3, 8), reason="Python version 3.8 or newer required"
)
def test_spack_entry_points(tmpdir):
    """Basic test of a functioning command."""
    package_src_root = package_creator(tmpdir)
    with tmpdir.as_cwd():
        Executable(sys.executable)("-m", "venv", "venv")
    venv_bin_path = os.path.join(tmpdir.strpath, "venv/bin")
    env = dict(os.environ)
    env["PATH"] = "%s%s%s" % (str(venv_bin_path), os.pathsep, os.environ["PATH"])
    python = Executable(os.path.join(venv_bin_path, "python3"))
    with package_src_root.as_cwd():
        python("-m", "pip", "install", ".", env=env)
        spack_script = os.path.join(spack.paths.bin_path, "spack")
        output = python(spack_script, "config", "get", "config", output=str, env=env)
        config = syaml.load(output)
        assert config["config"]["install_tree"]["root"] == "/spam/opt"
        output = python(spack_script, "spam", output=str, env=env)
        assert "spam for all!" in output, output


if __name__ == "__main__":
    import tempfile
    import pathlib
    import shutil

    try:
        d = pathlib.Path(tempfile.mkdtemp())
        test_spack_entry_points(d)
    finally:
        shutil.rmtree(str(d))
