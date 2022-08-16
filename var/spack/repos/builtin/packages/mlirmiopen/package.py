# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mlirmiopen(CMakePackage):
    """Multi-Level Intermediate Representation for rocm miopen project."""

    homepage = "https://github.com/ROCmSoftwarePlatform/llvm-project-mlir"
    url = "https://github.com/ROCmSoftwarePlatform/llvm-project-mlir/archive/refs/tags/rocm-5.2.0.tar.gz"
    git = "https://github.com/ROCmSoftwarePlatform/llvm-project-mlir.git"
    tags = ["rocm"]

    maintainers = ["srekolam"]

    version("5.2.0", sha256="546121f203e7787d3501fbaf6673bdbeefbb39e0446b02c480454338362a1f01")
    version("5.1.3", sha256="936f92707ffe9a1973728503db6365bb7f14e5aeccfaef9f0924e54d25080c69")
    version("5.1.0", sha256="56dab11877295784cbb754c10bf2bd6535a3dfea31ec0b97ffe77b94115109dc")

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    depends_on("python", type="build")
    depends_on("z3", type="link")
    depends_on("zlib", type="link")
    depends_on("ncurses+termlib", type="link")
    depends_on("bzip2")
    depends_on("sqlite")
    depends_on("half")
    depends_on("pkgconfig", type="build")

    for ver in ["5.1.0", "5.1.3", "5.2.0"]:
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("llvm-amdgpu@" + ver, when="@" + ver)
        depends_on("hsa-rocr-dev@" + ver, when="@" + ver)
        depends_on("rocm-cmake@" + ver, type="build", when="@" + ver)

    def cmake_args(self):
        spec = self.spec
        llvm_projects = ["mlir", "lld"]
        args = [
            self.define(
                "CMAKE_CXX_COMPILER", "{0}/bin/clang++".format(spec["llvm-amdgpu"].prefix)
            ),
            self.define("CMAKE_C_COMPILER", "{0}/bin/clang".format(spec["llvm-amdgpu"].prefix)),
            self.define("HIP_PATH", spec["hip"].prefix),
            self.define("BUILD_FAT_LIBMLIRMIOPEN", "ON"),
        ]
        args.extend([self.define("LLVM_ENABLE_PROJECTS", ";".join(llvm_projects))])
        return args
