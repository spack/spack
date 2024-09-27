# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Alpaka(CMakePackage, CudaPackage):
    """Abstraction Library for Parallel Kernel Acceleration."""

    homepage = "https://github.com/alpaka-group/alpaka"
    url = "https://github.com/alpaka-group/alpaka/archive/refs/tags/0.6.0.tar.gz"
    git = "https://github.com/alpaka-group/alpaka.git"

    maintainers("vvolkl")

    license("MPL-2.0-no-copyleft-exception")

    version("develop", branch="develop")
    version("1.1.0", sha256="95a8f1b706105d8a213116b6ba00e27bd904855c377f5a22a04aa0b86054dc35")
    version("1.0.0", sha256="38223dc1ca5bcf3916ff91f8825fb8caab7047430877222847e0ceb93bffecc9")
    version("0.9.0", sha256="3b2a5631366619fab5f3ceaf860219362f35db6c1148a601a3779a836cf29363")
    version("0.8.0", sha256="e01bc377a7657d9a3e0c5f8d3f83dffbd7d0b830283c59efcbc1fb98cf88de43")
    version("0.7.0", sha256="4b61119a7b3b073f281ba15b63430db98b77dbd9420bc290a114f80121fbdd97")

    depends_on("cxx", type="build")  # generated

    variant(
        "backend",
        multi=True,
        values=(
            "serial",
            "threads",
            "tbb",
            "omp2_gridblock",
            "omp2_blockthread",
            "cuda",
            "cuda_only",
            "hip",
            "hip_only",
        ),
        description="Backends to enable",
        default="serial",
    )

    variant("examples", default=False, description="Build alpaka examples")

    depends_on("boost@1.74:")
    depends_on("cmake@3.22:")

    # make sure no other backend is enabled if using cuda_only or hip_only
    for v in (
        "serial",
        "threads",
        "tbb",
        "omp2_gridblock",
        "omp2_blockthread",
        "cuda",
        "hip",
    ):
        conflicts("backend=cuda_only,%s" % v)
        conflicts("backend=hip_only,%s" % v)
    conflicts("backend=cuda_only,hip_only")

    # todo: add conflict between cuda 11.3 and gcc 10.3.0
    # see https://github.com/alpaka-group/alpaka/issues/1297

    def cmake_args(self):
        spec = self.spec
        args = []
        if spec.satisfies("backend=serial"):
            args.append(self.define("ALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLE", True))
        if self.spec.satisfies("backend=threads"):
            args.append(self.define("ALPAKA_ACC_CPU_B_SEQ_T_THREADS_ENABLE", True))
        if spec.satisfies("backend=tbb"):
            args.append(self.define("ALPAKA_ACC_CPU_B_TBB_T_SEQ_ENABLE", True))
        if spec.satisfies("backend=omp2_gridblock"):
            args.append(self.define("ALPAKA_ACC_CPU_B_OMP2_T_SEQ_ENABLE", True))
        if spec.satisfies("backend=omp2_blockthread"):
            args.append(self.define("ALPAKA_ACC_CPU_B_SEQ_T_OMP2_ENABLE", True))
        if spec.satisfies("backend=cuda"):
            args.append(self.define("ALPAKA_ACC_GPU_CUDA_ENABLE", True))
        if spec.satisfies("backend=cuda_only"):
            args.append(self.define("ALPAKA_ACC_GPU_CUDA_ENABLE", True))
            args.append(self.define("ALPAKA_ACC_GPU_CUDA_ONLY_MODE", True))
        if spec.satisfies("backend=hip"):
            args.append(self.define("ALPAKA_ACC_GPU_HIP_ENABLE", True))
        if spec.satisfies("backend=hip_only"):
            args.append(self.define("ALPAKA_ACC_GPU_HIP_ENABLE", True))
            args.append(self.define("ALPAKA_ACC_GPU_HIP_ONLY_MODE", True))

        args.append(self.define_from_variant("alpaka_BUILD_EXAMPLES", "examples"))
        # need to define, as it is explicitly declared as an option by alpaka:
        args.append(self.define("BUILD_TESTING", self.run_tests))
        return args
