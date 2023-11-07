# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import socket
import sys

from spack.package import *


class Lbann(CachedCMakePackage, CudaPackage, ROCmPackage):
    """LBANN: Livermore Big Artificial Neural Network Toolkit.  A distributed
    memory, HPC-optimized, model and data parallel training toolkit for deep
    neural networks.
    """

    homepage = "https://software.llnl.gov/lbann/"
    url = "https://github.com/LLNL/lbann/archive/v0.91.tar.gz"
    git = "https://github.com/LLNL/lbann.git"
    tags = ["ecp", "radiuss"]

    maintainers("bvanessen")

    version("develop", branch="develop")
    version("0.102", sha256="3734a76794991207e2dd2221f05f0e63a86ddafa777515d93d99d48629140f1a")
    version(
        "0.101",
        sha256="69d3fe000a88a448dc4f7e263bcb342c34a177bd9744153654528cd86335a1f7",
        deprecated=True,
    )
    version(
        "0.100",
        sha256="d1bab4fb6f1b80ae83a7286cc536a32830890f6e5b0c3107a17c2600d0796912",
        deprecated=True,
    )
    version(
        "0.99",
        sha256="3358d44f1bc894321ce07d733afdf6cb7de39c33e3852d73c9f31f530175b7cd",
        deprecated=True,
    )
    version(
        "0.98.1",
        sha256="9a2da8f41cd8bf17d1845edf9de6d60f781204ebd37bffba96d8872036c10c66",
        deprecated=True,
    )
    version(
        "0.98",
        sha256="8d64b9ac0f1d60db553efa4e657f5ea87e790afe65336117267e9c7ae6f68239",
        deprecated=True,
    )
    version(
        "0.97.1",
        sha256="2f2756126ac8bb993202cf532d72c4d4044e877f4d52de9fdf70d0babd500ce4",
        deprecated=True,
    )
    version(
        "0.97",
        sha256="9794a706fc7ac151926231efdf74564c39fbaa99edca4acb745ee7d20c32dae7",
        deprecated=True,
    )
    version(
        "0.96",
        sha256="97af78e9d3c405e963361d0db96ee5425ee0766fa52b43c75b8a5670d48e4b4a",
        deprecated=True,
    )
    version(
        "0.95",
        sha256="d310b986948b5ee2bedec36383a7fe79403721c8dc2663a280676b4e431f83c2",
        deprecated=True,
    )
    version(
        "0.94",
        sha256="567e99b488ebe6294933c98a212281bffd5220fc13a0a5cd8441f9a3761ceccf",
        deprecated=True,
    )
    version(
        "0.93",
        sha256="77bfd7fe52ee7495050f49bcdd0e353ba1730e3ad15042c678faa5eeed55fb8c",
        deprecated=True,
    )
    version(
        "0.92",
        sha256="9187c5bcbc562c2828fe619d53884ab80afb1bcd627a817edb935b80affe7b84",
        deprecated=True,
    )
    version(
        "0.91",
        sha256="b69f470829f434f266119a33695592f74802cff4b76b37022db00ab32de322f5",
        deprecated=True,
    )

    variant("al", default=True, description="Builds with support for Aluminum Library")
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
    variant(
        "conduit",
        default=True,
        description="Builds with support for Conduit Library "
        "(note that for v0.99 conduit is required)",
    )
    variant(
        "deterministic",
        default=False,
        description="Builds with support for deterministic execution",
    )
    variant(
        "dihydrogen", default=True, description="Builds with support for DiHydrogen Tensor Library"
    )
    variant(
        "distconv",
        default=False,
        description="Builds with support for spatial, filter, or channel "
        "distributed convolutions",
    )
    variant(
        "dtype",
        default="float",
        description="Type for floating point representation of weights",
        values=("float", "double"),
    )
    variant("fft", default=False, description="Support for FFT operations")
    variant("half", default=False, description="Builds with support for FP16 precision data types")
    variant("hwloc", default=True, description="Add support for topology aware algorithms")
    variant("nvprof", default=False, description="Build with region annotations for NVPROF")
    variant(
        "numpy", default=False, description="Builds with support for processing NumPy data files"
    )
    variant(
        "vision",
        default=False,
        description="Builds with support for image processing data with OpenCV",
    )
    variant("vtune", default=False, description="Builds with support for Intel VTune")
    variant("onednn", default=False, description="Support for OneDNN")
    variant("onnx", default=False, description="Support for exporting models into ONNX format")
    variant("nvshmem", default=False, description="Support for NVSHMEM")
    variant(
        "python",
        default=True,
        sticky=True,
        description="Support for Python extensions (e.g. Data Reader)",
    )
    variant(
        "pfe",
        default=True,
        sticky=True,
        description="Python Frontend for generating and launching models",
    )
    variant("boost", default=False, description="Enable callbacks that use Boost libraries")
    variant("asan", default=False, description="Build with support for address-sanitizer")
    variant("unit_tests", default=False, description="Support for unit testing")
    variant("caliper", default=False, description="Support for instrumentation with caliper")
    variant(
        "shared", default=True, sticky=True, description="Enables the build of shared libraries"
    )

    # LBANN benefits from high performance linkers, but passing these in as command
    # line options forces the linker flags to unnecessarily propagate to all
    # dependent packages. Don't include gold or lld as dependencies
    variant("gold", default=False, description="Use gold high performance linker")
    variant("lld", default=False, description="Use lld high performance linker")
    # Don't expose this a dependency until Spack can find the external properly
    # depends_on('binutils+gold', type='build', when='+gold')

    # Variant Conflicts
    conflicts("@:0.90,0.99:", when="~conduit")
    conflicts("@0.90:0.101", when="+fft")
    conflicts("@:0.90,0.102:", when="~dihydrogen")
    conflicts("~cuda", when="+nvprof")
    conflicts("~hwloc", when="+al")
    conflicts("~cuda", when="+nvshmem")
    conflicts("+cuda", when="+rocm", msg="CUDA and ROCm support are mutually exclusive")

    conflicts("~vision", when="@0.91:0.101")
    conflicts("~numpy", when="@0.91:0.101")
    conflicts("~python", when="@0.91:0.101")
    conflicts("~pfe", when="@0.91:0.101")

    requires("%clang", when="+lld")

    conflicts("+lld", when="+gold")
    conflicts("+gold", when="platform=darwin", msg="gold does not work on Darwin")
    conflicts("+lld", when="platform=darwin", msg="lld does not work on Darwin")

    depends_on("cmake@3.17.0:", type="build")
    depends_on("cmake@3.21.0:", type="build", when="@0.103:")

    # Specify the correct versions of Hydrogen
    depends_on("hydrogen@:1.3.4", when="@0.95:0.100")
    depends_on("hydrogen@1.4.0:1.4", when="@0.101:0.101.99")
    depends_on("hydrogen@1.5.0:", when="@:0.90,0.102:")

    # Add Hydrogen variants
    depends_on("hydrogen +openmp +shared +int64")
    depends_on("hydrogen +openmp_blas", when=sys.platform != "darwin")
    depends_on("hydrogen ~al", when="~al")
    depends_on("hydrogen +al", when="+al")
    depends_on("hydrogen ~cuda", when="~cuda")
    depends_on("hydrogen +cuda", when="+cuda")
    depends_on("hydrogen ~half", when="~half")
    depends_on("hydrogen +half", when="+half")
    depends_on("hydrogen ~rocm", when="~rocm")
    depends_on("hydrogen +rocm", when="+rocm")
    depends_on("hydrogen build_type=Debug", when="build_type=Debug")

    # Older versions depended on Elemental not Hydrogen
    depends_on("elemental +openmp_blas +shared +int64", when="@0.91:0.94")
    depends_on(
        "elemental +openmp_blas +shared +int64 build_type=Debug",
        when="build_type=Debug @0.91:0.94",
    )

    # Specify the correct version of Aluminum
    depends_on("aluminum@:0.3", when="@0.95:0.100 +al")
    depends_on("aluminum@0.4.0:0.4", when="@0.101:0.101.99 +al")
    depends_on("aluminum@0.5.0:", when="@:0.90,0.102: +al")

    # Add Aluminum variants
    depends_on("aluminum +cuda +nccl", when="+al +cuda")
    depends_on("aluminum +rocm +rccl", when="+al +rocm")

    depends_on("dihydrogen@0.2.0:", when="@:0.90,0.102:")
    depends_on("dihydrogen +openmp", when="+dihydrogen")
    depends_on("dihydrogen +openmp_blas", when=sys.platform != "darwin")
    depends_on("dihydrogen ~cuda", when="+dihydrogen ~cuda")
    depends_on("dihydrogen +cuda", when="+dihydrogen +cuda")
    depends_on("dihydrogen ~al", when="+dihydrogen ~al")
    depends_on("dihydrogen +al", when="+dihydrogen +al")
    depends_on("dihydrogen +distconv +cuda", when="+distconv +cuda")
    depends_on("dihydrogen +distconv +rocm", when="+distconv +rocm")
    depends_on("dihydrogen ~half", when="+dihydrogen ~half")
    depends_on("dihydrogen +half", when="+dihydrogen +half")
    depends_on("dihydrogen ~nvshmem", when="+dihydrogen ~nvshmem")
    depends_on("dihydrogen +nvshmem", when="+dihydrogen +nvshmem")
    depends_on("dihydrogen ~rocm", when="+dihydrogen ~rocm")
    depends_on("dihydrogen +rocm", when="+dihydrogen +rocm")
    depends_on("dihydrogen@0.1", when="@0.101:0.101.99 +dihydrogen")
    depends_on("dihydrogen@:0.0,0.2:", when="@:0.90,0.102: +dihydrogen")
    conflicts("~dihydrogen", when="+distconv")

    depends_on("hdf5+mpi", when="+distconv")

    for arch in CudaPackage.cuda_arch_values:
        depends_on("hydrogen cuda_arch=%s" % arch, when="+cuda cuda_arch=%s" % arch)
        depends_on("aluminum cuda_arch=%s" % arch, when="+al +cuda cuda_arch=%s" % arch)
        depends_on("dihydrogen cuda_arch=%s" % arch, when="+dihydrogen +cuda cuda_arch=%s" % arch)
        depends_on("nccl cuda_arch=%s" % arch, when="+cuda cuda_arch=%s" % arch)

    # variants +rocm and amdgpu_targets are not automatically passed to
    # dependencies, so do it manually.
    for val in ROCmPackage.amdgpu_targets:
        depends_on("hydrogen amdgpu_target=%s" % val, when="amdgpu_target=%s" % val)
        depends_on("aluminum amdgpu_target=%s" % val, when="+al amdgpu_target=%s" % val)
        depends_on("dihydrogen amdgpu_target=%s" % val, when="+dihydrogen amdgpu_target=%s" % val)

    depends_on("roctracer-dev", when="+rocm +distconv")

    depends_on("cudnn", when="@0.90:0.100 +cuda")
    depends_on("cudnn@8.0.2:", when="@:0.90,0.101: +cuda")
    depends_on("cub", when="@0.94:0.98.2 +cuda ^cuda@:10")
    depends_on("cutensor", when="@:0.90,0.102: +cuda")
    depends_on("hipcub", when="+rocm")
    depends_on("mpi")
    depends_on("hwloc@1.11:", when="@:0.90,0.102: +hwloc")
    depends_on("hwloc@1.11.0:1.11", when="@0.95:0.101 +hwloc")
    depends_on("hwloc +cuda +nvml", when="+cuda")
    depends_on("hwloc@2.3.0:", when="+rocm")
    depends_on("hiptt", when="+rocm")

    depends_on("half", when="+half")

    depends_on("fftw@3.3: +openmp", when="+fft")

    # LBANN wraps OpenCV calls in OpenMP parallel loops, build without OpenMP
    # Additionally disable video related options, they incorrectly link in a
    # bad OpenMP library when building with clang or Intel compilers
    depends_on(
        "opencv@4.1.0: build_type=RelWithDebInfo +highgui "
        "+imgcodecs +imgproc +jpeg +png +tiff +fast-math ~cuda",
        when="+vision",
    )

    # Note that for Power systems we want the environment to add +powerpc
    # When using a GCC compiler
    depends_on("opencv@4.1.0: +powerpc", when="+vision %gcc arch=ppc64le:")

    depends_on("cnpy", when="+numpy")
    depends_on("nccl", when="@0.94:0.98.2 +cuda")

    # Note that conduit defaults to +fortran +parmetis +python, none of which are
    # necessary by LBANN: you may want to disable those options in your
    # packages.yaml
    depends_on("conduit@0.4.0: +hdf5", when="@0.94:0 +conduit")
    depends_on("conduit@0.5.0:0.6 +hdf5", when="@0.100:0.101 +conduit")
    depends_on("conduit@0.6.0: +hdf5", when="@:0.90,0.99:")

    # LBANN can use Python in two modes 1) as part of an extensible framework
    # and 2) to drive the front end model creation and launch

    # Core library support for Python Data Reader and extensible interface
    depends_on("python@3: +shared", type=("run"), when="@:0.90,0.99: +python")
    extends("python", when="+python")

    # Python front end and possible extra packages
    depends_on("python@3: +shared", type=("build", "run"), when="@:0.90,0.99: +pfe")
    extends("python", when="+pfe")
    depends_on("py-setuptools", type="build", when="+pfe")
    depends_on("py-protobuf+cpp@3.10.0:", type=("build", "run"), when="@:0.90,0.99: +pfe")

    depends_on("protobuf+shared@3.10.0:", when="@:0.90,0.99:")
    depends_on("zlib-api", when="protobuf@3.11.0:")

    # using cereal@1.3.1 and above requires changing the
    # find_package call to lowercase, so stick with :1.3.0
    depends_on("cereal@:1.3.0")
    depends_on("catch2@2.9.0:2.99.999", when="+unit_tests", type=("build", "test"))
    depends_on("clara")

    depends_on("llvm-openmp", when="%apple-clang")

    depends_on("onednn cpu_runtime=omp gpu_runtime=none", when="+onednn")
    depends_on("onnx", when="+onnx")
    depends_on("nvshmem", when="+nvshmem")

    depends_on("spdlog", when="@:0.90,0.102:")
    depends_on("zstr")

    depends_on("caliper+adiak+mpi", when="+caliper")

    generator("ninja")

    def setup_build_environment(self, env):
        if self.spec.satisfies("%apple-clang"):
            env.append_flags("CPPFLAGS", self.compiler.openmp_flag)
            env.append_flags("CFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("CXXFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("LDFLAGS", self.spec["llvm-openmp"].libs.ld_flags)

    def _get_sys_type(self, spec):
        sys_type = spec.architecture
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    @property
    def libs(self):
        shared = True if "+shared" in self.spec else False
        return find_libraries("liblbann", root=self.prefix, shared=shared, recursive=True)

    @property
    def cache_name(self):
        hostname = socket.gethostname()
        # Get a hostname that has no node identifier
        hostname = hostname.rstrip("1234567890")
        return "LBANN_{0}_{1}-{2}-{3}@{4}.cmake".format(
            hostname,
            self.spec.version,
            self._get_sys_type(self.spec),
            self.spec.compiler.name,
            self.spec.compiler.version,
        )

    def initconfig_compiler_entries(self):
        spec = self.spec
        entries = super().initconfig_compiler_entries()
        entries.append(cmake_cache_string("CMAKE_CXX_STANDARD", "17"))
        entries.append(cmake_cache_option("BUILD_SHARED_LIBS", "+shared" in spec))
        if not spec.satisfies("^cmake@3.23.0"):
            # There is a bug with using Ninja generator in this version
            # of CMake
            entries.append(cmake_cache_option("CMAKE_EXPORT_COMPILE_COMMANDS", True))

        # Use lld high performance linker
        if "+lld" in spec:
            entries.append(cmake_cache_string("CMAKE_EXE_LINKER_FLAGS", "-fuse-ld=lld"))
            entries.append(cmake_cache_string("CMAKE_SHARED_LINKER_FLAGS", "-fuse-ld=lld"))

        # Use gold high performance linker
        if "+gold" in spec:
            entries.append(cmake_cache_string("CMAKE_EXE_LINKER_FLAGS", "-fuse-ld=gold"))
            entries.append(cmake_cache_string("CMAKE_SHARED_LINKER_FLAGS", "-fuse-ld=gold"))

        # Set the generator in the cached config
        if self.spec.satisfies("generator=make"):
            entries.append(cmake_cache_string("CMAKE_GENERATOR", "Unix Makefiles"))
        if self.spec.satisfies("generator=ninja"):
            entries.append(cmake_cache_string("CMAKE_GENERATOR", "Ninja"))
            entries.append(
                cmake_cache_string(
                    "CMAKE_MAKE_PROGRAM", "{0}/ninja".format(spec["ninja"].prefix.bin)
                )
            )

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        entries = super().initconfig_hardware_entries()

        if "+cuda" in spec:
            if self.spec.satisfies("%clang"):
                for flag in self.spec.compiler_flags["cxxflags"]:
                    if "gcc-toolchain" in flag:
                        entries.append(
                            cmake_cache_string("CMAKE_CUDA_FLAGS", "-Xcompiler={0}".format(flag))
                        )
            if spec.satisfies("^cuda@11.0:"):
                entries.append(cmake_cache_string("CMAKE_CUDA_STANDARD", "17"))
            else:
                entries.append(cmake_cache_string("CMAKE_CUDA_STANDARD", "14"))

            entries.append(self.define_cmake_cache_from_variant("LBANN_WITH_NVPROF", "nvprof"))

            if spec.satisfies("%cce") and spec.satisfies("^cuda+allow-unsupported-compilers"):
                entries.append(
                    cmake_cache_string("CMAKE_CUDA_FLAGS", "-allow-unsupported-compiler")
                )

        if "+rocm" in spec:
            if "platform=cray" in spec:
                entries.append(cmake_cache_option("MPI_ASSUME_NO_BUILTIN_MPI", True))

        return entries

    def initconfig_package_entries(self):
        spec = self.spec
        entries = []
        entries = [
            "#------------------{0}".format("-" * 60),
            "# LBANN",
            "#------------------{0}\n".format("-" * 60),
        ]

        cmake_variant_fields = [
            ("LBANN_WITH_CNPY", "numpy"),
            ("LBANN_DETERMINISTIC", "deterministic"),
            ("LBANN_WITH_HWLOC", "hwloc"),
            ("LBANN_WITH_ALUMINUM", "al"),
            ("LBANN_WITH_ADDRESS_SANITIZER", "asan"),
            ("LBANN_WITH_BOOST", "boost"),
            ("LBANN_WITH_CALIPER", "caliper"),
            ("LBANN_WITH_CONDUIT", "conduit"),
            ("LBANN_WITH_NVSHMEM", "nvshmem"),
            ("LBANN_WITH_FFT", "fft"),
            ("LBANN_WITH_ONEDNN", "onednn"),
            ("LBANN_WITH_ONNX", "onnx"),
            ("LBANN_WITH_EMBEDDED_PYTHON", "python"),
            ("LBANN_WITH_PYTHON_FRONTEND", "pfe"),
            ("LBANN_WITH_UNIT_TESTING", "unit_tests"),
            ("LBANN_WITH_VISION", "vision"),
            ("LBANN_WITH_VTUNE", "vtune"),
        ]

        for opt, val in cmake_variant_fields:
            entries.append(self.define_cmake_cache_from_variant(opt, val))

        entries.append(cmake_cache_option("LBANN_WITH_ROCTRACER", "+rocm +distconv" in spec))
        entries.append(cmake_cache_option("LBANN_WITH_TBINF", False))
        entries.append(
            cmake_cache_string("LBANN_DATATYPE", "{0}".format(spec.variants["dtype"].value))
        )
        entries.append(cmake_cache_option("protobuf_MODULE_COMPATIBLE", True))

        if spec.satisfies("^python") and "+pfe" in spec:
            entries.append(
                cmake_cache_path(
                    "LBANN_PFE_PYTHON_EXECUTABLE", "{0}/python3".format(spec["python"].prefix.bin)
                )
            )
            entries.append(
                cmake_cache_string("LBANN_PFE_PYTHONPATH", env["PYTHONPATH"])
            )  # do NOT need to sub ; for : because
            # value will only be interpreted by
            # a shell, which expects :

        # Add support for OpenMP with external (Brew) clang
        if spec.satisfies("%clang platform=darwin"):
            clang = self.compiler.cc
            clang_bin = os.path.dirname(clang)
            clang_root = os.path.dirname(clang_bin)
            entries.append(cmake_cache_string("OpenMP_CXX_FLAGS", "-fopenmp=libomp"))
            entries.append(cmake_cache_string("OpenMP_CXX_LIB_NAMES", "libomp"))
            entries.append(
                cmake_cache_string(
                    "OpenMP_libomp_LIBRARY", "{0}/lib/libomp.dylib".format(clang_root)
                )
            )

        entries.append(self.define_cmake_cache_from_variant("LBANN_WITH_DIHYDROGEN", "dihydrogen"))
        entries.append(self.define_cmake_cache_from_variant("LBANN_WITH_DISTCONV", "distconv"))

        # IF IBM ESSL is used it needs help finding the proper LAPACK libraries
        if self.spec.satisfies("^essl"):
            entries.append(
                cmake_cache_string(
                    "LAPACK_LIBRARIES",
                    "%s;-llapack;-lblas"
                    % ";".join("-l{0}".format(lib) for lib in self.spec["essl"].libs.names),
                )
            )
            entries.append(
                cmake_cache_string(
                    "BLAS_LIBRARIES",
                    "%s;-lblas"
                    % ";".join("-l{0}".format(lib) for lib in self.spec["essl"].libs.names),
                )
            )

        return entries
