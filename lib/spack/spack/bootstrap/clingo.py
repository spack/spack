# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Bootstrap concrete specs for clingo

Spack uses clingo to concretize specs. When clingo itself needs to be bootstrapped from sources,
we need to rely on another mechanism to get a concrete spec that fits the current host.

This module contains the logic to get a concrete spec for clingo, starting from a prototype
JSON file for a similar platform.
"""
import pathlib
import sys
from typing import Dict, Optional, Tuple

import archspec.cpu

import spack.compiler
import spack.compilers
import spack.platforms
import spack.spec
import spack.traverse

from .config import spec_for_current_python


class ClingoBootstrapConcretizer:
    def __init__(self, configuration):
        self.host_platform = spack.platforms.host()
        self.host_os = self.host_platform.operating_system("frontend")
        self.host_target = archspec.cpu.host().family
        self.host_architecture = spack.spec.ArchSpec.frontend_arch()
        self.host_architecture.target = str(self.host_target)
        self.host_compiler = self._valid_compiler_or_raise()
        self.host_python = self.python_external_spec()
        self.host_libc = self.libc_external_spec()

        self.external_cmake, self.external_bison = self._externals_from_yaml(configuration)

    def _valid_compiler_or_raise(self) -> "spack.compiler.Compiler":
        # TODO: Add validation for host compiler
        return spack.compilers.compilers_for_spec("gcc", arch_spec=self.host_architecture)[0]

    def _externals_from_yaml(
        self, configuration: "spack.config.Configuration"
    ) -> Tuple[Optional["spack.spec.Spec"], Optional["spack.spec.Spec"]]:
        packages_yaml = configuration.get("packages")
        requirements = {"cmake": "@3.16:", "bison": "@2.5:"}
        selected: Dict[str, Optional["spack.spec.Spec"]] = {"cmake": None, "bison": None}
        for pkg_name in ["cmake", "bison"]:
            if pkg_name not in packages_yaml:
                continue

            candidates = packages_yaml[pkg_name].get("externals", [])
            for candidate in candidates:
                s = spack.spec.Spec(candidate["spec"], external_path=candidate["prefix"])
                if not s.satisfies(requirements[pkg_name]):
                    continue

                if not s.intersects(f"%{self.host_compiler.spec}"):
                    continue

                if not s.intersects(f"arch={self.host_architecture}"):
                    continue

                selected[pkg_name] = self._external_spec(s)
                break
        return selected["cmake"], selected["bison"]

    def prototype_path(self) -> pathlib.Path:
        """Path to a prototype concrete specfile for clingo"""
        parent_dir = pathlib.Path(__file__).parent
        if str(self.host_platform) == "linux":
            result = (
                parent_dir / "prototypes" / f"clingo-{self.host_platform}-{self.host_target}.json"
            )
            # Using aarch64 as a fallback, since it has gnuconfig (x86_64 doesn't have it)
            if not result.exists():
                result = parent_dir / "prototypes" / f"clingo-{self.host_platform}-aarch64.json"
        else:
            raise RuntimeError(f"Cannot bootstrap clingo from sources on {self.host_platform}")
        return result

    def concretize(self) -> "spack.spec.Spec":
        # Read the prototype and mark it NOT concrete
        s = spack.spec.Spec.from_specfile(str(self.prototype_path()))
        s._mark_concrete(False)

        # Tweak it to conform to the host architecture
        for node in s.traverse():
            node.architecture.os = str(self.host_os)
            node.compiler = self.host_compiler.spec
            node.architecture = self.host_architecture

            if node.name == "gcc-runtime":
                node.versions = self.host_compiler.spec.versions

        for edge in spack.traverse.traverse_edges([s], cover="edges"):
            if edge.spec.name == "python":
                edge.spec = self.host_python

            if edge.spec.name == "bison" and self.external_bison:
                edge.spec = self.external_bison

            if edge.spec.name == "cmake" and self.external_cmake:
                edge.spec = self.external_cmake

            if "libc" in edge.virtuals:
                edge.spec = self.host_libc

        s._finalize_concretization()

        # Work around the fact that the installer calls Spec.dependents() and
        # we modified edges inconsistently
        return s.copy()

    def python_external_spec(self) -> "spack.spec.Spec":
        """Python external spec corresponding to the current running interpreter"""
        result = spack.spec.Spec(spec_for_current_python(), external_path=sys.exec_prefix)
        return self._external_spec(result)

    def libc_external_spec(self) -> "spack.spec.Spec":
        result = self.host_compiler.default_libc
        return self._external_spec(result)

    def _external_spec(self, initial_spec) -> "spack.spec.Spec":
        initial_spec.namespace = "builtin"
        initial_spec.compiler = self.host_compiler.spec
        initial_spec.architecture = self.host_architecture
        for flag_type in spack.spec.FlagMap.valid_compiler_flags():
            initial_spec.compiler_flags[flag_type] = []
        return spack.spec.parse_with_version_concrete(initial_spec)
