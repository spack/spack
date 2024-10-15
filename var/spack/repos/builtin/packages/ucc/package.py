# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Ucc(AutotoolsPackage, CudaPackage, ROCmPackage):
    """UCC is a collective communication operations API and library that is
    flexible, complete, and feature-rich for current and emerging programming
    models and runtimes."""

    homepage = "https://openucx.github.io/ucc/"
    url = "https://github.com/openucx/ucc/archive/refs/tags/v1.2.0.tar.gz"

    maintainers("zzzoom")

    version("1.3.0", sha256="b56379abe5f1c125bfa83be305d78d81a64aa271b7b5fff0ac17b86725ff3acf")
    version("1.2.0", sha256="c1552797600835c0cf401b82dc89c4d27d5717f4fb805d41daca8e19f65e509d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("cuda", default=False, description="Enable CUDA TL")
    variant("nccl", default=False, description="Enable NCCL TL", when="+cuda")
    variant("rccl", default=False, description="Enable RCCL TL", when="+rocm")

    # https://github.com/openucx/ucc/pull/847
    patch(
        "https://github.com/openucx/ucc/commit/9d716eb9c964ec7a7a23e9ec663f28265ff8a357.patch?full_index=1",
        sha256="f99d1ba6b94360375d2ea59b04de9cbf6bb3290458bc86ce13891ba90522f7e2",
        when="@1.2.0 +cuda",
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("ucx")

    depends_on("nccl", when="+nccl")
    depends_on("rccl", when="+rccl")

    with when("+nccl"):
        for arch in CudaPackage.cuda_arch_values:
            depends_on(
                "nccl +cuda cuda_arch={0}".format(arch), when="+cuda cuda_arch={0}".format(arch)
            )
    # The hip path is not properly set when the ROCM_PARSE_FLAGS function is used.
    # This patch adds the option of a hip_path flag that will set it
    patch("0001-set_hip_path.patch")

    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")()

    def configure_args(self):
        args = []
        args.extend(self.with_or_without("cuda", activation_value="prefix"))
        args.extend(self.with_or_without("nccl", activation_value="prefix"))
        if self.spec.satisfies("+rocm"):
            rocm_flags = " ".join(
                [
                    "-I" + self.spec["hip"].prefix.include,
                    "-I" + self.spec["hip"].prefix.include.hip,
                    "-I" + self.spec["hsa-rocr-dev"].prefix.include.hsa,
                    "-L" + self.spec["hip"].prefix.lib,
                    "-L" + self.spec["hsa-rocr-dev"].prefix.lib,
                    "hip_path=" + self.spec["hip"].prefix,
                ]
            )
            args.append("--with-rocm=" + rocm_flags)
            args.append("--with-ucx=" + self.spec["ucx"].prefix)
        else:
            args.append("--without-rocm")
        args.extend(self.with_or_without("rccl", activation_value="prefix"))
        return args
