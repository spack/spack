# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class PyAmrex(CMakePackage, PythonExtension, CudaPackage, ROCmPackage):
    """AMReX Python Bindings with pybind11"""

    homepage = "https://amrex-codes.github.io/amrex/"
    url = "https://github.com/AMReX-Codes/pyamrex/archive/refs/tags/24.10.tar.gz"
    git = "https://github.com/AMReX-Codes/pyamrex.git"

    maintainers("ax3l", "RTSandberg", "sayerhs", "WeiqunZhang")

    license("BSD-3-Clause-LBNL")

    version("develop", branch="development")
    version("24.10", sha256="dc1752ed3fbd5113dcfdbddcfe6c3c458e572b288ac9d41ed3ed7db130591d74")

    for v in ["24.10", "develop"]:
        depends_on("amrex@{0}".format(v), when="@{0}".format(v), type=("build", "link"))

    # CMake: Fix List of Pip Options
    patch(
        "https://github.com/AMReX-Codes/pyamrex/pull/377.patch?full_index=1",
        sha256="57e3e0a777b69895026f1527dc062647a7f2cc356154fa6e05a48f1d7c9bee16",
        when="@24.10",
    )

    variant(
        "dimensions",
        default="1,2,3",
        values=("1", "2", "3"),
        multi=True,
        description="Dimensionality",
    )
    # Spack defaults to False but pybind11 defaults to True (and IPO is highly
    # encouraged to be used with pybind11 projects)
    variant("ipo", default=True, description="CMake interprocedural optimization")
    variant("mpi", default=True, description="Build with MPI support")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant(
        "precision",
        default="double",
        description="Real precision (double/single)",
        values=("single", "double"),
    )
    variant("tiny_profile", default=False, description="Enable tiny profiling")
    variant("sycl", default=False, description="Enable SYCL backend")

    extends("python")

    depends_on("cxx", type="build")

    depends_on("cmake@3.20:3", type="build", when="@:24.08")
    depends_on("cmake@3.24:3", type="build", when="@24.09:")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-mpi4py@2.1.0:", type=("build", "run"), when="+mpi")
    depends_on("py-numpy@1.15:", type=("build", "run"))
    depends_on("py-packaging@23:", type="build")
    depends_on("py-pip@23:", type="build")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-pybind11@2.12.0:", type=("build", "link"))
    depends_on("py-wheel@0.40:", type="build")

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
    with when("~mpi"):
        depends_on("amrex ~mpi")
    with when("+openmp"):
        depends_on("amrex +openmp")
    with when("~openmp"):
        depends_on("amrex ~openmp")
    with when("+tiny_profile"):
        depends_on("amrex +tiny_profile")
    with when("+cuda"):
        depends_on("amrex +cuda")
        # todo: how to forward cuda_arch?
    with when("~cuda"):
        depends_on("amrex ~cuda")
    with when("+rocm"):
        depends_on("amrex +rocm")
        # todo: how to forward amdgpu_target?
    with when("~rocm"):
        depends_on("amrex ~rocm")
    with when("+sycl"):
        depends_on("amrex +sycl")
    with when("~sycl"):
        depends_on("amrex ~sycl")

    depends_on("py-pytest", type="test")
    depends_on("py-pandas", type="test")
    depends_on("py-cupy", type="test", when="+cuda")

    phases = ("cmake", "build", "install")
    build_targets = ["all", "pip_wheel", "pip_install_nodeps"]

    tests_src_dir = "tests/"

    def cmake_args(self):
        pip_args = PythonPipBuilder.std_args(self) + [f"--prefix={self.prefix}"]
        idx = pip_args.index("install")
        # Docs: https://pyamrex.readthedocs.io/en/24.10/install/cmake.html#build-options
        return [
            "-DpyAMReX_amrex_internal=OFF",
            "-DpyAMReX_pybind11_internal=OFF",
            "-DPY_PIP_OPTIONS=" + ";".join(pip_args[:idx]),
            "-DPY_PIP_INSTALL_OPTIONS=" + ";".join(pip_args[idx + 1 :]),
        ]

    def check(self):
        """Checks after the build phase"""
        pytest = which("pytest")
        pytest(join_path(self.stage.source_path, self.tests_src_dir))

    @run_after("install")
    def copy_test_sources(self):
        """Copy the example test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, [self.tests_src_dir])

    def test_pytest(self):
        """Perform smoke tests on the installed package."""
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.tests_src_dir)
        with working_dir(test_dir):
            pytest = which("pytest")
            # TODO: Remove once test dependencies made available
            assert pytest is not None, "Make sure a suitable 'pytest' is in your path"
            pytest()
