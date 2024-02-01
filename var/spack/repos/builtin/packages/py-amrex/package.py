# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAmrex(PythonPackage, CudaPackage, ROCmPackage):
    """AMReX Python Bindings with pybind11"""

    homepage = "https://amrex-codes.github.io/amrex/"
    git = "https://github.com/AMReX-Codes/pyamrex.git"

    maintainers("ax3l", "RTSandberg", "sayerhs", "WeiqunZhang")

    version("develop", branch="development")

    variant("dimensions", default="3", description="Dimensionality", values=("1", "2", "3"))
    variant("mpi", default=True, description="Build with MPI support")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant(
        "precision",
        default="double",
        description="Real precision (double/single)",
        values=("single", "double"),
    )
    variant("tiny_profile", default=False, description="Enable tiny profiling")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-numpy@1.15.0:1", type=("build", "run"))
    depends_on("py-mpi4py@2.1.0:", type=("build", "run"), when="+mpi")
    depends_on("py-setuptools@42:", type="build")
    # We just need a CMake binary, and py-cmake is notoriously hard to build on
    # exotic architectures. So ignore the pyproject.toml declaration and use
    # Spack's cmake package.
    # depends_on('py-cmake@3.20:3', type='build')
    depends_on("cmake@3.20:3", type="build")
    depends_on("py-pybind11@2.9.1:", type="link")

    # AMReX options
    depends_on("amrex@22.08:", type=("build", "link"))
    #   required variants
    depends_on("amrex +pic +particles")
    #   controllable variants
    with when("dimensions=1"):
        depends_on("amrex dimensions=1")
    with when("dimensions=2"):
        depends_on("amrex dimensions=2")
    with when("dimensions=3"):
        depends_on("amrex dimensions=3")
    with when("+mpi"):
        depends_on("amrex +mpi")
    with when("+openmp"):
        depends_on("amrex +openmp")
    with when("+tiny_profile"):
        depends_on("amrex +tiny_profile")
    with when("+cuda"):
        depends_on("amrex +cuda")
        # todo: how to forward cuda_arch?
    with when("+rocm"):
        depends_on("amrex +rocm")
        # todo: how to forward amdgpu_target?

    def setup_build_environment(self, env):
        spec = self.spec

        # disable superbuilds: use external dependencies
        env.set("AMREX_INTERNAL", "OFF")
        env.set("PYBIND11_INTERNAL", "OFF")

        # configure to require the exact AMReX configs provided by Spack
        env.set("AMREX_SPACEDIM", spec.variants["dimensions"].value)
        env.set("AMREX_MPI", "ON" if spec.satisfies("+mpi") else "OFF")
        env.set("AMREX_OMP", "ON" if spec.satisfies("+omp") else "OFF")
        env.set("AMREX_PRECISION", spec.variants["precision"].value.upper())
        with when("+cuda"):
            env.set("AMREX_GPU_BACKEND", "CUDA")
        with when("+rocm"):
            env.set("AMREX_GPU_BACKEND", "HIP")
        # with when("+sycl"):
        #     env.set("AMREX_GPU_BACKEND", "SYCL")

        # control build parallelism
        env.set("CMAKE_BUILD_PARALLEL_LEVEL", make_jobs)
