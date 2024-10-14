# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Arrayfire(CMakePackage, CudaPackage):
    """ArrayFire is a high performance software library for parallel computing
    with an easy-to-use API. Its array based function set makes parallel
    programming more accessible."""

    homepage = "https://arrayfire.org/docs/index.htm"
    git = "https://github.com/arrayfire/arrayfire.git"
    maintainers("umar456")

    license("FreeImage")

    with default_args(submodules=True, no_cache=True):
        version("master")
        version("3.9.0", commit="b59a1ae535da369db86451e5b28a7bc0eaf3e84a", tag="v3.9.0")
        version("3.8.1", commit="823e8e399fe8c120c6ec7ec75f09e6106b3074ca", tag="v3.8.1")
        version("3.7.3", commit="59ac7b980d1ae124aae914fb29cbf086c948954d", tag="v3.7.3")
        version("3.7.2", commit="218dd2c99300e77496239ade76e94b0def65d032", tag="v3.7.2")
        version("3.7.0", commit="fbea2aeb6f7f2d277dcb0ab425a77bb18ed22291", tag="v3.7.0")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cmake@3.18:", type="build", when="@3.9:")

    variant("forge", default=False, description="Enable graphics library")
    variant("opencl", default=False, description="Enable OpenCL backend")
    variant("cuda", default=True, description="Enable CUDA backend")

    conflicts("~opencl", when="@3.9:")

    conflicts("%gcc@13:", when="@:3.8.1")
    conflicts("%lang@14:", when="@:3.8.1")

    depends_on("boost@1.70:")
    conflicts("boost@1.86:", when="@3.9", msg="arrayfire@3.9.0 fails to build with boost@1.86:")

    depends_on("fftw-api@3:")
    depends_on("blas")

    # arrayfire@3.8.1 fails to build with spdlog and fmt:
    depends_on("fmt@8.1.1:", when="@3.7")
    depends_on("fmt@8.1.1:", when="@3.9:")
    depends_on("spdlog@1.9.2:", when="@3.7")
    depends_on("spdlog@1.9.2:", when="@3.9:")

    # https://github.com/arrayfire/arrayfire/wiki/Build-Instructions-for-Linux
    depends_on("cuda@9.1:", when="+cuda")
    depends_on("cudnn", when="+cuda")

    depends_on("opencl", when="+opencl")
    depends_on("pocl+icd", when="^[virtuals=opencl] pocl")

    # TODO add more opencl backends:
    # currently only Cuda backend is enabled
    # https://github.com/arrayfire/arrayfire/wiki/Build-Instructions-for-Linux#opencl-backend-dependencies

    depends_on("fontconfig", when="+forge")
    depends_on("glfw@3.1.4:", when="+forge")

    # 3.9.0 introduced a cmake bug due to absolute paths being used.
    # add_subdirectory not given a binary directory... (referencing internal build of span-lite).
    patch("add-build-dir-to-cmake.patch", level=0, when="@3.9.0:")
    # from Arch Linux https://gitlab.archlinux.org/archlinux/packaging/packages/arrayfire/-/raw/main/fmt-v11.patch?ref_type=heads
    patch("fmt-v11.patch", level=1, when="@3.9.0:")
    # https://gitlab.archlinux.org/archlinux/packaging/packages/arrayfire/-/blob/6add204c734deaed234c71f2a05c3e7bcf6f73dc/3521-fix-build-failure-with-cudnn.patch
    patch("3521-fix-build-failure-with-cudnn.patch", level=1, when="@3.9.0:")

    conflicts("cuda_arch=none", when="+cuda", msg="CUDA architecture is required")

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters

        libraries = []
        if "cpu" in query_parameters:
            libraries.append("libafcpu")
        if "cuda" in query_parameters and "+cuda" in self.spec:
            libraries.append("libafcuda")
        if "opencl" in query_parameters and "+opencl" in self.spec:
            libraries.append("libafopencl")
        if not query_parameters or "unified" in query_parameters:
            libraries.append("libaf")

        return find_libraries(libraries, root=self.prefix, recursive=True)

    def cmake_args(self):
        args = []
        args.extend(
            [
                self.define_from_variant("AF_BUILD_CUDA", "cuda"),
                self.define_from_variant("AF_BUILD_FORGE", "forge"),
                self.define_from_variant("AF_BUILD_OPENCL", "opencl"),
                self.define("BUILD_TESTING", self.run_tests),
                self.define("AF_WITH_SPDLOG_HEADER_ONLY", not self.spec.satisfies("@3.8")),
                self.define("AF_WITH_FMT_HEADER_ONLY", not self.spec.satisfies("@3.8")),
            ]
        )

        if self.spec.satisfies("+cuda"):
            arch_list = [
                "{}.{}".format(arch[:-1], arch[-1])
                for arch in self.spec.variants["cuda_arch"].value
            ]
            args.append(self.define("CUDA_architecture_build_targets", arch_list))

        if self.spec["blas"].name in INTEL_MATH_LIBRARIES:
            if self.version >= Version("3.8.0"):
                args.append(self.define("AF_COMPUTE_LIBRARY", "Intel-MKL"))
            else:
                args.append(self.define("USE_CPU_MKL", True))
                args.append(self.define("USE_OPENCL_MKL", True))
            if "%intel" not in self.spec:
                args.append(self.define("MKL_THREAD_LAYER", "GNU OpenMP"))
        else:
            if self.version >= Version("3.8.0"):
                args.append(self.define("AF_COMPUTE_LIBRARY", "FFTW/LAPACK/BLAS"))
            else:
                args.append(self.define("USE_CPU_MKL", False))
                args.append(self.define("USE_OPENCL_MKL", False))

        return args
