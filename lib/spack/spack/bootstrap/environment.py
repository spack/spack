# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Bootstrap non-core Spack dependencies from an environment."""

import contextlib
import hashlib
import os
import pathlib
import sys
from typing import Iterable, List

import spack.vendor.archspec.cpu

import spack.binary_distribution
import spack.config
import spack.environment
import spack.spec
import spack.tengine
import spack.util.gpg
import spack.util.path
from spack.llnl.util import tty

from .config import root_path, spec_for_current_python, store_path
from .core import _add_externals_if_missing


class BootstrapEnvironment(spack.environment.Environment):
    """Environment to install dependencies of Spack for a given interpreter and architecture"""

    def __init__(self) -> None:
        if not self.spack_yaml().exists():
            self._write_spack_yaml_file()
        super().__init__(self.environment_root())

        # Remove python package roots created before python-venv was introduced
        for s in self.concrete_roots():
            if "python" in s.package.extendees and not s.dependencies("python-venv"):
                self.deconcretize_by_hash(s.dag_hash())

    @classmethod
    def spack_dev_requirements(cls) -> List[str]:
        """Spack development requirements"""
        return [pytest_root_spec(), ruff_root_spec(), mypy_root_spec()]

    @classmethod
    def environment_root(cls) -> pathlib.Path:
        """Environment root directory"""
        bootstrap_root_path = root_path()
        python_part = spec_for_current_python().replace("@", "")
        arch_part = spack.vendor.archspec.cpu.host().family
        interpreter_part = hashlib.md5(sys.exec_prefix.encode()).hexdigest()[:5]
        environment_dir = f"{python_part}-{arch_part}-{interpreter_part}"
        return pathlib.Path(
            spack.util.path.canonicalize_path(
                os.path.join(bootstrap_root_path, "environments", environment_dir)
            )
        )

    @classmethod
    def view_root(cls) -> pathlib.Path:
        """Location of the view"""
        return cls.environment_root().joinpath("view")

    @classmethod
    def bin_dir(cls) -> pathlib.Path:
        """Paths to be added to PATH"""
        return cls.view_root().joinpath("bin")

    def python_dirs(self) -> Iterable[pathlib.Path]:
        python = next(s for s in self.all_specs_generator() if s.name == "python-venv").package
        return {self.view_root().joinpath(p) for p in (python.platlib, python.purelib)}

    @classmethod
    def spack_yaml(cls) -> pathlib.Path:
        """Environment spack.yaml file"""
        return cls.environment_root().joinpath("spack.yaml")

    @contextlib.contextmanager
    def trust_bootstrap_mirror_keys(self):
        with spack.util.gpg.gnupghome_override(os.path.join(root_path(), ".bootstrap-gpg")):
            spack.binary_distribution.get_keys(install=True, trust=True)
            yield

    def update_installations(self) -> None:
        """Update the installations of this environment."""
        log_enabled = tty.is_debug() or tty.is_verbose()
        with tty.SuppressOutput(msg_enabled=log_enabled, warn_enabled=log_enabled):
            specs = self.concretize()
        if specs:
            colorized_specs = [
                spack.spec.Spec(x).cformat("{name}{@version}")
                for x in self.spack_dev_requirements()
            ]
            tty.msg(f"[BOOTSTRAPPING] Installing dependencies ({', '.join(colorized_specs)})")
            self.write(regenerate=False)
            with tty.SuppressOutput(msg_enabled=log_enabled, warn_enabled=log_enabled):
                with self.trust_bootstrap_mirror_keys():
                    fetch_policy = (
                        "cache_only"
                        if not spack.config.get("bootstrap:dev:enable_source", False)
                        else "auto"
                    )
                    self.install_all(
                        fail_fast=True, root_policy=fetch_policy, dependencies_policy=fetch_policy
                    )
                    self.write(regenerate=True)

    def load(self) -> None:
        """Update PATH and sys.path."""
        # Make executables available (shouldn't need PYTHONPATH)
        os.environ["PATH"] = f"{self.bin_dir()}{os.pathsep}{os.environ.get('PATH', '')}"

        # Spack itself imports pytest
        sys.path.extend(str(p) for p in self.python_dirs())

    def _write_spack_yaml_file(self) -> None:
        tty.msg(
            "[BOOTSTRAPPING] Spack has missing dependencies, creating a bootstrapping environment"
        )
        env = spack.tengine.make_environment()
        template = env.get_template("bootstrap/spack.yaml")
        context = {
            "python_spec": f"{spec_for_current_python()}+ctypes",
            "python_prefix": sys.exec_prefix,
            "architecture": spack.vendor.archspec.cpu.host().family,
            "environment_path": self.environment_root(),
            "environment_specs": self.spack_dev_requirements(),
            "store_path": store_path(),
            "bootstrap_mirrors": dev_bootstrap_mirror_names(),
        }
        self.environment_root().mkdir(parents=True, exist_ok=True)
        self.spack_yaml().write_text(template.render(context), encoding="utf-8")


def mypy_root_spec() -> str:
    """Return the root spec used to bootstrap mypy"""
    return "py-mypy@0.900: ^py-mypy-extensions@:1.0"


def pytest_root_spec() -> str:
    """Return the root spec used to bootstrap pytest"""
    return "py-pytest@6.2.4:"


def ruff_root_spec() -> str:
    """Return the root spec used to bootstrap ruff"""
    return "py-ruff@0.15.0"


def dev_bootstrap_mirror_names() -> List[str]:
    """Return the mirror names used for bootstrapping dev
    requirements"""
    return [
        "developer-tools-darwin",
        "developer-tools-x86_64_v3-linux-gnu",
        "developer-tools-aarch64-linux-gnu",
    ]


def ensure_environment_dependencies() -> None:
    """Ensure Spack dependencies from the bootstrap environment are installed and ready to use"""
    _add_externals_if_missing()
    with BootstrapEnvironment() as env:
        env.update_installations()
        env.load()
