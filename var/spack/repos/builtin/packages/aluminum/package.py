# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.platforms.cray
from spack.package import *


class Aluminum(CMakePackage, CudaPackage, ROCmPackage):
    """Aluminum provides a generic interface to high-performance
    communication libraries, with a focus on allreduce
    algorithms. Blocking and non-blocking algorithms and GPU-aware
    algorithms are supported. Aluminum also contains custom
    implementations of select algorithms to optimize for certain
    situations."""

    homepage = "https://github.com/LLNL/Aluminum"
    url = "https://github.com/LLNL/Aluminum/archive/v1.0.0.tar.gz"
    git = "https://github.com/LLNL/Aluminum.git"
    tags = ["ecp", "radiuss"]

    maintainers("bvanessen")

    version("master", branch="master")
    version("1.3.1", sha256="28ce0af6c6f29f97b7f19c5e45184bd2f8a0b1428f1e898b027d96d47cb74b0b")
    version("1.3.0", sha256="d0442efbebfdfb89eec793ae65eceb8f1ba65afa9f2e48df009f81985a4c27e3")
    version("1.2.3", sha256="9b214bdf30f9b7e8e017f83e6615db6be2631f5be3dd186205dbe3aa62f4018a")
    version(
        "1.2.2",
        sha256="c01d9dd98be4cab9b944bae99b403abe76d65e9e1750e7f23bf0105636ad5485",
        deprecated=True,
    )
    version(
        "1.2.1",
        sha256="869402708c8a102a67667b83527b4057644a32b8cdf4990bcd1a5c4e5f0e30af",
        deprecated=True,
    )
    version(
        "1.2.0",
        sha256="2f3725147f4dbc045b945af68d3d747f5dffbe2b8e928deed64136785210bc9a",
        deprecated=True,
    )
    version(
        "1.1.0",
        sha256="78b03e36e5422e8651f400feb4d8a527f87302db025d77aa37e223be6b9bdfc9",
        deprecated=True,
    )
    version("1.0.0-lbann", tag="v1.0.0-lbann")
    version("1.0.0", sha256="028d12e271817214db5c07c77b0528f88862139c3e442e1b12f58717290f414a")
    version(
        "0.7.0",
        sha256="bbb73d2847c56efbe6f99e46b41d837763938483f2e2d1982ccf8350d1148caa",
        deprecated=True,
    )
    version(
        "0.6.0",
        sha256="6ca329951f4c7ea52670e46e5020e7e7879d9b56fed5ff8c5df6e624b313e925",
        deprecated=True,
    )
    version(
        "0.5.0",
        sha256="dc365a5849eaba925355a8efb27005c5f22bcd1dca94aaed8d0d29c265c064c1",
        deprecated=True,
    )
    version(
        "0.4.0",
        sha256="4d6fab5481cc7c994b32fb23a37e9ee44041a9f91acf78f981a97cb8ef57bb7d",
        deprecated=True,
    )
    version(
        "0.3.3",
        sha256="26e7f263f53c6c6ee0fe216e981a558dfdd7ec997d0dd2a24285a609a6c68f3b",
        deprecated=True,
    )
    version(
        "0.3.2",
        sha256="09b6d1bcc02ac54ba269b1123eee7be20f0104b93596956c014b794ba96b037f",
        deprecated=True,
    )
    version(
        "0.2.1-1",
        sha256="066b750e9d1134871709a3e2414b96b166e0e24773efc7d512df2f1d96ee8eef",
        deprecated=True,
    )
    version(
        "0.2.1",
        sha256="3d5d15853cccc718f60df68205e56a2831de65be4d96e7f7e8497097e7905f89",
        deprecated=True,
    )
    version(
        "0.2",
        sha256="fc8f06c6d8faab17a2aedd408d3fe924043bf857da1094d5553f35c4d2af893b",
        deprecated=True,
    )
    version(
        "0.1",
        sha256="3880b736866e439dd94e6a61eeeb5bb2abccebbac82b82d52033bc6c94950bdb",
        deprecated=True,
    )

    variant("nccl", default=False, description="Builds with support for NCCL communication lib")
    variant(
        "ht",
        default=False,
        description="Builds with support for host-enabled MPI"
        " communication of accelerator data",
    )
    variant(
        "cuda_rma",
        default=False,
        description="Builds with support for CUDA intra-node "
        " Put/Get and IPC RMA functionality",
    )
    variant("rccl", default=False, description="Builds with support for RCCL communication lib")
    variant(
        "ofi_libfabric_plugin",
        default=spack.platforms.cray.slingshot_network(),
        when="+rccl",
        description="Builds with support for OFI libfabric enhanced RCCL/NCCL communication lib",
    )
    variant(
        "ofi_libfabric_plugin",
        default=spack.platforms.cray.slingshot_network(),
        when="+nccl",
        description="Builds with support for OFI libfabric enhanced RCCL/NCCL communication lib",
    )

    depends_on("cmake@3.21.0:", type="build", when="@1.0.1:")
    depends_on("cmake@3.17.0:", type="build", when="@:1.0.0")
    depends_on("mpi")
    depends_on("nccl@2.7.0-0:", when="+nccl")
    depends_on("hwloc@1.11:")
    depends_on("hwloc +cuda +nvml", when="+cuda")
    depends_on("hwloc@2.3.0:", when="+rocm")
    depends_on("cub", when="@:0.1,0.6.0: +cuda ^cuda@:10")
    depends_on("hipcub", when="@:0.1,0.6.0: +rocm")

    depends_on("rccl", when="+rccl")
    depends_on("aws-ofi-rccl", when="+rccl +ofi_libfabric_plugin")
    depends_on("aws-ofi-nccl", when="+nccl +ofi_libfabric_plugin")

    conflicts("~cuda", when="+cuda_rma", msg="CUDA RMA support requires CUDA")
    conflicts("+cuda", when="+rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("+nccl", when="+rccl", msg="NCCL and RCCL support are mutually exclusive")

    generator("ninja")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DCMAKE_CXX_STANDARD:STRING=17",
            "-DALUMINUM_ENABLE_CUDA:BOOL=%s" % ("+cuda" in spec),
            "-DALUMINUM_ENABLE_NCCL:BOOL=%s" % ("+nccl" in spec or "+rccl" in spec),
            "-DALUMINUM_ENABLE_ROCM:BOOL=%s" % ("+rocm" in spec),
        ]

        if not spec.satisfies("^cmake@3.23.0"):
            # There is a bug with using Ninja generator in this version
            # of CMake
            args.append("-DCMAKE_EXPORT_COMPILE_COMMANDS=ON")

        if "+cuda" in spec:
            if self.spec.satisfies("%clang"):
                for flag in self.spec.compiler_flags["cxxflags"]:
                    if "gcc-toolchain" in flag:
                        args.append("-DCMAKE_CUDA_FLAGS=-Xcompiler={0}".format(flag))
            if spec.satisfies("^cuda@11.0:"):
                args.append("-DCMAKE_CUDA_STANDARD=17")
            else:
                args.append("-DCMAKE_CUDA_STANDARD=14")
            archs = spec.variants["cuda_arch"].value
            if archs != "none":
                arch_str = ";".join(archs)
                args.append("-DCMAKE_CUDA_ARCHITECTURES=%s" % arch_str)

            if spec.satisfies("%cce") and spec.satisfies("^cuda+allow-unsupported-compilers"):
                args.append("-DCMAKE_CUDA_FLAGS=-allow-unsupported-compiler")

        if spec.satisfies("@0.5:"):
            args.extend(
                [
                    "-DALUMINUM_ENABLE_HOST_TRANSFER:BOOL=%s" % ("+ht" in spec),
                    "-DALUMINUM_ENABLE_MPI_CUDA:BOOL=%s" % ("+cuda_rma" in spec),
                    "-DALUMINUM_ENABLE_MPI_CUDA_RMA:BOOL=%s" % ("+cuda_rma" in spec),
                ]
            )
        else:
            args.append("-DALUMINUM_ENABLE_MPI_CUDA:BOOL=%s" % ("+ht" in spec))

        if spec.satisfies("@:0.1,0.6.0: +cuda ^cuda@:10"):
            args.append("-DCUB_DIR:FILEPATH=%s" % spec["cub"].prefix)

        # Add support for OS X to find OpenMP (LLVM installed via brew)
        if self.spec.satisfies("%clang platform=darwin"):
            clang = self.compiler.cc
            clang_bin = os.path.dirname(clang)
            clang_root = os.path.dirname(clang_bin)
            args.extend(["-DOpenMP_DIR={0}".format(clang_root)])

        if "+rocm" in spec:
            args.extend(
                [
                    "-DHIP_ROOT_DIR={0}".format(spec["hip"].prefix),
                    "-DHIP_CXX_COMPILER={0}".format(self.spec["hip"].hipcc),
                    "-DCMAKE_CXX_FLAGS=-std=c++17",
                ]
            )
            archs = self.spec.variants["amdgpu_target"].value
            if archs != "none":
                arch_str = ",".join(archs)
                if spec.satisfies("%rocmcc@:5"):
                    args.append(
                        "-DHIP_HIPCC_FLAGS=--amdgpu-target={0}"
                        " -g -fsized-deallocation -fPIC -std=c++17".format(arch_str)
                    )
                args.extend(
                    [
                        "-DCMAKE_HIP_ARCHITECTURES=%s" % arch_str,
                        "-DAMDGPU_TARGETS=%s" % arch_str,
                        "-DGPU_TARGETS=%s" % arch_str,
                    ]
                )

        return args
