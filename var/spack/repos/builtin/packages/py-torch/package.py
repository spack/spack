# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.operating_systems.mac_os import macos_version
from spack.package import *


class PyTorch(PythonPackage, CudaPackage, ROCmPackage):
    """Tensors and Dynamic neural networks in Python
    with strong GPU acceleration."""

    homepage = "https://pytorch.org/"
    git = "https://github.com/pytorch/pytorch.git"

    maintainers("adamjstewart")

    # Exact set of modules is version- and variant-specific, just attempt to import the
    # core libraries to ensure that the package was successfully installed.
    import_modules = ["torch", "torch.autograd", "torch.nn", "torch.utils"]

    version("master", branch="master", submodules=True)
    version("2.0.1", tag="v2.0.1", submodules=True)
    version("2.0.0", tag="v2.0.0", submodules=True)
    version("1.13.1", tag="v1.13.1", submodules=True)
    version("1.13.0", tag="v1.13.0", submodules=True)
    version("1.12.1", tag="v1.12.1", submodules=True)
    version("1.12.0", tag="v1.12.0", submodules=True)
    version("1.11.0", tag="v1.11.0", submodules=True)
    version("1.10.2", tag="v1.10.2", submodules=True)
    version("1.10.1", tag="v1.10.1", submodules=True)
    version("1.10.0", tag="v1.10.0", submodules=True)
    version("1.9.1", tag="v1.9.1", submodules=True)
    version("1.9.0", tag="v1.9.0", submodules=True)
    version("1.8.2", tag="v1.8.2", submodules=True)
    version("1.8.1", tag="v1.8.1", submodules=True)
    version("1.8.0", tag="v1.8.0", submodules=True)
    version("1.7.1", tag="v1.7.1", submodules=True)
    version("1.7.0", tag="v1.7.0", submodules=True)
    version("1.6.0", tag="v1.6.0", submodules=True)
    version("1.5.1", tag="v1.5.1", submodules=True)
    version("1.5.0", tag="v1.5.0", submodules=True)
    version("1.4.1", tag="v1.4.1", submodules=True)
    version("1.3.1", tag="v1.3.1", submodules=True)
    version("1.3.0", tag="v1.3.0", submodules=True)
    version("1.2.0", tag="v1.2.0", submodules=True)
    version("1.1.0", tag="v1.1.0", submodules=True)
    version("1.0.1", tag="v1.0.1", submodules=True)
    version("1.0.0", tag="v1.0.0", submodules=True)

    is_darwin = sys.platform == "darwin"

    # All options are defined in CMakeLists.txt.
    # Some are listed in setup.py, but not all.
    variant("debug", default=False, description="Build with debugging support")
    variant("caffe2", default=False, description="Build Caffe2", when="@1.7:")
    variant("test", default=False, description="Build C++ test binaries")
    variant("cuda", default=not is_darwin, description="Use CUDA")
    variant("rocm", default=False, description="Use ROCm")
    variant("cudnn", default=not is_darwin, description="Use cuDNN", when="+cuda")
    variant("fbgemm", default=True, description="Use FBGEMM (quantized 8-bit server operators)")
    variant("kineto", default=True, description="Use Kineto profiling library", when="@1.8:")
    variant("magma", default=not is_darwin, description="Use MAGMA", when="+cuda")
    variant("metal", default=is_darwin, description="Use Metal for Caffe2 iOS build")
    variant(
        "mps",
        default=is_darwin and macos_version() >= Version("12.3"),
        description="Use MPS for macOS build (requires full Xcode suite)",
        when="@1.12: platform=darwin",
    )
    variant("nccl", default=True, description="Use NCCL", when="+cuda platform=linux")
    variant("nccl", default=True, description="Use NCCL", when="+cuda platform=cray")
    variant("nccl", default=True, description="Use NCCL", when="+rocm platform=linux")
    variant("nccl", default=True, description="Use NCCL", when="+rocm platform=cray")
    # Requires AVX2: https://discuss.pytorch.org/t/107518
    variant("nnpack", default=True, description="Use NNPACK", when="target=x86_64_v3:")
    variant("numa", default=True, description="Use NUMA", when="platform=linux")
    variant("numa", default=True, description="Use NUMA", when="platform=cray")
    variant("numpy", default=True, description="Use NumPy")
    variant("openmp", default=True, description="Use OpenMP for parallel code")
    variant("qnnpack", default=True, description="Use QNNPACK (quantized 8-bit operators)")
    variant("valgrind", default=True, description="Use Valgrind", when="@1.8: platform=linux")
    variant("valgrind", default=True, description="Use Valgrind", when="@1.8: platform=cray")
    variant("xnnpack", default=True, description="Use XNNPACK", when="@1.5:")
    variant("mkldnn", default=True, description="Use MKLDNN")
    variant("distributed", default=not is_darwin, description="Use distributed")
    variant("mpi", default=not is_darwin, description="Use MPI for Caffe2", when="+distributed")
    variant("gloo", default=not is_darwin, description="Use Gloo", when="+distributed")
    variant(
        "tensorpipe",
        default=not is_darwin,
        description="Use TensorPipe",
        when="@1.6: +distributed",
    )
    variant("onnx_ml", default=True, description="Enable traditional ONNX ML API", when="@1.5:")
    variant(
        "breakpad",
        default=True,
        description="Enable breakpad crash dump library",
        when="@1.9:1.11",
    )

    conflicts("+cuda+rocm")
    conflicts("+tensorpipe", when="+rocm ^hip@:5.1", msg="TensorPipe not supported until ROCm 5.2")
    conflicts("+breakpad", when="target=ppc64:")
    conflicts("+breakpad", when="target=ppc64le:")

    # https://github.com/pytorch/pytorch/issues/77811
    conflicts("+qnnpack", when="platform=darwin target=aarch64:")

    # https://github.com/pytorch/pytorch/issues/80805
    conflicts("+openmp", when="platform=darwin target=aarch64:")

    # https://github.com/pytorch/pytorch/issues/97397
    conflicts(
        "~tensorpipe",
        when="@1.8: +distributed",
        msg="TensorPipe must be enabled with +distributed",
    )

    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    # Required dependencies
    # See python_min_version in setup.py
    # Upper bounds come from wheel availability on PyPI
    depends_on("python@3.8:3.11", when="@2:", type=("build", "link", "run"))
    depends_on("python@3.7:3.10", when="@1.11:1", type=("build", "link", "run"))
    depends_on("python@3.6.2:3.9", when="@1.7.1:1.10", type=("build", "link", "run"))
    depends_on("python@3.6.1:3.8", when="@1.6:1.7.0", type=("build", "link", "run"))
    depends_on("python@3.5:3.8", when="@1.5", type=("build", "link", "run"))
    depends_on("python@2.7:2,3.5:3.8", when="@1.4", type=("build", "link", "run"))
    depends_on("python@2.7:2,3.5:3.7", when="@:1.3", type=("build", "link", "run"))

    # CMakelists.txt
    depends_on("cmake@3.18:", when="@2:", type="build")
    depends_on("cmake@3.13:", when="@1.11:", type="build")
    depends_on("cmake@3.10:", when="@1.10:", type="build")
    depends_on("cmake@3.5:", type="build")

    # pyproject.toml
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-astunparse", when="@1.13:", type=("build", "run"))
    depends_on("py-numpy@1.16.6:", type=("build", "run"))
    depends_on("ninja@1.5:", when="@1.1:", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-requests", when="@1.13:", type=("build", "run"))
    depends_on("py-cffi", when="@:1", type=("build", "run"))
    depends_on("py-future", when="@1.5:1", type=("build", "run"))
    depends_on("py-six", when="@1.13:1", type=("build", "run"))

    # setup.py
    depends_on("py-filelock", when="@2:", type=("build", "run"))
    depends_on("py-typing-extensions@3.6.2.1:", when="@1.7:", type=("build", "run"))
    depends_on("py-sympy", when="@2:", type=("build", "run"))
    depends_on("py-networkx", when="@2:", type=("build", "run"))
    depends_on("py-jinja2", when="@2:", type=("build", "run"))

    # Undocumented dependencies
    depends_on("py-tqdm", type="run")
    depends_on("blas")
    depends_on("lapack")

    # third_party
    depends_on("py-pybind11@2.10.1", when="@2:", type=("build", "link", "run"))
    depends_on("py-pybind11@2.10.0", when="@1.13:1", type=("build", "link", "run"))
    depends_on("py-pybind11@2.6.2", when="@1.8:1.12", type=("build", "link", "run"))
    depends_on("py-pybind11@2.3.0", when="@1.1:1.7", type=("build", "link", "run"))
    depends_on("py-pybind11@2.2.4", when="@:1.0", type=("build", "link", "run"))
    depends_on("py-protobuf@3.12.2:", when="@1.10:", type=("build", "run"))
    depends_on("py-protobuf@:3.14", when="@:1.9", type=("build", "run"))
    depends_on("protobuf@3.12.2:", when="@1.10:")
    depends_on("protobuf@:3.14", when="@:1.9")
    # https://github.com/protocolbuffers/protobuf/issues/10051
    # https://github.com/pytorch/pytorch/issues/78362
    depends_on("py-protobuf@:3", type=("build", "run"))
    depends_on("protobuf@:3", type=("build", "run"))
    depends_on("eigen")
    # https://github.com/pytorch/pytorch/issues/60329
    # depends_on("cpuinfo@2022-08-19", when="@1.13:")
    # depends_on("cpuinfo@2020-12-17", when="@1.8:1.12")
    # depends_on("cpuinfo@2020-06-11", when="@1.6:1.7")
    # https://github.com/shibatch/sleef/issues/427
    # depends_on("sleef@3.5.1_2020-12-22", when="@1.8:")
    # https://github.com/pytorch/pytorch/issues/60334
    # depends_on("sleef@3.4.0_2019-07-30", when="@1.6:1.7")
    # https://github.com/Maratyszcza/FP16/issues/18
    # depends_on("fp16@2020-05-14", when="@1.6:")
    depends_on("pthreadpool@2021-04-13", when="@1.9:")
    depends_on("pthreadpool@2020-10-05", when="@1.8")
    depends_on("pthreadpool@2020-06-15", when="@1.6:1.7")
    depends_on("psimd@2020-05-17", when="@1.6:")
    depends_on("fxdiv@2020-04-17", when="@1.6:")
    depends_on("benchmark", when="@1.6:+test")

    # Optional dependencies
    # https://github.com/pytorch/pytorch#prerequisites
    depends_on("cuda@11:", when="@2:+cuda", type=("build", "link", "run"))
    depends_on("cuda@10.2:", when="@1.11:1+cuda", type=("build", "link", "run"))
    # https://discuss.pytorch.org/t/compiling-1-10-1-from-source-with-gcc-11-and-cuda-11-5/140971
    depends_on("cuda@10.2:11.4", when="@1.10+cuda", type=("build", "link", "run"))
    depends_on("cuda@9.2:11.4", when="@1.6:1.9+cuda", type=("build", "link", "run"))
    depends_on("cuda@9:11.4", when="@1.2:1.5+cuda", type=("build", "link", "run"))
    depends_on("cuda@7.5:11.4", when="@:1.1+cuda", type=("build", "link", "run"))
    depends_on("cudnn@7:", when="@1.6:+cudnn")
    depends_on("cudnn@7", when="@1.2:1.5+cudnn")
    depends_on("cudnn@6.5:7", when="@:1.1+cudnn")
    depends_on("magma+cuda", when="+magma+cuda")
    depends_on("magma+rocm", when="+magma+rocm")
    depends_on("nccl", when="+nccl+cuda")
    depends_on("numactl", when="+numa")
    depends_on("llvm-openmp", when="%apple-clang +openmp")
    depends_on("valgrind", when="+valgrind")
    with when("+rocm"):
        depends_on("hsa-rocr-dev")
        depends_on("hip")
        depends_on("rccl", when="+nccl")
        depends_on("rocprim")
        depends_on("hipcub")
        depends_on("rocthrust")
        depends_on("roctracer-dev")
        depends_on("rocrand")
        depends_on("hipsparse")
        depends_on("hipfft")
        depends_on("rocfft")
        depends_on("rocblas")
        depends_on("miopen-hip")
        depends_on("rocminfo")
    # https://github.com/pytorch/pytorch/issues/60332
    # depends_on("xnnpack@2022-12-21", when="@2:+xnnpack")
    # depends_on("xnnpack@2022-02-16", when="@1.12:1+xnnpack")
    # depends_on("xnnpack@2021-06-21", when="@1.10:1.11+xnnpack")
    # depends_on("xnnpack@2021-02-22", when="@1.8:1.9+xnnpack")
    # depends_on("xnnpack@2020-03-23", when="@1.6:1.7+xnnpack")
    depends_on("mpi", when="+mpi")
    # https://github.com/pytorch/pytorch/issues/60270
    # depends_on("gloo@2023-01-17", when="@2:+gloo")
    # depends_on("gloo@2022-05-18", when="@1.13:1+gloo")
    # depends_on("gloo@2021-05-21", when="@1.10:1.12+gloo")
    # depends_on("gloo@2021-05-04", when="@1.9+gloo")
    # depends_on("gloo@2020-09-18", when="@1.7:1.8+gloo")
    # depends_on("gloo@2020-03-17", when="@1.6+gloo")
    # https://github.com/pytorch/pytorch/issues/60331
    # depends_on("onnx@1.13.1", when="@2:+onnx_ml")
    # depends_on("onnx@1.12.0", when="@1.13:1+onnx_ml")
    # depends_on("onnx@1.11.0", when="@1.12+onnx_ml")
    # depends_on("onnx@1.10.1_2021-10-08", when="@1.11+onnx_ml")
    # depends_on("onnx@1.10.1", when="@1.10+onnx_ml")
    # depends_on("onnx@1.8.0_2020-11-03", when="@1.8:1.9+onnx_ml")
    # depends_on("onnx@1.7.0_2020-05-31", when="@1.6:1.7+onnx_ml")
    depends_on("mkl", when="+mkldnn")

    # Test dependencies
    depends_on("py-hypothesis", type="test")
    depends_on("py-six", type="test")
    depends_on("py-psutil", type="test")

    # Fix BLAS being overridden by MKL
    # https://github.com/pytorch/pytorch/issues/60328
    patch(
        "https://github.com/pytorch/pytorch/pull/59220.patch?full_index=1",
        sha256="6d5717267f901e8ee493dfacd08734d9bcc48ad29a76ca9ef702368e96bee675",
        when="@1.2:1.11",
    )

    # Fixes build on older systems with glibc <2.12
    patch(
        "https://github.com/pytorch/pytorch/pull/55063.patch?full_index=1",
        sha256="2229bcbf20fbe88aa9f7318f89c126ec7f527875ffe689a763c78abfa127a65c",
        when="@1.1:1.8.1",
    )

    # Fixes CMake configuration error when XNNPACK is disabled
    # https://github.com/pytorch/pytorch/pull/35607
    # https://github.com/pytorch/pytorch/pull/37865
    patch("xnnpack.patch", when="@1.5")

    # Fixes build error when ROCm is enabled for pytorch-1.5 release
    patch("rocm.patch", when="@1.5+rocm")

    # Fixes fatal error: sleef.h: No such file or directory
    # https://github.com/pytorch/pytorch/pull/35359
    # https://github.com/pytorch/pytorch/issues/26555
    # patch("sleef.patch", when="@:1.5")

    # Fixes compilation with Clang 9.0.0 and Apple Clang 11.0.3
    # https://github.com/pytorch/pytorch/pull/37086
    patch(
        "https://github.com/pytorch/pytorch/commit/e921cd222a8fbeabf5a3e74e83e0d8dfb01aa8b5.patch?full_index=1",
        sha256="0f3ad037a95af9d34b1d085050c1e7771fd00f0b89e5b3a276097b7c9f4fabf8",
        when="@1.1:1.5",
    )

    # Removes duplicate definition of getCusparseErrorString
    # https://github.com/pytorch/pytorch/issues/32083
    patch("cusparseGetErrorString.patch", when="@:1.0^cuda@10.1.243:")

    # Fixes 'FindOpenMP.cmake'
    # to detect openmp settings used by Fujitsu compiler.
    patch("detect_omp_of_fujitsu_compiler.patch", when="%fj")

    # Fixes to build with fujitsu-ssl2
    patch("fj-ssl2_1.11.patch", when="@1.11:^fujitsu-ssl2")
    patch("fj-ssl2_1.10.patch", when="@1.10^fujitsu-ssl2")
    patch("fj-ssl2_1.9.patch", when="@1.9^fujitsu-ssl2")
    patch("fj-ssl2_1.8.patch", when="@1.8^fujitsu-ssl2")
    patch("fj-ssl2_1.6-1.7.patch", when="@1.6:1.7^fujitsu-ssl2")
    patch("fj-ssl2_1.3-1.5.patch", when="@1.3:1.5^fujitsu-ssl2")
    patch("fj-ssl2_1.2.patch", when="@1.2^fujitsu-ssl2")

    # Fix compilation of +distributed~tensorpipe
    # https://github.com/pytorch/pytorch/issues/68002
    patch(
        "https://github.com/pytorch/pytorch/commit/c075f0f633fa0136e68f0a455b5b74d7b500865c.patch?full_index=1",
        sha256="41271e494a3a60a65a8dd45ac053d1a6e4e4d5b42c2dac589ac67524f61ac41e",
        when="@1.10.0+distributed~tensorpipe",
    )

    # Use patches from IBM's Open CE to enable building on Power systems
    # 01xx patches are specific to open-ce, we only include 03xx patches used in meta.yaml
    # https://github.com/open-ce/pytorch-feedstock
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.7.4/pytorch-1.10/recipe/0302-cpp-extension.patch",
        sha256="ecb3973fa7d0f4c8f8ae40433f3ca5622d730a7b16f6cb63325d1e95baff8aa2",
        when="@1.10:1.11 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.7.4/pytorch-1.10/recipe/0311-PR66085-Remove-unused-dump-method-from-VSX-vec256-methods.patch",
        sha256="f05db59f3def4c4215db7142d81029c73fe330c660492159b66d65ca5001f4d1",
        when="@1.10 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.7.4/pytorch-1.10/recipe/0312-PR67331-Dummpy-VSX-bfloat16-implementation.patch",
        sha256="860b64afa85f5e6647ebc3c91d5a0bb258784770900c9302c3599c98d5cff1ee",
        when="@1.10 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.7.4/pytorch-1.10/recipe/0313-add-missing-vsx-dispatch.patch",
        sha256="7393c2bc0b6d41ecc813c829a1e517bee864686652e91f174cb7bcdfb10ba451",
        when="@1.10 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.7.4/pytorch-1.10/recipe/0314-fix-nullpointer-error.patch",
        sha256="b9cff8966f316f58514c66a403b7a6786be3cdb252f1380a6b91c722686a4097",
        when="@1.10 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.7.4/pytorch-1.12/recipe/0302-cpp-extension.patch",
        sha256="2fac519cca8997f074c263505657ff867e7ba2d6637fc8bda99c70a99be0442a",
        when="@1.12 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.8.0/pytorch-1.13/recipe/0302-cpp-extension.patch",
        sha256="a54db63640b90e5833cc1099c0935572f5297d2d8625f62f01ac1fda79ed4569",
        when="@1.13 arch=ppc64le:",
    )
    conflicts("arch=ppc64le:", when="@:1.9,2:")

    # Cherry-pick a patch to allow earlier versions of PyTorch to work with CUDA 11.4
    patch(
        "https://github.com/pytorch/pytorch/commit/c74c0c571880df886474be297c556562e95c00e0.patch?full_index=1",
        sha256="8ff7d285e52e4718bad1ca01ceb3bb6471d7828329036bb94222717fcaa237da",
        when="@:1.9.1 ^cuda@11.4.100:",
    )

    # PyTorch does not build with GCC 12 (fixed in 2.0)
    # See: https://github.com/pytorch/pytorch/issues/77614
    patch(
        "https://github.com/facebookincubator/gloo/commit/4a5e339b764261d20fc409071dc7a8b8989aa195.patch?full_index=1",
        sha256="dc8b3a9bea4693f32d6850ea2ce6ce75e1778538bfba464b50efca92bac425e3",
        when="@:1 %gcc@12:",
        working_dir="third_party/gloo",
    )

    # PyTorch does not build on Linux >=6.0.3 (fixed in master)
    # See: https://github.com/facebookincubator/gloo/issues/345
    patch(
        "https://github.com/facebookincubator/gloo/commit/10909297fedab0a680799211a299203e53515032.patch?full_index=1",
        sha256="8e6e9a44e0533ba4303a95a651b1934e5d73632cab08cc7d5a9435e1e64aa424",
        when="@:1",
        working_dir="third_party/gloo",
    )

    # Some missing includes
    # See: https://github.com/pytorch/pytorch/pull/100036
    patch(
        "https://patch-diff.githubusercontent.com/raw/pytorch/pytorch/pull/100036.patch?full_index=1",
        sha256="65060b54c31196b26dcff29bbb178fd17d5677e8481a2a06002c0ca4dd37b3d0",
        when="@2.0.0:2.0.1",
    )
    # See: https://github.com/pytorch/pytorch/pull/100049
    patch(
        "https://patch-diff.githubusercontent.com/raw/pytorch/pytorch/pull/100049.patch?full_index=1",
        sha256="673056141c0ea6ff4411f65a26f1a9d7a7c49ad8fe034a01ef0d56ba8a7a9386",
        when="@2.0.0:2.0.1",
    )

    @when("@1.5.0:")
    def patch(self):
        # https://github.com/pytorch/pytorch/issues/52208
        filter_file(
            "torch_global_deps PROPERTIES LINKER_LANGUAGE C",
            "torch_global_deps PROPERTIES LINKER_LANGUAGE CXX",
            "caffe2/CMakeLists.txt",
        )

    def setup_build_environment(self, env):
        """Set environment variables used to control the build.

        PyTorch's ``setup.py`` is a thin wrapper around ``cmake``.
        In ``tools/setup_helpers/cmake.py``, you can see that all
        environment variables that start with ``BUILD_``, ``USE_``,
        or ``CMAKE_``, plus a few more explicitly specified variable
        names, are passed directly to the ``cmake`` call. Therefore,
        most flags defined in ``CMakeLists.txt`` can be specified as
        environment variables.
        """

        def enable_or_disable(variant, keyword="USE", var=None, newer=False):
            """Set environment variable to enable or disable support for a
            particular variant.

            Parameters:
                variant (str): the variant to check
                keyword (str): the prefix to use for enabling/disabling
                var (str): CMake variable to set. Defaults to variant.upper()
                newer (bool): newer variants that never used NO_*
            """
            if var is None:
                var = variant.upper()

            # Version 1.1.0 switched from NO_* to USE_* or BUILD_*
            # But some newer variants have always used USE_* or BUILD_*
            if self.spec.satisfies("@1.1:") or newer:
                if "+" + variant in self.spec:
                    env.set(keyword + "_" + var, "ON")
                elif "~" + variant in self.spec:
                    env.set(keyword + "_" + var, "OFF")
            else:
                if "+" + variant in self.spec:
                    env.unset("NO_" + var)
                elif "~" + variant in self.spec:
                    env.set("NO_" + var, "ON")

        # Build in parallel to speed up build times
        env.set("MAX_JOBS", make_jobs)

        # Spack logs have trouble handling colored output
        env.set("COLORIZE_OUTPUT", "OFF")

        enable_or_disable("test", keyword="BUILD")
        enable_or_disable("caffe2", keyword="BUILD")

        enable_or_disable("cuda")
        if "+cuda" in self.spec:
            # cmake/public/cuda.cmake
            # cmake/Modules_CUDA_fix/upstream/FindCUDA.cmake
            env.unset("CUDA_ROOT")
            torch_cuda_arch = ";".join(
                "{0:.1f}".format(float(i) / 10.0) for i in self.spec.variants["cuda_arch"].value
            )
            env.set("TORCH_CUDA_ARCH_LIST", torch_cuda_arch)
            if self.spec.satisfies("%clang"):
                for flag in self.spec.compiler_flags["cxxflags"]:
                    if "gcc-toolchain" in flag:
                        env.set("CMAKE_CUDA_FLAGS", "=-Xcompiler={0}".format(flag))

        enable_or_disable("rocm")
        if "+rocm" in self.spec:
            env.set("PYTORCH_ROCM_ARCH", ";".join(self.spec.variants["amdgpu_target"].value))
            env.set("HSA_PATH", self.spec["hsa-rocr-dev"].prefix)
            env.set("ROCBLAS_PATH", self.spec["rocblas"].prefix)
            env.set("ROCFFT_PATH", self.spec["rocfft"].prefix)
            env.set("HIPFFT_PATH", self.spec["hipfft"].prefix)
            env.set("HIPSPARSE_PATH", self.spec["hipsparse"].prefix)
            env.set("HIP_PATH", self.spec["hip"].prefix)
            env.set("HIPRAND_PATH", self.spec["rocrand"].prefix)
            env.set("ROCRAND_PATH", self.spec["rocrand"].prefix)
            env.set("MIOPEN_PATH", self.spec["miopen-hip"].prefix)
            if "+nccl" in self.spec:
                env.set("RCCL_PATH", self.spec["rccl"].prefix)
            env.set("ROCPRIM_PATH", self.spec["rocprim"].prefix)
            env.set("HIPCUB_PATH", self.spec["hipcub"].prefix)
            env.set("ROCTHRUST_PATH", self.spec["rocthrust"].prefix)
            env.set("ROCTRACER_PATH", self.spec["roctracer-dev"].prefix)
            if self.spec.satisfies("^hip@5.2.0:"):
                env.set("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip)

        enable_or_disable("cudnn")
        if "+cudnn" in self.spec:
            # cmake/Modules_CUDA_fix/FindCUDNN.cmake
            env.set("CUDNN_INCLUDE_DIR", self.spec["cudnn"].prefix.include)
            env.set("CUDNN_LIBRARY", self.spec["cudnn"].libs[0])

        enable_or_disable("fbgemm")
        enable_or_disable("kineto")
        enable_or_disable("magma")
        enable_or_disable("metal")
        enable_or_disable("mps")
        enable_or_disable("breakpad")

        enable_or_disable("nccl")
        if "+cuda+nccl" in self.spec:
            env.set("NCCL_LIB_DIR", self.spec["nccl"].libs.directories[0])
            env.set("NCCL_INCLUDE_DIR", self.spec["nccl"].prefix.include)

        # cmake/External/nnpack.cmake
        enable_or_disable("nnpack")

        enable_or_disable("numa")
        if "+numa" in self.spec:
            # cmake/Modules/FindNuma.cmake
            env.set("NUMA_ROOT_DIR", self.spec["numactl"].prefix)

        # cmake/Modules/FindNumPy.cmake
        enable_or_disable("numpy")
        # cmake/Modules/FindOpenMP.cmake
        enable_or_disable("openmp", newer=True)
        enable_or_disable("qnnpack")
        enable_or_disable("qnnpack", var="PYTORCH_QNNPACK")
        enable_or_disable("valgrind")
        enable_or_disable("xnnpack")
        enable_or_disable("mkldnn")
        enable_or_disable("distributed")
        enable_or_disable("mpi")
        # cmake/Modules/FindGloo.cmake
        enable_or_disable("gloo", newer=True)
        enable_or_disable("tensorpipe")

        if "+debug" in self.spec:
            env.set("DEBUG", "ON")
        else:
            env.set("DEBUG", "OFF")

        if "+onnx_ml" in self.spec:
            env.set("ONNX_ML", "ON")
        elif "~onnx_ml" in self.spec:
            env.set("ONNX_ML", "OFF")

        if not self.spec.satisfies("@master"):
            env.set("PYTORCH_BUILD_VERSION", self.version)
            env.set("PYTORCH_BUILD_NUMBER", 0)

        # BLAS to be used by Caffe2
        # Options defined in cmake/Dependencies.cmake and cmake/Modules/FindBLAS.cmake
        if self.spec["blas"].name == "atlas":
            env.set("BLAS", "ATLAS")
            env.set("WITH_BLAS", "atlas")
        elif self.spec["blas"].name in ["blis", "amdblis"]:
            env.set("BLAS", "BLIS")
            env.set("WITH_BLAS", "blis")
        elif self.spec["blas"].name == "eigen":
            env.set("BLAS", "Eigen")
        elif self.spec["lapack"].name in ["libflame", "amdlibflame"]:
            env.set("BLAS", "FLAME")
            env.set("WITH_BLAS", "FLAME")
        elif self.spec["blas"].name in ["intel-mkl", "intel-parallel-studio", "intel-oneapi-mkl"]:
            env.set("BLAS", "MKL")
            env.set("WITH_BLAS", "mkl")
            # help find MKL
            if self.spec["mkl"].name == "intel-oneapi-mkl":
                env.set("INTEL_MKL_DIR", self.spec["mkl"].prefix.mkl.latest)
            else:
                env.set("INTEL_MKL_DIR", self.spec["mkl"].prefix.mkl)
        elif self.spec["blas"].name == "openblas":
            env.set("BLAS", "OpenBLAS")
            env.set("WITH_BLAS", "open")
        elif self.spec["blas"].name == "veclibfort":
            env.set("BLAS", "vecLib")
            env.set("WITH_BLAS", "veclib")
        elif self.spec["blas"].name == "fujitsu-ssl2":
            env.set("BLAS", "SSL2")
            env.set("WITH_BLAS", "ssl2")
        else:
            env.set("BLAS", "Generic")
            env.set("WITH_BLAS", "generic")

        # Don't use vendored third-party libraries when possible
        env.set("BUILD_CUSTOM_PROTOBUF", "OFF")
        env.set("USE_SYSTEM_NCCL", "ON")
        env.set("USE_SYSTEM_EIGEN_INSTALL", "ON")
        env.set("pybind11_DIR", self.spec["py-pybind11"].prefix)
        env.set("pybind11_INCLUDE_DIR", self.spec["py-pybind11"].prefix.include)
        if self.spec.satisfies("@1.10:"):
            env.set("USE_SYSTEM_PYBIND11", "ON")
        # https://github.com/pytorch/pytorch/issues/60334
        # if self.spec.satisfies("@1.8:"):
        #     env.set("USE_SYSTEM_SLEEF", "ON")
        if self.spec.satisfies("@1.6:"):
            # env.set("USE_SYSTEM_LIBS", "ON")
            # https://github.com/pytorch/pytorch/issues/60329
            # env.set("USE_SYSTEM_CPUINFO", "ON")
            # https://github.com/pytorch/pytorch/issues/60270
            # env.set("USE_SYSTEM_GLOO", "ON")
            # https://github.com/Maratyszcza/FP16/issues/18
            # env.set("USE_SYSTEM_FP16", "ON")
            env.set("USE_SYSTEM_PTHREADPOOL", "ON")
            env.set("USE_SYSTEM_PSIMD", "ON")
            env.set("USE_SYSTEM_FXDIV", "ON")
            env.set("USE_SYSTEM_BENCHMARK", "ON")
            # https://github.com/pytorch/pytorch/issues/60331
            # env.set("USE_SYSTEM_ONNX", "ON")
            # https://github.com/pytorch/pytorch/issues/60332
            # env.set("USE_SYSTEM_XNNPACK", "ON")

    @run_before("install")
    def build_amd(self):
        if "+rocm" in self.spec:
            python(os.path.join("tools", "amd_build", "build_amd.py"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("test"):
            python("run_test.py")

    @property
    def cmake_prefix_paths(self):
        cmake_prefix_paths = [
            join_path(self.prefix, self.spec["python"].package.platlib, "torch", "share", "cmake")
        ]
        return cmake_prefix_paths
