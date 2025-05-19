# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib
import shutil
import sys
from typing import List

from spack_repo.builtin.build_systems.generic import Package

import archspec.cpu

from llnl.util import lang

import spack.compilers.libraries
import spack.package_base
from spack.package import *


class CompilerWrapper(Package):
    """Spack compiler wrapper script.

    Compiler commands go through this compiler wrapper in Spack builds.
    The compiler wrapper is a thin layer around the standard compilers.
    It enables several key pieces of functionality:

    1. It allows Spack to swap compilers into and out of builds easily.
    2. It adds several options to the compile line so that spack
       packages can find their dependencies at build time and run time:
       -I and/or -isystem arguments for dependency /include directories.
       -L                 arguments for dependency /lib directories.
       -Wl,-rpath         arguments for dependency /lib directories.
    3. It provides a mechanism to inject flags from specs
    """

    homepage = "https://github.com/spack/spack"
    url = f"file:///{pathlib.PurePath(__file__).parent}/cc.sh"

    # FIXME (compiler as nodes): use a different tag, since this is only to exclude
    # this node from auto-generated rules
    tags = ["runtime"]

    license("Apache-2.0 OR MIT")

    if sys.platform != "win32":
        version(
            "1.0",
            sha256="c65a9d2b2d4eef67ab5cb0684d706bb9f005bb2be94f53d82683d7055bdb837c",
            expand=False,
        )
    else:
        version("1.0")
        has_code = False

    def bin_dir(self) -> pathlib.Path:
        # This adds an extra "spack" subdir, so that the script and symlinks don't get
        # their way to the default view
        return pathlib.Path(str(self.prefix)) / "libexec" / "spack"

    def install(self, spec, prefix):
        if sys.platform == "win32":
            placeholder = self.bin_dir() / "placeholder-wrapper"
            placeholder.parent.mkdir(parents=True)
            placeholder.write_text(
                "This file is a placeholder for the compiler wrapper on Windows."
            )
            return

        cc_script = pathlib.Path(self.stage.source_path) / "cc.sh"
        bin_dir = self.bin_dir()

        # Copy the script
        bin_dir.mkdir(parents=True)
        installed_script = bin_dir / "cc"
        shutil.copy(cc_script, str(installed_script))
        set_executable(installed_script)

        # Create links to use the script under different names
        for name in (
            "ld.lld",
            "ld.gold",
            "ld",
            "ftn",
            "fc",
            "f95",
            "f90",
            "f77",
            "cpp",
            "c99",
            "c89",
            "c++",
        ):
            (bin_dir / name).symlink_to(installed_script)

        for subdir, name in (
            ("aocc", "clang"),
            ("aocc", "clang++"),
            ("aocc", "flang"),
            ("arm", "armclang"),
            ("arm", "armclang++"),
            ("arm", "armflang"),
            ("case-insensitive", "CC"),
            ("cce", "cc"),
            ("cce", "craycc"),
            ("cce", "crayftn"),
            ("cce", "ftn"),
            ("clang", "clang"),
            ("clang", "clang++"),
            ("clang", "flang"),
            ("fj", "fcc"),
            ("fj", "frt"),
            ("gcc", "gcc"),
            ("gcc", "g++"),
            ("gcc", "gfortran"),
            ("intel", "icc"),
            ("intel", "icpc"),
            ("intel", "ifort"),
            ("nag", "nagfor"),
            ("nvhpc", "nvc"),
            ("nvhpc", "nvc++"),
            ("nvhpc", "nvfortran"),
            ("oneapi", "icx"),
            ("oneapi", "icpx"),
            ("oneapi", "ifx"),
            ("rocmcc", "amdclang"),
            ("rocmcc", "amdclang++"),
            ("rocmcc", "amdflang"),
            ("xl", "xlc"),
            ("xl", "xlc++"),
            ("xl", "xlf"),
            ("xl", "xlf90"),
            ("xl_r", "xlc_r"),
            ("xl_r", "xlc++_r"),
            ("xl_r", "xlf_r"),
            ("xl_r", "xlf90_r"),
        ):
            (bin_dir / subdir).mkdir(exist_ok=True)
            (bin_dir / subdir / name).symlink_to(installed_script)

        # Extra symlinks for Cray
        cray_dir = bin_dir / "cce" / "case-insensitive"
        cray_dir.mkdir(exist_ok=True)
        (cray_dir / "crayCC").symlink_to(installed_script)
        (cray_dir / "CC").symlink_to(installed_script)

    def setup_dependent_build_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        if sys.platform == "win32":
            return

        _var_list = []
        if dependent_spec.has_virtual_dependency("c"):
            _var_list.append(("c", "cc", "CC", "SPACK_CC"))

        if dependent_spec.has_virtual_dependency("cxx"):
            _var_list.append(("cxx", "cxx", "CXX", "SPACK_CXX"))

        if dependent_spec.has_virtual_dependency("fortran"):
            _var_list.append(("fortran", "fortran", "F77", "SPACK_F77"))
            _var_list.append(("fortran", "fortran", "FC", "SPACK_FC"))

        # The package is not used as a compiler, so skip this setup
        if not _var_list:
            return

        bin_dir = self.bin_dir()
        implicit_rpaths, env_paths = [], []
        extra_rpaths = []
        for language, attr_name, wrapper_var_name, spack_var_name in _var_list:
            compiler_pkg = dependent_spec[language].package
            if not hasattr(compiler_pkg, attr_name):
                continue

            compiler = getattr(compiler_pkg, attr_name)
            env.set(spack_var_name, compiler)

            if language not in compiler_pkg.compiler_wrapper_link_paths:
                continue

            wrapper_path = bin_dir / compiler_pkg.compiler_wrapper_link_paths.get(language)

            env.set(wrapper_var_name, str(wrapper_path))
            env.set(f"SPACK_{wrapper_var_name}_RPATH_ARG", compiler_pkg.rpath_arg)

            uarch = dependent_spec.architecture.target
            version_number, _ = archspec.cpu.version_components(
                compiler_pkg.spec.version.dotted_numeric_string
            )
            try:
                isa_arg = uarch.optimization_flags(compiler_pkg.archspec_name(), version_number)
            except (ValueError, archspec.cpu.UnsupportedMicroarchitecture):
                isa_arg = ""

            if isa_arg:
                env.set(f"SPACK_TARGET_ARGS_{attr_name.upper()}", isa_arg)

            # Add spack build environment path with compiler wrappers first in
            # the path. We add the compiler wrapper path, which includes default
            # wrappers (cc, c++, f77, f90), AND a subdirectory containing
            # compiler-specific symlinks.  The latter ensures that builds that
            # are sensitive to the *name* of the compiler see the right name when
            # we're building with the wrappers.
            #
            # Conflicts on case-insensitive systems (like "CC" and "cc") are
            # handled by putting one in the <bin_dir>/case-insensitive
            # directory.  Add that to the path too.
            compiler_specific_dir = (
                bin_dir / compiler_pkg.compiler_wrapper_link_paths[language]
            ).parent

            for item in [bin_dir, compiler_specific_dir]:
                env_paths.append(item)
                ci = item / "case-insensitive"
                if ci.is_dir():
                    env_paths.append(ci)

            env.set(f"SPACK_{wrapper_var_name}_LINKER_ARG", compiler_pkg.linker_arg)

            # Check if this compiler has implicit rpaths
            implicit_rpaths.extend(_implicit_rpaths(pkg=compiler_pkg))

            # Add extra rpaths, if they are defined in an external spec
            extra_rpaths.extend(
                getattr(compiler_pkg.spec, "extra_attributes", {}).get("extra_rpaths", [])
            )

        if implicit_rpaths:
            # Implicit rpaths are accumulated across all compilers so, whenever they are mixed,
            # the compiler used in ccld mode will account for rpaths from other compilers too.
            implicit_rpaths = lang.dedupe(implicit_rpaths)
            env.set("SPACK_COMPILER_IMPLICIT_RPATHS", ":".join(implicit_rpaths))

        if extra_rpaths:
            extra_rpaths = lang.dedupe(extra_rpaths)
            env.set("SPACK_COMPILER_EXTRA_RPATHS", ":".join(extra_rpaths))

        env.set("SPACK_ENABLE_NEW_DTAGS", self.enable_new_dtags)
        env.set("SPACK_DISABLE_NEW_DTAGS", self.disable_new_dtags)

        for item in env_paths:
            env.prepend_path("SPACK_COMPILER_WRAPPER_PATH", item)

    def setup_dependent_package(self, module, dependent_spec):
        def _spack_compiler_attribute(*, language: str) -> str:
            compiler_pkg = dependent_spec[language].package
            if sys.platform != "win32":
                # On non-Windows we return the appropriate path to the compiler wrapper
                return str(self.bin_dir() / compiler_pkg.compiler_wrapper_link_paths[language])

            # On Windows we return the real compiler
            if language == "c":
                return compiler_pkg.cc
            elif language == "cxx":
                return compiler_pkg.cxx
            elif language == "fortran":
                return compiler_pkg.fortran

        if dependent_spec.has_virtual_dependency("c"):
            setattr(module, "spack_cc", _spack_compiler_attribute(language="c"))

        if dependent_spec.has_virtual_dependency("cxx"):
            setattr(module, "spack_cxx", _spack_compiler_attribute(language="cxx"))

        if dependent_spec.has_virtual_dependency("fortran"):
            setattr(module, "spack_fc", _spack_compiler_attribute(language="fortran"))
            setattr(module, "spack_f77", _spack_compiler_attribute(language="fortran"))

    @property
    def disable_new_dtags(self) -> str:
        if self.spec.satisfies("platform=darwin"):
            return ""
        return "--disable-new-dtags"

    @property
    def enable_new_dtags(self) -> str:
        if self.spec.satisfies("platform=darwin"):
            return ""
        return "--enable-new-dtags"


def _implicit_rpaths(pkg: spack.package_base.PackageBase) -> List[str]:
    detector = spack.compilers.libraries.CompilerPropertyDetector(pkg.spec)
    paths = detector.implicit_rpaths()
    return paths
