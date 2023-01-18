# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylaneLightning(PythonPackage):
    """The PennyLane-Lightning plugin provides a fast state-vector simulator written in C++."""

    homepage = "https://github.com/PennyLaneAI/pennylane-lightning"
    git = "https://github.com/PennyLaneAI/pennylane-lightning.git"
    url = "https://github.com/PennyLaneAI/pennylane-lightning/archive/refs/tags/v0.28.0.tar.gz"

    maintainers = ["mlxd, AmintorDusko"]
    phases = ["build_ext", "install"]

    version("develop", branch="master")
    version("0.28.0",  sha256="f5849c2affb5fb57aca20feb40ca829d171b07db2304fde0a37c2332c5b09e18")
    version("0.28.1",  sha256="038bc11ec913c3b90dd056bd0b134920db0ec5ff6f6a0bb94db6eaa687ce6618")

    # hard dependencies needed to build package
    depends_on('cmake@3.21.0:', type='build') #3.21 and newer
    depends_on('ninja', type='build')

    variant("python",  default=True,  description="Build with Python support")
    variant("native",  default=False, description="Build natively for given hardware")
    variant("blas",    default=False, description="Build with BLAS support")
    variant("openmp",  default=True,  description="Build with OpenMP support")
    variant("kokkos",  default=True,  description="Build with Kokkos support")
    variant("verbose", default=False, description="Build with full verbosity")

    variant('cpptests', default=False, description='Build CPP tests')
    # variant('cppbenchmark', default=False, description='Build CPP benchmark examples')

    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )

    # variant defined dependencies
    depends_on("blas", when="+blas")
    depends_on("kokkos@3.7.00", when="+kokkos")
    depends_on("kokkos-kernels@3.7.00", when="+kokkos")
    # depends_on("llvm-openmp", when="+openmp %apple-clang")

    depends_on("python@3.8:", type=("build", "run"), when="+python")
    depends_on("py-setuptools", type="build", when="+python")


    # depends_on("py-pennylane", type=("build", "run"), when="+python") # circular dependency?
    # At this moment, in Spack, we have py-pennylane depending on py-pennylane-lightning.

    depends_on("py-numpy", type=("build", "run"), when="+python")
    depends_on("py-pybind11", type=("build"), when="+python")
    depends_on("py-pip", type="build", when="+python")

    def cmake_args(self):
        """
        Here we specify all variant options that can be dynamicaly specified at build time
        """

        args = [f"-DCMAKE_BUILD_TYPE={self.spec.variants['build_type'].value}"]
        if self.spec.variants['native'].value:
            args += ["-DENABLE_NATIVE=ON"]
        if self.spec.variants['blas'].value:
            args += ["-DENABLE_BLAS=ON"]
        if not self.spec.variants['openmp'].value:
            args += ["-DENABLE_OPENMP=OFF"]
        if not self.spec.variants['kokkos'].value:
            args += ["-DENABLE_KOKKOS=OFF"]
        else:
            args += [   "-DENABLE_KOKKOS=ON",
                        f"-DKokkos_Core_DIR={self.spec['kokkos'].home}",
                        f"-DKokkos_Kernels_DIR={self.spec['kokkos-kernels'].home}",
                    ]

        if self.spec.variants['verbose'].value:
            args += ["-DCMAKE_VERBOSE_MAKEFILE=ON"]

        if not self.spec.variants['python'].value:
            args += ["-DENABLE_PYTHON=OFF"]

        # Build tests
        if self.spec.variants['cpptests'].value:
            args += ["-DBUILD_TESTS=ON"]
    #     # Build benchmarks
    #     if self.spec.variants['cppbenchmark'].value:
    #         args += ["-DBUILD_BENCHMARKS=ON"]

        return args

    def build_ext(self, spec, prefix):
        if self.spec.variants['python'].value:
            cm_args = ";".join([s[2:] for s in self.cmake_args()])
            args = ["-i", f"--define={cm_args}"]
            build_ext = Executable(f"{self.spec['python'].command.path}" + " setup.py build_ext")
            build_ext(*args)
        else:
            print("Python disabled")

    def install(self, spec, prefix):
        if self.spec.variants['python'].value:
            pip_args = std_pip_args + ["--prefix=" + prefix, "."]
            pip(*pip_args)
        else:
            print("Python disabled")