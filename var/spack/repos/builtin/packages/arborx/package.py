# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Arborx(CMakePackage, CudaPackage, ROCmPackage):
    """ArborX is a performance-portable library for geometric search"""

    homepage = "https://github.com/arborx/arborx"
    url = "https://github.com/arborx/arborx/archive/v1.1.tar.gz"
    git = "https://github.com/arborx/arborx.git"

    tags = ["e4s", "ecp"]

    maintainers("aprokop")

    test_requires_compiler = True

    version("master", branch="master")
    version("1.4.1", sha256="2ca828ef6615859654b233a7df17017e7cfd904982b80026ec7409eb46b77a95")
    version("1.4", sha256="803a1018a6305cf3fea161172b3ada49537f59261279d91c2abbcce9492ee7af")
    version("1.3", sha256="3f1e17f029a460ab99f8396e2772cec908eefc4bf3868c8828907624a2d0ce5d")
    version("1.2", sha256="ed1939110b2330b7994dcbba649b100c241a2353ed2624e627a200a398096c20")
    version("1.1", sha256="2b5f2d2d5cec57c52f470c2bf4f42621b40271f870b4f80cb57e52df1acd90ce")
    version("1.0", sha256="9b5f45c8180622c907ef0b7cc27cb18ba272ac6558725d9e460c3f3e764f1075")
    version(
        "0.9-beta",
        sha256="b349b5708d1aa00e8c20c209ac75dc2d164ff9bf1b85adb5437346d194ba6c0d",
        deprecated=True,
    )

    # Allowed C++ standard
    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "2a", "2b"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    conflicts("cxxstd=14", when="@1.3:")

    # ArborX relies on Kokkos to provide devices, providing one-to-one matching
    # variants. The only way to disable those devices is to make sure Kokkos
    # does not provide them.
    kokkos_backends = {
        "serial": (True, "enable Serial backend (default)"),
        "openmp": (False, "enable OpenMP backend"),
        "sycl": (False, "enable SYCL backend"),
    }

    variant("mpi", default=True, description="enable MPI")
    for backend in kokkos_backends:
        deflt, descr = kokkos_backends[backend]
        variant(backend.lower(), default=deflt, description=descr)
    variant("trilinos", default=False, description="use Kokkos from Trilinos")

    depends_on("cmake@3.12:", type="build")
    depends_on("cmake@3.16:", type="build", when="@1.0:")
    depends_on("mpi", when="+mpi")
    depends_on("rocthrust", when="+rocm")

    # Standalone Kokkos
    depends_on("kokkos@3.1.00:", when="~trilinos")
    depends_on("kokkos@3.4.00:", when="@1.2~trilinos")
    depends_on("kokkos@3.6.00:", when="@1.3~trilinos")
    depends_on("kokkos@3.7.01:", when="@1.4:~trilinos")
    for backend in kokkos_backends:
        depends_on("kokkos+%s" % backend.lower(), when="~trilinos+%s" % backend.lower())

    for arch in CudaPackage.cuda_arch_values:
        cuda_dep = "+cuda cuda_arch={0}".format(arch)
        depends_on("kokkos {0}".format(cuda_dep), when=cuda_dep)

    for arch in ROCmPackage.amdgpu_targets:
        rocm_dep = "+rocm amdgpu_target={0}".format(arch)
        depends_on("kokkos {0}".format(rocm_dep), when=rocm_dep)

    conflicts("+cuda", when="cuda_arch=none")
    depends_on("kokkos+cuda_lambda", when="~trilinos+cuda")

    # Trilinos/Kokkos
    # Notes:
    # - current version of Trilinos package does not allow disabling Serial
    # - current version of Trilinos package does not allow enabling CUDA
    depends_on("trilinos+kokkos", when="+trilinos")
    depends_on("trilinos+openmp", when="+trilinos+openmp")
    depends_on("trilinos@13.2.0:", when="@1.2+trilinos")
    depends_on("trilinos@13.4.0:", when="@1.3+trilinos")
    depends_on("trilinos@14.0.0:", when="@1.4:+trilinos")
    patch("trilinos14.0-kokkos-major-version.patch", when="@1.4+trilinos ^trilinos@14.0.0")
    conflicts("~serial", when="+trilinos")
    conflicts("+cuda", when="+trilinos")

    def cmake_args(self):
        spec = self.spec

        options = [
            "-DKokkos_ROOT=%s"
            % (spec["kokkos"].prefix if "~trilinos" in spec else spec["trilinos"].prefix),
            self.define_from_variant("ARBORX_ENABLE_MPI", "mpi"),
        ]

        if "+cuda" in spec:
            # Only Kokkos allows '+cuda' for now
            options.append("-DCMAKE_CXX_COMPILER=%s" % spec["kokkos"].kokkos_cxx)
        if "+rocm" in spec:
            options.append("-DCMAKE_CXX_COMPILER=%s" % spec["hip"].hipcc)

        return options

    examples_src_dir = "examples"

    @run_after("install")
    def setup_build_tests(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources([self.examples_src_dir])

    @property
    def cached_tests_work_dir(self):
        """The working directory for cached test sources."""
        return join_path(self.test_suite.current_test_cache_dir, self.examples_src_dir)

    def test_run_ctest(self):
        """run ctest tests on the installed package"""

        arborx_dir = self.spec["arborx"].prefix
        cmake_prefix_path = f"-DCMAKE_PREFIX_PATH={arborx_dir}"
        if "+mpi" in self.spec:
            cmake_prefix_path += f";{self.spec['mpi'].prefix}"

        cmake_args = [
            ".",
            cmake_prefix_path,
            f"-DCMAKE_CXX_COMPILER={os.environ['CXX']}",
            self.define(
                "Kokkos_ROOT",
                self.spec["kokkos"].prefix
                if "~trilinos" in self.spec
                else self.spec["trilinos"].prefix,
            ),
        ]
        cmake = which(self.spec["cmake"].prefix.bin.cmake)
        make = which("make")
        ctest = which("ctest")

        with working_dir(self.cached_tests_work_dir):
            cmake(*cmake_args)
            make()
            ctest("-V")
