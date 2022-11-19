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


class BootstrapEnvironment(spack.environment.Environment):
    @classmethod
    def environment_root(cls):
        """Environment root directory"""
        return pathlib.Path(environment_path())

    @classmethod
    def view_root(cls):
        """Location of the view"""
        return cls.environment_root().joinpath("view")

    @classmethod
    def pythonpaths(cls):
        """Paths to be added to sys.path or PYTHONPATH"""
        python_dir_part = f"python{'.'.join(str(x) for x in sys.version_info[:2])}"
        glob_expr = str(cls.view_root().joinpath("**", python_dir_part, "**"))
        result = glob.glob(glob_expr)
        if not result:
            msg = f"Cannot find any Python path in {cls.view_root()}"
            warnings.warn(msg)
        return result

    @classmethod
    def bin_dirs(cls):
        """Paths to be added to PATH"""
        return [cls.view_root().joinpath("bin")]

    @classmethod
    def spack_yaml(cls):
        """Environment spack.yaml file"""
        return cls.environment_root().joinpath("spack.yaml")

    def __init__(self):
        if not self.spack_yaml().exists():
            self._write_spack_yaml_file()
        super().__init__(self.environment_root())

    def update_installations(self):
        """Update the installations of this environment.

        The update is done using a depfile on Linux and macOS, and using the ``install_all``
        method of environments on Windows.
        """
        specs = self.concretize()
        if specs:
            tty.msg("Bootstrapping Spack dependencies")
            self.write(regenerate=False)
            if sys.platform == "win32":
                self.install_all()
            else:
                self._install_with_depfile()
            self.write(regenerate=True)

    def update_syspath_and_environ(self):
        """Update ``sys.path`` and the PATH, PYTHONPATH environment variables to point to
        the environment view.
        """
        # Do minimal modifications to sys.path and environment variables. In particular, pay
        # attention to have the smallest PYTHONPATH / sys.path possible, since that may impact
        # the performance of the current interpreter
        sys.path.extend(self.pythonpaths())
        os.environ["PATH"] = os.pathsep.join(
            [str(x) for x in self.bin_dirs()] + os.environ.get("PATH", "").split(os.pathsep)
        )
        os.environ["PYTHONPATH"] = os.pathsep.join(
            os.environ.get("PYTHONPATH", "").split(os.pathsep)
            + [str(x) for x in self.pythonpaths()]
        )

    def _install_with_depfile(self):
        spackcmd = spack.util.executable.which("spack")
        spackcmd(
            "-e",
            str(self.environment_root()),
            "env",
            "depfile",
            "-o",
            str(self.environment_root().joinpath("Makefile")),
        )
        make = spack.util.executable.which("make")
        make("-C", str(self.environment_root()), "-j", output=os.devnull, error=os.devnull)

    def _write_spack_yaml_file(self):
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
        self.environment_root().mkdir(parents=True, exist_ok=True)
        self.spack_yaml().write_text(template.render(context), encoding="utf-8")


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
    with BootstrapEnvironment() as env:
        env.update_installations()
        env.update_syspath_and_environ()
