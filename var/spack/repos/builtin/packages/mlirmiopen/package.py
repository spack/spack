# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mlirmiopen(CMakePackage):
    """Multi-Level Intermediate Representation for rocm miopen project."""

    homepage = "https://github.com/ROCmSoftwarePlatform/llvm-project-mlir"
    url = "https://github.com/ROCmSoftwarePlatform/llvm-project-mlir/archive/refs/tags/rocm-5.4.0.tar.gz"
    git = "https://github.com/ROCmSoftwarePlatform/llvm-project-mlir.git"
    tags = ["rocm"]

    maintainers("srekolam")

    version("5.4.0", sha256="3823f455ee392118c3281e27d45fa0e5381f3c4070eb4e06ba13bc6b34a90a60")
    version("5.3.3", sha256="e9aa407df775d00fdb9404689f69ac755575188f8b25c6bd0fa9599928c5c57f")
    version("5.3.0", sha256="e8471a13cb39d33adff34730d3162adaa5d20f9544d61a6a94b39b9b5762ad6d")
    version("5.2.3", sha256="29e1c352d203622fa083432d5d368caccb53ba141119fbb7e8d5247d99854625")
    version("5.2.1", sha256="9e305e05474076d84c78b7a796bca20b64c70ee3e2caa066c625216c5ee21d95")
    version("5.2.0", sha256="546121f203e7787d3501fbaf6673bdbeefbb39e0446b02c480454338362a1f01")
    version("5.1.3", sha256="936f92707ffe9a1973728503db6365bb7f14e5aeccfaef9f0924e54d25080c69")
    version("5.1.0", sha256="56dab11877295784cbb754c10bf2bd6535a3dfea31ec0b97ffe77b94115109dc")

    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )

    def patch(self):
        if self.spec.satisfies("@5.3.0:"):
            filter_file(
                "${ROCM_PATH}/bin",
                self.spec["rocminfo"].prefix.bin,
                "external/llvm-project/mlir/lib/ExecutionEngine/CMakeLists.txt",
                string=True,
            )

    depends_on("python", type="build")
    depends_on("z3", type="link")
    depends_on("zlib", type="link")
    depends_on("ncurses+termlib", type="link")
    depends_on("bzip2")
    depends_on("sqlite")
    depends_on("half")
    depends_on("pkgconfig", type="build")

    for ver in ["5.1.0", "5.1.3", "5.2.0", "5.2.1", "5.2.3", "5.3.0", "5.3.3", "5.4.0"]:
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("llvm-amdgpu@" + ver, when="@" + ver)
        depends_on("hsa-rocr-dev@" + ver, when="@" + ver)
        depends_on("rocm-cmake@" + ver, type="build", when="@" + ver)
        depends_on("rocminfo@" + ver, type="build", when="@" + ver)

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
