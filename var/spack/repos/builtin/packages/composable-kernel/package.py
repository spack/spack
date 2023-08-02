# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class ComposableKernel(CMakePackage):
    """Composable Kernel: Performance Portable Programming Model
    for Machine Learning Tensor Operators."""

    homepage = "https://github.com/ROCmSoftwarePlatform/composable_kernel"
    git = "https://github.com/ROCmSoftwarePlatform/composable_kernel.git"

    maintainers("srekolam", "afzpatel")

    version("5.5.1", commit="ac9e01e2cc3721be24619807adc444e1f59a9d25")
    version("5.5.0", commit="8b76b832420a3d69708401de6607a033163edcce")
    version("5.4.3", commit="bb3d9546f186e39cefedc3e7f01d88924ba20168")
    version("5.4.0", commit="236bd148b98c7f1ec61ee850fcc0c5d433576305")

    depends_on("python", type="build")
    depends_on("z3", type="link")
    depends_on("zlib", type="link")
    depends_on("ncurses+termlib", type="link")
    depends_on("bzip2")
    depends_on("sqlite")
    depends_on("half")
    depends_on("pkgconfig", type="build")
    depends_on("cmake@3.16:", type="build")

    for ver in [
        "5.5.1",
        "5.5.0",
        "5.4.3",
        "5.4.0",
    ]:
        depends_on("hip@" + ver, when="@" + ver)
        depends_on("llvm-amdgpu@" + ver, when="@" + ver)
        depends_on("rocm-cmake@" + ver, when="@" + ver, type="build")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define(
                "CMAKE_CXX_COMPILER", "{0}/bin/clang++".format(spec["llvm-amdgpu"].prefix)
            ),
            self.define("CMAKE_C_COMPILER", "{0}/bin/clang".format(spec["llvm-amdgpu"].prefix)),
            self.define("HIP_PATH", spec["hip"].prefix),
            self.define("HIP_ROOT_DIR", "{0}".format(spec["hip"].prefix)),
            self.define("CMAKE_CXX_FLAGS", "-O3"),
            self.define("CMAKE_BUILD_TYPE", "Release"),
        ]
        return args

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            # only instances is necessary to build and install
            make("instances")
