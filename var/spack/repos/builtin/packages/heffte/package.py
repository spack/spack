# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from llnl.util import tty

from spack.package import *


class Heffte(CMakePackage, CudaPackage, ROCmPackage):
    """Highly Efficient FFT for Exascale"""

    homepage = "https://bitbucket.org/icl/heffte"
    url = "https://bitbucket.org/icl/heffte/get/v1.0.tar.gz"
    git = "https://bitbucket.org/icl/heffte.git"

    maintainers("mkstoyanov")
    tags = ["e4s", "ecp"]

    test_requires_compiler = True

    version("develop", branch="master")
    version("2.3.0", sha256="27c0a8da8f7bc91c8715ecb640721ab7e0454e22f6e3f521fe5acc45c28d60a9")
    version("2.2.0", sha256="aff4f5111d3d05b269a1378bb201271c40b39e9c960c05c4ef247a31a039be58")
    version("2.1.0", sha256="527a3e21115231715a0342afdfaf6a8878d2dd0f02f03c92b53692340fd940b9")
    version("2.0.0", sha256="12f2b49a1a36c416eac174cf0cc50e729d56d68a9f68886d8c34bd45a0be26b6")
    version("1.0", sha256="0902479fb5b1bad01438ca0a72efd577a3529c3d8bad0028f3c18d3a4935ca74")
    version("0.2", sha256="4e76ae60982b316c2e873b2e5735669b22620fefa1fc82f325cdb6989bec78d1")
    version("0.1", sha256="d279a03298d2dc76574b1ae1031acb4ea964348cf359273d1afa4668b5bfe748")

    patch("threads10.patch", when="@1.0")
    patch("fortran200.patch", when="@2.0.0")

    depends_on("cmake@3.10:", type=("build", "run"))
    depends_on("cmake@3.19:", when="@develop", type=("build", "run"))
    depends_on("cmake@3.21:", when="@develop+rocm", type=("build", "run"))

    variant("shared", default=True, description="Builds with shared libraries")
    variant("fftw", default=False, description="Builds with support for FFTW backend")
    variant("mkl", default=False, description="Builds with support for MKL backend")
    variant("magma", default=False, description="Use helper methods from the UTK MAGMA library")
    variant("python", default=False, description="Install the Python bindings")
    variant("fortran", default=False, description="Install the Fortran modules")

    depends_on("python@3.0:", when="+python", type=("build", "run"))
    depends_on("py-mpi4py", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-numba", when="+python+cuda", type=("build", "run"))
    extends("python", when="+python", type=("build", "run"))

    conflicts("~fftw", when="@:2.1.0~mkl~cuda")  # requires at least one backend
    conflicts("+fftw", when="+mkl@:1.0")  # old API supports at most one CPU backend
    conflicts("^openmpi~cuda", when="+cuda")  # +cuda requires CUDA enabled OpenMPI
    conflicts("~cuda~rocm", when="+magma")  # magma requires CUDA or HIP
    conflicts("+rocm", when="@:2.1.0")  # heffte+rocm is in in development in spack
    conflicts("+python", when="@:1.0")  # python support was added post v1.0
    conflicts("+fortran", when="@:1.0")  # fortran support was added post v1.0
    conflicts("+magma", when="@:1.0")  # magma support was added post v1.0

    depends_on("mpi", type=("build", "run"))

    depends_on("fftw@3.3.8:", when="+fftw", type=("build", "run"))
    depends_on("intel-mkl@2018.0.128:", when="+mkl", type=("build", "run"))
    depends_on("cuda@8.0:", when="+cuda", type=("build", "run"))
    depends_on("hip@3.8.0:", when="+rocm", type=("build", "run"))
    depends_on("rocfft@3.8.0:", when="+rocm", type=("build", "run"))
    depends_on("hip@5.2.3:", when="@develop+rocm", type=("build", "run"))
    depends_on("rocfft@5.2.3:", when="@develop+rocm", type=("build", "run"))
    depends_on("magma@2.5.3:", when="+cuda+magma", type=("build", "run"))
    depends_on("magma+rocm@2.6.1:", when="+magma+rocm @2.1:", type=("build", "run"))
    depends_on("hipblas@3.8:", when="+magma+rocm", type=("build", "run"))
    depends_on("hipsparse@3.8:", when="+magma+rocm", type=("build", "run"))

    examples_src_dir = "examples"

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("Heffte_ENABLE_CUDA", "cuda"),
            self.define_from_variant("Heffte_ENABLE_ROCM", "rocm"),
            self.define_from_variant("Heffte_ENABLE_FFTW", "fftw"),
            self.define_from_variant("Heffte_ENABLE_MKL", "mkl"),
            self.define_from_variant("Heffte_ENABLE_MAGMA", "magma"),
            self.define_from_variant("Heffte_ENABLE_FORTRAN", "fortran"),
            self.define_from_variant("Heffte_ENABLE_PYTHON", "python"),
            "-DBUILD_GPU={0:1s}".format(
                "ON" if ("+cuda" in self.spec and "+fftw" in self.spec) else "OFF"
            ),
        ]

        if "+cuda" in self.spec:
            cuda_arch = self.spec.variants["cuda_arch"].value
            if len(cuda_arch) > 0 or cuda_arch[0] != "none":
                nvcc_flags = ""
                for nvflag in self.cuda_flags(cuda_arch):
                    nvcc_flags += "{0};".format(nvflag)

                args.append("-DCUDA_NVCC_FLAGS={0}".format(nvcc_flags))

        if "+rocm" in self.spec:
            args.append("-DCMAKE_CXX_COMPILER={0}".format(self.spec["hip"].hipcc))

            rocm_arch = self.spec.variants["amdgpu_target"].value
            if "none" not in rocm_arch:
                args.append("-DCMAKE_CXX_FLAGS={0}".format(self.hip_flags(rocm_arch)))

            # See https://github.com/ROCmSoftwarePlatform/rocFFT/issues/322
            if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
                args.append(self.define("__skip_rocmclang", "ON"))

        return args

    def cmake_bin(self, set=True):
        """(Hack) Set/get cmake dependency path. Sync with Tasmanian."""
        filepath = join_path(self.install_test_root, "cmake_bin_path.txt")
        if set:
            with open(filepath, "w") as out_file:
                cmake_bin = join_path(self.spec["cmake"].prefix.bin, "cmake")
                out_file.write("{0}\n".format(cmake_bin))
        elif os.path.isfile(filepath):
            with open(filepath, "r") as in_file:
                return in_file.read().strip()

    @run_after("install")
    def setup_smoke_test(self):
        install_tree(
            self.prefix.share.heffte.testing, join_path(self.install_test_root, "testing")
        )
        self.cmake_bin(set=True)

    def test(self):
        cmake_bin = self.cmake_bin(set=False)

        if not cmake_bin:
            tty.msg("Skipping heffte test: cmake_bin_path.txt not found")
            return

        # using the tests copied from <prefix>/share/heffte/testing
        cmake_dir = self.test_suite.current_test_cache_dir.testing

        options = [cmake_dir]
        if "+rocm" in self.spec:
            options.append(
                "-Dhip_DIR=" + join_path(self.spec["hip"].prefix, "lib", "cmake", "hip")
            )
            options.append(
                "-DAMDDeviceLibs_DIR="
                + join_path(self.spec["llvm-amdgpu"].prefix, "lib", "cmake", "AMDDeviceLibs")
            )
            options.append(
                "-Damd_comgr_DIR="
                + join_path(self.spec["comgr"].prefix, "lib", "cmake", "amd_comgr")
            )
            options.append(
                "-Dhsa-runtime64_DIR="
                + join_path(self.spec["hsa-rocr-dev"].prefix, "lib", "cmake", "hsa-runtime64")
            )
            options.append(
                "-DHSA_HEADER=" + join_path(self.spec["hsa-rocr-dev"].prefix, "include")
            )
            options.append(
                "-Drocfft_DIR=" + join_path(self.spec["rocfft"].prefix, "lib", "cmake", "rocfft")
            )

        if not self.run_test(cmake_bin, options=options, purpose="Generate the Makefile"):
            tty.msg("Skipping heffte test: failed to generate Makefile")
            return

        if not self.run_test("make", purpose="Build test software"):
            tty.msg("Skipping heffte test: failed to build test")
            return

        if not self.run_test("make", options=["test"], purpose="Run test"):
            tty.msg("Failed heffte test: failed to run test")
