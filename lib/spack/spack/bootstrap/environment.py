# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Bootstrap non-core Spack dependencies from an environment."""
import pathlib
import sys

import archspec.cpu

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


def all_environment_root_specs():
    """Return a list of all the root specs that may be used to bootstrap Spack.

    Args:
        development (bool): if True include dev dependencies
    """
    return [isort_root_spec(), mypy_root_spec(), black_root_spec(), flake8_root_spec()]


def ensure_environment_dependencies():
    if not Paths.spack_yaml().exists():
        _write_spack_yaml_file()

    with spack.environment.Environment(environment_path()) as env:
        specs = env.concretize()
        if specs:
            _install_all_specs(env)
        modifications = spack.util.environment.EnvironmentModifications()
        env.add_default_view_to_env(modifications)
    environment_modifications = modifications
    # TODO: apply PYTHONPATH to sys.path directly
    environment_modifications.apply_modifications()


def _install_all_specs(env):
    # TODO: win32?
    env.write(regenerate=False)
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
    make("-C", str(Paths.environment_root()), "-j")
    env.write(regenerate=True)


def _write_spack_yaml_file():
    env = spack.tengine.make_environment()
    template = env.get_template("bootstrap/spack.yaml")
    context = {
        "python_spec": spec_for_current_python(),
        "python_prefix": sys.exec_prefix,
        "architecture": archspec.cpu.host().family,
        "environment_path": environment_path(),
        "environment_specs": all_environment_root_specs(),
        "store_path": store_path(),
    }
    Paths.environment_root().mkdir(parents=True, exist_ok=True)
    Paths.spack_yaml().write_text(template.render(context), encoding="utf-8")
