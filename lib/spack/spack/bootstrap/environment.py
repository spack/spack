# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Bootstrap non-core Spack dependencies from an environment."""
import glob
import hashlib
import os
import pathlib
import sys
import warnings

import archspec.cpu

from llnl.util import tty

import spack.build_environment
import spack.environment
import spack.tengine
import spack.util.executable

from ._common import _root_spec
from .config import root_path, spec_for_current_python, store_path


class BootstrapEnvironment(spack.environment.Environment):
    """Environment to install dependencies of Spack for a given interpreter and architecture"""

    @classmethod
    def spack_dev_requirements(cls):
        """Spack development requirements"""
        return [
            isort_root_spec(),
            mypy_root_spec(),
            black_root_spec(),
            flake8_root_spec(),
            pytest_root_spec(),
        ]

    @classmethod
    def environment_root(cls):
        """Environment root directory"""
        bootstrap_root_path = root_path()
        python_part = spec_for_current_python().replace("@", "")
        arch_part = archspec.cpu.host().family
        interpreter_part = hashlib.md5(sys.exec_prefix.encode()).hexdigest()[:5]
        environment_dir = f"{python_part}-{arch_part}-{interpreter_part}"
        return pathlib.Path(
            spack.util.path.canonicalize_path(
                os.path.join(bootstrap_root_path, "environments", environment_dir)
            )
        )

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
        with tty.SuppressOutput(msg_enabled=False, warn_enabled=False):
            specs = self.concretize()
        if specs:
            colorized_specs = [
                spack.spec.Spec(x).cformat("{name}{@version}")
                for x in self.spack_dev_requirements()
            ]
            tty.msg(f"[BOOTSTRAPPING] Installing dependencies ({', '.join(colorized_specs)})")
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
        kwargs = {}
        if not tty.is_debug():
            kwargs = {"output": os.devnull, "error": os.devnull}
        make(
            "-C",
            str(self.environment_root()),
            "-j",
            str(spack.build_environment.determine_number_of_jobs(parallel=True)),
            **kwargs,
        )

    def _write_spack_yaml_file(self):
        tty.msg(
            "[BOOTSTRAPPING] Spack has missing dependencies, creating a bootstrapping environment"
        )
        env = spack.tengine.make_environment()
        template = env.get_template("bootstrap/spack.yaml")
        context = {
            "python_spec": spec_for_current_python(),
            "python_prefix": sys.exec_prefix,
            "architecture": archspec.cpu.host().family,
            "environment_path": self.environment_root(),
            "environment_specs": self.spack_dev_requirements(),
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
    return _root_spec("py-black@:23.1.0")


def flake8_root_spec():
    """Return the root spec used to bootstrap flake8"""
    return _root_spec("py-flake8")


def pytest_root_spec():
    """Return the root spec used to bootstrap flake8"""
    return _root_spec("py-pytest")


def ensure_environment_dependencies():
    """Ensure Spack dependencies from the bootstrap environment are installed and ready to use"""
    with BootstrapEnvironment() as env:
        env.update_installations()
        env.update_syspath_and_environ()
