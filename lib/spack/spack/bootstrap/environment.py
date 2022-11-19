# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Bootstrap non-core Spack dependencies from an environment."""
import glob
import os
import pathlib
import sys
import warnings

import archspec.cpu

from llnl.util import tty

import spack.environment
import spack.tengine
import spack.util.executable

from .common import _root_spec
from .config import environment_path, spec_for_current_python, store_path


class Paths:
    @classmethod
    def environment_root(cls):
        """Environment root directory"""
        return pathlib.Path(environment_path())

    @classmethod
    def view_root(cls):
        return cls.environment_root().joinpath("view")

    @classmethod
    def pythonpaths(cls):
        python_dir_part = f"python{'.'.join(str(x) for x in sys.version_info[:2])}"
        glob_expr = str(cls.view_root().joinpath("**", python_dir_part, "**"))
        result = glob.glob(glob_expr)
        if not result:
            msg = f"Cannot find any Python path in {cls.view_root()}"
            warnings.warn(msg)
        return result

    @classmethod
    def bin_dirs(cls):
        return [cls.view_root().joinpath("bin")]

    @classmethod
    def spack_yaml(cls):
        """Environment spack.yaml file"""
        return cls.environment_root().joinpath("spack.yaml")


def isort_root_spec():
    """Return the root spec used to bootstrap isort"""
    return _root_spec("py-isort@4.3.5:")


def mypy_root_spec():
    """Return the root spec used to bootstrap mypy"""
    return _root_spec("py-mypy@0.900:")


def black_root_spec():
    """Return the root spec used to bootstrap black"""
    return _root_spec("py-black")


def flake8_root_spec():
    """Return the root spec used to bootstrap flake8"""
    return _root_spec("py-flake8")


def pytest_spec():
    return _root_spec("py-pytest")


def all_environment_root_specs():
    """Return a list of all the root specs that may be used to bootstrap Spack.

    Args:
        development (bool): if True include dev dependencies
    """
    return [
        isort_root_spec(),
        mypy_root_spec(),
        black_root_spec(),
        flake8_root_spec(),
        pytest_spec(),
    ]


def ensure_environment_dependencies():
    if not Paths.spack_yaml().exists():
        _write_spack_yaml_file()

    with spack.environment.Environment(environment_path()) as env:
        specs = env.concretize()
        if specs:
            env.write(regenerate=False)
            _install_all_specs(env)
            env.write(regenerate=True)

    # Do minimal modifications to sys.path and environment variables. In particular, pay
    # attention to have the smallest PYTHONPATH / sys.path possible, since that may impact
    # the performance of the current interpreter
    sys.path.extend(Paths.pythonpaths())
    os.environ["PATH"] = os.pathsep.join(
        [str(x) for x in Paths.bin_dirs()] + os.environ.get("PATH", "").split(os.pathsep)
    )
    os.environ["PYTHONPATH"] = os.pathsep.join(
        os.environ.get("PYTHONPATH", "").split(os.pathsep) + [str(x) for x in Paths.pythonpaths()]
    )


def _install_all_specs(env):
    tty.msg("Bootstrapping Spack dependencies")

    if sys.platform == "win32":
        env.install_all()
        return

    # On Linux and macOS use the depfile, since it's faster at installing things
    spackcmd = spack.util.executable.which("spack")
    spackcmd(
        "-e",
        str(Paths.environment_root()),
        "env",
        "depfile",
        "-o",
        str(Paths.environment_root().joinpath("Makefile")),
    )
    make = spack.util.executable.which("make")
    make("-C", str(Paths.environment_root()), "-j", output=os.devnull, error=os.devnull)


def _write_spack_yaml_file():
    env = spack.tengine.make_environment()
    template = env.get_template("bootstrap/spack.yaml")
    context = {
        "python_spec": spec_for_current_python(),
        "python_prefix": sys.exec_prefix,
        "architecture": archspec.cpu.host().family,
        "environment_path": environment_path(),
        "environment_specs": all_environment_root_specs() + [spec_for_current_python()],
        "store_path": store_path(),
    }
    Paths.environment_root().mkdir(parents=True, exist_ok=True)
    Paths.spack_yaml().write_text(template.render(context), encoding="utf-8")
