# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAmrex(PythonPackage, CudaPackage, ROCmPackage):
    """AMReX Python Bindings with pybind11"""

    homepage = "https://amrex-codes.github.io/amrex/"
    url = "https://github.com/AMReX-Codes/pyamrex/archive/refs/tags/24.04.tar.gz"
    git = "https://github.com/AMReX-Codes/pyamrex.git"

    maintainers("ax3l", "RTSandberg", "sayerhs", "WeiqunZhang")

    license("BSD-3-Clause-LBNL")

    version("develop", branch="development")
    version("24.04", sha256="ab85695bb9644b702d0fc84e77205d264d27ba94999cab912c8a3212a7eb77fc")
    version("24.03", sha256="bf85b4ad35b623278cbaae2c07e22138545dec0732d15c4ab7c53be76a7f2315")

    for v in ["24.04", "24.03"]:
        depends_on("amrex@{0}".format(v), when="@{0}".format(v), type=("build", "link"))

    variant(
        "dimensions",
        default="1,2,3",
        values=("1", "2", "3"),
        multi=True,
        description="Dimensionality",
    )
    variant("mpi", default=True, description="Build with MPI support")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant(
        "precision",
        default="double",
        description="Real precision (double/single)",
        values=("single", "double"),
    )
    variant("tiny_profile", default=False, description="Enable tiny profiling")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-numpy@1.15.0:1", type=("build", "run"))
    depends_on("py-mpi4py@2.1.0:", type=("build", "run"), when="+mpi")
    depends_on("py-packaging@23:", type="build")
    depends_on("py-setuptools@42:", type="build")
    # We just need a CMake binary, and py-cmake is notoriously hard to build on
    # exotic architectures. So ignore the pyproject.toml declaration and use
    # Spack's cmake package.
    # depends_on('py-cmake@3.20:3', type='build')
    depends_on("cmake@3.20:3", type="build")
    depends_on("py-pybind11@2.11.1:", type="link")

    # AMReX options
    #   required variants
    depends_on("amrex +shared +pic +particles")
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

    depends_on("py-pytest", type="test")
    depends_on("py-pandas", type="test")
    depends_on("py-cupy", type="test", when="+cuda")

    tests_src_dir = "tests/"

    def setup_build_environment(self, env):
        spec = self.spec

        # disable superbuilds: use external dependencies
        env.set("AMREX_INTERNAL", "OFF")
        env.set("PYAMREX_CCACHE", "ON")
        env.set("PYAMREX_IPO", "ON")
        env.set("PYBIND11_INTERNAL", "OFF")

        # configure to require the exact AMReX configs provided by Spack
        env.set("AMREX_SPACEDIM", ";".join(spec.variants["dimensions"].value))
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

    def check(self):
        """Checks after the build phase"""
        pytest = which("pytest")
        pytest(join_path(self.stage.source_path, self.tests_src_dir))

    @run_after("install")
    def copy_test_sources(self):
        """Copy the example test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, [self.tests_src_dir])

    def test(self):
        """Perform smoke tests on the installed package."""
        pytest = which("pytest")
        pytest(join_path(install_test_root(self), self.tests_src_dir))
