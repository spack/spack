# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylaneLightningKokkos(CMakePackage, PythonExtension):
    """The PennyLane-Lightning-Kokkos plugin provides a fast state-vector simulator with Kokkos kernels."""

    homepage = "https://docs.pennylane.ai/projects/lightning-kokkos"
    git = "https://github.com/PennyLaneAI/pennylane-lightning-kokkos.git"
    url = (
        "https://github.com/PennyLaneAI/pennylane-lightning-kokkos/archive/refs/tags/v0.28.0.tar.gz"
    )
    tag = "v0.28.0"

    maintainers("vincentmr")

    version("main", branch="main")
    version("develop", commit="551edca8cb0d83c7ea5139ef91a25fe9780864ca")
    version("0.28.0", sha256="1d6f0ad9658e70cc6875e9df5710d1fa83a0ccbe21c5fc8daf4e76ab3ff59b73")

    # patch(
    #     "v0.28-spack_support.patch",
    #     when="@0.28.0",
    #     sha256="26e79a0a01fbd1d9364d2328ccdbdcdd5109ea289a4e79f86f7a8206bcb35419",
    # )

    backends = {
        "serial": (False, "enable Serial Kokkos backend (default)"),
        "openmp": (False, "enable OpenMP Kokkos backend"),
        "pthread": (False, "enable Pthread Kokkos backend"),
        "cuda": (False, "enable Cuda Kokkos backend"),
    }

    for backend in backends:
        deflt_bool, descr = backends[backend]
        variant(backend.lower(), default=deflt_bool, description=descr)
        depends_on(
            "kokkos+%s" % backend.lower(), when="+%s" % backend.lower(), type=("run", "build")
        )

    # variant("serial", default=True, description="Build serial backend")
    # variant("openmp", default=True, description="Build with OpenMP support")

    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )
    variant("cppbenchmarks", default=False, description="Build CPP benchmark examples")
    variant("cpptests", default=False, description="Build CPP tests")
    variant("native", default=False, description="Build natively for given hardware")
    variant("sanitize", default=False, description="Build with address sanitization")
    # variant("verbose", default=False, description="Build with full verbosity")
    # variant("warnings", default=False, description="Build with Kokkos warnings")

    extends("python")

    # hard dependencies
    depends_on("ninja", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("cmake@3.21:3.24,3.25.2:", type="build")

    # variant defined dependencies
    depends_on("llvm-openmp", when="+openmp %apple-clang")

    depends_on("py-pybind11", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-pennylane", type="run")

    # Test deps
    depends_on("py-pytest", type=("test"))
    depends_on("py-pytest-cov", type=("test"))
    depends_on("py-pytest-mock", type=("test"))
    depends_on("py-flaky", type=("test"))


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    build_directory = "build"

    def cmake_args(self):
        """
        Here we specify all variant options that can be dynamically specified at build time
        """
        args = [
            self.define_from_variant("CMAKE_BUILD_TYPE", "build_type"),
            # self.define_from_variant("CMAKE_VERBOSE_MAKEFILE:BOOL", "verbose"),
            self.define_from_variant("PLKOKKOS_ENABLE_NATIVE", "native"),
            self.define_from_variant("PLKOKKOS_BUILD_TESTS", "cpptests"),
            # self.define_from_variant("PLKOKKOS_ENABLE_WARNINGS", "warnings"),
            self.define_from_variant("PLKOKKOS_ENABLE_SANITIZER", "sanitize"),
        ]
        args.append("-DCMAKE_PREFIX_PATH=" + self.spec["kokkos"].prefix)
        return args

    def build(self, pkg, spec, prefix):
        super().build(pkg, spec, prefix)
        cm_args = ";".join([s[2:] for s in self.cmake_args()])
        args = ["-i", f"--define={cm_args}"]
        build_ext = Executable(f"{self.spec['python'].command.path} setup.py build_ext")
        build_ext(*args)

    def install(self, pkg, spec, prefix):
        pip_args = std_pip_args + [f"--prefix={prefix}", "."]
        pip(*pip_args)
        super().install(pkg, spec, prefix)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        pytest = which("pytest")
        pytest("tests")
