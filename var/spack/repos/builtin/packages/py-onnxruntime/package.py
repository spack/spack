# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOnnxruntime(CMakePackage, PythonExtension):
    """ONNX Runtime is a performance-focused complete scoring
    engine for Open Neural Network Exchange (ONNX) models, with
    an open extensible architecture to continually address the
    latest developments in AI and Deep Learning. ONNX Runtime
    stays up to date with the ONNX standard with complete
    implementation of all ONNX operators, and supports all
    ONNX releases (1.2+) with both future and backwards
    compatibility."""

    homepage = "https://github.com/microsoft/onnxruntime"
    git = "https://github.com/microsoft/onnxruntime.git"

    version("1.10.0", tag="v1.10.0", submodules=True)
    version("1.7.2", tag="v1.7.2", submodules=True)

    variant("cuda", default=False, description="Build with CUDA support")

    depends_on("cmake@3.1:", type="build")
    depends_on("ninja", type="build")
    depends_on("python", type=("build", "run"))
    depends_on("py-pip", type="build")
    depends_on("protobuf")
    # https://github.com/microsoft/onnxruntime/pull/11639
    depends_on("protobuf@:3.19", when="@:1.11")
    depends_on("py-protobuf", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.16.6:", type=("build", "run"))
    depends_on("py-sympy@1.1:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-cerberus", type=("build", "run"))
    depends_on("py-wheel", type="build")
    depends_on("py-onnx", type=("build", "run"))
    depends_on("py-flatbuffers", type=("build", "run"))
    depends_on("zlib")
    depends_on("libpng")
    depends_on("py-pybind11", type="build")
    depends_on("cuda", when="+cuda")
    depends_on("cudnn", when="+cuda")
    depends_on("iconv", type=("build", "link", "run"))
    depends_on("re2+shared")

    extends("python")
    # Adopted from CMS experiment's fork of onnxruntime
    # https://github.com/cms-externals/onnxruntime/compare/5bc92df...d594f80
    patch("cms.patch", level=1, when="@1.7.2")
    # https://github.com/cms-externals/onnxruntime/compare/0d9030e...7a6355a
    patch("cms_1_10.patch", whe="@1.10")
    # https://github.com/microsoft/onnxruntime/issues/4234#issuecomment-698077636
    # only needed when iconv is provided by libiconv
    patch("libiconv.patch", level=0, when="@1.7.2 ^libiconv")
    patch("libiconv-1.10.patch", level=0, when="@1.10.0 ^libiconv")
    # https://github.com/microsoft/onnxruntime/commit/de4089f8cbe0baffe56a363cc3a41595cc8f0809.patch
    patch("gcc11.patch", level=1, when="@1.7.2")

    dynamic_cpu_arch_values = ("NOAVX", "AVX", "AVX2", "AVX512")

    variant(
        "dynamic_cpu_arch",
        default="AVX512",
        values=dynamic_cpu_arch_values,
        multi=False,
        description="AVX support level",
    )

    generator = "Ninja"
    root_cmakelists_dir = "cmake"
    build_directory = "."

    def setup_build_environment(self, env):
        value = self.spec.variants["dynamic_cpu_arch"].value
        value = self.dynamic_cpu_arch_values.index(value)
        env.set("MLAS_DYNAMIC_CPU_ARCH", str(value))

    def setup_run_environment(self, env):
        value = self.spec.variants["dynamic_cpu_arch"].value
        value = self.dynamic_cpu_arch_values.index(value)
        env.set("MLAS_DYNAMIC_CPU_ARCH", str(value))

    def cmake_args(self):
        define = self.define
        define_from_variant = self.define_from_variant

        args = [
            define("onnxruntime_ENABLE_PYTHON", True),
            define("onnxruntime_BUILD_SHARED_LIB", True),
            define_from_variant("onnxruntime_USE_CUDA", "cuda"),
            define("onnxruntime_BUILD_CSHARP", False),
            define("onnxruntime_USE_EIGEN_FOR_BLAS", True),
            define("onnxruntime_USE_OPENBLAS", False),
            define("onnxruntime_USE_MKLML", False),
            define("onnxruntime_USE_NGRAPH", False),
            define("onnxruntime_USE_OPENMP", False),
            define("onnxruntime_USE_TVM", False),
            define("onnxruntime_USE_LLVM", False),
            define("onnxruntime_ENABLE_MICROSOFT_INTERNAL", False),
            define("onnxruntime_USE_BRAINSLICE", False),
            define("onnxruntime_USE_NUPHAR", False),
            define("onnxruntime_USE_TENSORRT", False),
            define("onnxruntime_CROSS_COMPILING", False),
            define("onnxruntime_USE_FULL_PROTOBUF", True),
            define("onnxruntime_DISABLE_CONTRIB_OPS", False),
            define("onnxruntime_USE_PREINSTALLED_PROTOBUF", True),
            define("onnxruntime_PREFER_SYSTEM_LIB", True),
        ]

        if self.spec.satisfies("+cuda"):
            args.extend(
                (
                    define("onnxruntime_CUDA_VERSION", str(self.spec["cuda"].version)),
                    define("onnxruntime_CUDA_HOME", self.spec["cuda"].prefix),
                    define("onnxruntime_CUDNN_HOME", self.spec["cudnn"].prefix),
                    define("CMAKE_CUDA_FLAGS", "-cudart shared"),
                    define("CMAKE_CUDA_RUNTIME_LIBRARY", "Shared"),
                    define("DCMAKE_TRY_COMPILE_PLATFORM_VARIABLES", "CMAKE_CUDA_RUNTIME_LIBRARY"),
                )
            )

        return args

    @run_after("install")
    def install_python(self):
        """Install everything from build directory."""
        args = std_pip_args + ["--prefix=" + prefix, "."]
        with working_dir(self.build_directory):
            pip(*args)
