# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class LlvmOpenmp(CMakePackage):
    """The OpenMP subproject of LLVM contains the components required to build
    an executable OpenMP program that are outside the compiler itself."""

    homepage = "https://openmp.llvm.org/"
    url = "https://github.com/llvm/llvm-project/releases/download/llvmorg-14.0.6/openmp-14.0.6.src.tar.xz"

    license("Apache-2.0")

    version("16.0.0", sha256="e30f69c6533157ec4399193ac6b158807610815accfbed98695d72074e4bedd0")
    version("14.0.6", sha256="4f731ff202add030d9d68d4c6daabd91d3aeed9812e6a5b4968815cfdff0eb1f")
    version("12.0.1", sha256="60fe79440eaa9ebf583a6ea7f81501310388c02754dbe7dc210776014d06b091")
    version("9.0.0", sha256="9979eb1133066376cc0be29d1682bc0b0e7fb541075b391061679111ae4d3b5b")
    version("8.0.0", sha256="f7b1705d2f16c4fc23d6531f67d2dd6fb78a077dd346b02fed64f4b8df65c9d5")

    variant(
        "multicompat",
        default=False,
        description="Support gomp and the Intel openMP runtime library.",
    )

    depends_on("cmake@3.13.4:", when="@12:", type="build")
    depends_on("cmake@2.8:", type="build")
    depends_on("py-lit", type="test")
    depends_on("py-filecheck", type="test")
    # depends_on("llvm-utils", type="test")  # for "not"

    resource(
        name="cmake",
        url="https://github.com/llvm/llvm-project/releases/download/llvmorg-16.0.0/cmake-16.0.0.src.tar.xz",
        sha256="04e62ab7d0168688d9102680adf8eabe7b04275f333fe20eef8ab5a3a8ea9fcc",
        when="@16.0.0",
    )

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@14"):
            return "openmp-{}.src".format(self.version)
        else:
            return "."

    def url_for_version(self, version):
        if version >= Version("9.0.1"):
            url = "https://github.com/llvm/llvm-project/releases/download/llvmorg-{0}/openmp-{0}.src.tar.xz"
        else:
            url = "https://releases.llvm.org/{0}/openmp-{0}.src.tar.xz"

        return url.format(version)

    @when("@16:")
    def patch(self):
        src = os.path.join(self.stage.source_path, f"cmake-{self.version}.src")
        dst = os.path.join(self.stage.path, "cmake")
        os.rename(src, dst)

    def cmake_args(self):
        # Disable LIBOMP_INSTALL_ALIASES, otherwise the library is installed as
        # libgomp alias which can conflict with GCC's libgomp.
        cmake_args = ["-DLIBOMP_INSTALL_ALIASES=OFF"]
        # Add optional support for both Intel and gcc compilers
        if self.spec.satisfies("+multicompat"):
            cmake_args.append("-DKMP_GOMP_COMPAT=1")
        return cmake_args

    @property
    def libs(self):
        return find_libraries("libomp", root=self.prefix, recursive=True)
