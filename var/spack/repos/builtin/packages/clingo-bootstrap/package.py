# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from spack.pkg.builtin.clingo import Clingo


class ClingoBootstrap(Clingo):
    """Clingo with some options used for bootstrapping"""

    maintainers("alalazo")

    variant("build_type", default="Release", values=("Release",), description="CMake build type")

    variant("static_libstdcpp", default=False, description="Require a static version of libstdc++")

    # CMake at version 3.16.0 or higher has the possibility to force the
    # Python interpreter, which is crucial to build against external Python
    # in environment where more than one interpreter is in the same prefix
    depends_on("cmake@3.16.0:", type="build")

    # On Linux we bootstrap with GCC
    for compiler_spec in [c for c in spack.compilers.supported_compilers() if c != "gcc"]:
        conflicts(
            "%{0}".format(compiler_spec),
            when="platform=linux",
            msg="GCC is required to bootstrap clingo on Linux",
        )
        conflicts(
            "%{0}".format(compiler_spec),
            when="platform=cray",
            msg="GCC is required to bootstrap clingo on Cray",
        )
    conflicts("%gcc@:5", msg="C++14 support is required to bootstrap clingo")

    # On Darwin we bootstrap with Apple Clang
    for compiler_spec in [c for c in spack.compilers.supported_compilers() if c != "apple-clang"]:
        conflicts(
            "%{0}".format(compiler_spec),
            when="platform=darwin",
            msg="Apple-clang is required to bootstrap clingo on MacOS",
        )

    # Clingo needs the Python module to be usable by Spack
    conflicts("~python", msg="Python support is required to bootstrap Spack")

    @property
    def cmake_py_shared(self):
        return self.define("CLINGO_BUILD_PY_SHARED", "OFF")

    def cmake_args(self):
        args = super().cmake_args()
        args.extend(
            [
                # Avoid building the clingo executable
                self.define("CLINGO_BUILD_APPS", "OFF")
            ]
        )
        return args

    def setup_build_environment(self, env):
        opts = None
        if "%apple-clang platform=darwin" in self.spec:
            opts = "-mmacosx-version-min=10.13"
        elif "%gcc" in self.spec:
            if "+static_libstdcpp" in self.spec:
                # This is either linux or cray
                opts = "-static-libstdc++ -static-libgcc -Wl,--exclude-libs,ALL"
        elif "platform=windows" in self.spec:
            pass
        else:
            msg = 'unexpected compiler for spec "{0}"'.format(self.spec)
            raise RuntimeError(msg)

        if opts:
            env.set("CXXFLAGS", opts)
            env.set("LDFLAGS", opts)
