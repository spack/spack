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

    version("master", branch="develop")
    version("5.6.1", commit="f5ec04f091fa5c48c67d7bacec36a414d0be06a5")
    version("5.6.0", commit="f5ec04f091fa5c48c67d7bacec36a414d0be06a5")
    version("5.5.1", commit="ac9e01e2cc3721be24619807adc444e1f59a9d25")
    version("5.5.0", commit="8b76b832420a3d69708401de6607a033163edcce")
    version("5.4.3", commit="bb3d9546f186e39cefedc3e7f01d88924ba20168")
    version("5.4.0", commit="236bd148b98c7f1ec61ee850fcc0c5d433576305")

    amdgpu_targets = ROCmPackage.amdgpu_targets
    variant(
        "amdgpu_target",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
        description="set gpu targets",
    )

    depends_on("python", type="build")
    depends_on("z3", type="build")
    depends_on("zlib", type="build")
    depends_on("ncurses+termlib", type="build")
    depends_on("bzip2", type="build")
    depends_on("sqlite", type="build")
    depends_on("half", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("cmake@3.16:", type="build")

    for ver in ["master", "5.6.1", "5.6.0", "5.5.1", "5.5.0", "5.4.3", "5.4.0"]:
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
        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))
        if self.spec.satisfies("@5.6.0:"):
            args.append(self.define("INSTANCES_ONLY", "ON"))
        return args

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            # only instances is necessary to build and install
            if self.spec.satisfies("@5.6.0:"):
                make()
            else:
                make("instances")
