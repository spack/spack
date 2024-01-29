# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylaneLightning(CMakePackage, PythonExtension):
    """The PennyLane-Lightning plugin provides a fast state-vector simulator written in C++."""

    homepage = "https://docs.pennylane.ai/projects/lightning"
    git = "https://github.com/PennyLaneAI/pennylane-lightning.git"
    url = "https://github.com/PennyLaneAI/pennylane-lightning/archive/refs/tags/v0.32.0.tar.gz"

    maintainers("mlxd", "AmintorDusko")

    license("Apache-2.0")

    version("master", branch="master")
    version("0.32.0", sha256="124edae1828c7e72e7b3bfbb0e75e98a07a490d7f1eab19eebb3311bfa8a23d4")
    version("0.31.0", sha256="b177243625b6fdac0699d163bbc330c92ca87fb9f427643785069273d2a255f6")
    version("0.30.0", sha256="0f4032409d20d00991b5d14fe0b2b928baca4a13c5a1b16eab91f61f9273e58d")
    version("0.29.0", sha256="da9912f0286d1a54051cc19cf8bdbdcd732795636274c95f376db72a88e52d85")

    variant("blas", default=True, description="Build with BLAS support")
    variant(
        "dispatcher",
        default=True,
        description="Build with AVX2/AVX512 gate automatic dispatching support",
    )
    variant("kokkos", default=True, description="Build with Kokkos support", when="@:0.31")
    variant("openmp", default=True, description="Build with OpenMP support")

    variant("native", default=False, description="Build natively for given hardware")
    variant("verbose", default=False, description="Build with full verbosity")

    variant("cpptests", default=False, description="Build CPP tests")
    variant("cppbenchmarks", default=False, description="Build CPP benchmark examples")

    extends("python")

    # hard dependencies
    depends_on("cmake@3.21:3.24,3.25.2:", type="build")
    depends_on("ninja", type=("run", "build"))

    # variant defined dependencies
    depends_on("blas", when="+blas")
    depends_on("kokkos@:4.0.01", when="@:0.31+kokkos")
    depends_on("kokkos-kernels@:4.0.01", when="@:0.31+kokkos")
    depends_on("llvm-openmp", when="+openmp %apple-clang")

    depends_on("python@3.8:", type=("build", "run"), when="@:0.31")
    depends_on("python@3.9:", type=("build", "run"), when="@0.32:")
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pybind11", type="link")
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")
    # depends_on("py-pennylane@0.28:", type=("build", "run"))  # circular dependency


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    build_directory = "build"

    def cmake_args(self):
        """
        Here we specify all variant options that can be dynamicaly specified at build time
        """
        args = [
            self.define_from_variant("ENABLE_OPENMP", "openmp"),
            self.define_from_variant("ENABLE_NATIVE", "native"),
            self.define_from_variant("ENABLE_BLAS", "blas"),
            self.define_from_variant("CMAKE_VERBOSE_MAKEFILE:BOOL", "verbose"),
            self.define_from_variant("BUILD_TESTS", "cpptests"),
            self.define_from_variant("BUILD_BENCHMARKS", "cppbenchmarks"),
            self.define_from_variant("ENABLE_GATE_DISPATCHER", "dispatcher"),
        ]

        if "+kokkos" in self.spec:
            args += [
                "-DENABLE_KOKKOS=ON",
                f"-DKokkos_Core_DIR={self.spec['kokkos'].home}",
                f"-DKokkos_Kernels_DIR={self.spec['kokkos-kernels'].home}",
            ]
        elif self.spec.version < Version("0.32"):
            args += ["-DENABLE_KOKKOS=OFF"]

        return args

    def build(self, pkg, spec, prefix):
        super().build(pkg, spec, prefix)
        cm_args = ";".join(
            [
                s[2:]
                for s in self.cmake_args()
                if s[2:] not in ["BUILD_TESTS:BOOL=ON", "BUILD_BENCHMARKS:BOOL=ON"]
            ]
        )
        args = ["-i", f"--define={cm_args}"]
        python("setup.py", "build_ext", *args)

    def install(self, pkg, spec, prefix):
        pip_args = std_pip_args + ["--prefix=" + prefix, "."]
        pip(*pip_args)
        super().install(pkg, spec, prefix)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_lightning_build(self):
        with working_dir(self.stage.source_path):
            pl_runner = Executable(self.prefix.bin.pennylane_lightning_test_runner)
            pl_runner()
