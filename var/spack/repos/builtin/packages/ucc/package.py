# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Ucc(AutotoolsPackage, CudaPackage):
    """UCC is a collective communication operations API and library that is
    flexible, complete, and feature-rich for current and emerging programming
    models and runtimes."""

    homepage = "https://openucx.github.io/ucc/"
    url = "https://github.com/openucx/ucc/archive/refs/tags/v1.2.0.tar.gz"

    maintainers("zzzoom")

    version("1.2.0", sha256="c1552797600835c0cf401b82dc89c4d27d5717f4fb805d41daca8e19f65e509d")

    variant("cuda", default=False, description="Enable CUDA TL", when="@1.1:")
    variant("nccl", default=False, description="Enable NCCL TL")
    # RCCL build not tested
    # variant("rccl", default=False, description="Enable RCCL TL")

    conflicts("cuda@12:", when="@1.1", msg="UCC 1.1 supports CUDA <12")
    conflicts("~cuda", when="+nccl", msg="UCC NCCL TL requires CUDA")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("cuda", when="+nccl")
    depends_on("ucx")

    depends_on("nccl", when="+nccl")
    # depends_on("rccl", when="+rccl")

    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")()

    def configure_args(self):
        args = []
        args.extend(self.with_or_without("cuda", activation_value="prefix"))
        args.extend(self.with_or_without("nccl", activation_value="prefix"))
        # args.extend(self.with_or_without("rccl", activation_value="prefix"))
        return args
