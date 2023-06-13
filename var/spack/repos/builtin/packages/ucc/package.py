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
    url = "https://github.com/openucx/ucc/archive/refs/tags/v1.1.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    version("1.1.0", sha256="74c8ba75037b5bd88cb703e8c8ae55639af3fecfd4428912a433c010c97b4df7")
    version("1.0.0", sha256="d3b4aa7004bf339d35952a1699a6e408064ba578bdc93861f5f07527ad0a5e8c")

    variant("cuda", default=False, description="Enable CUDA TL")
    variant("nccl", default=False, description="Enable NCCL TL")
    variant("rccl", default=False, description="Enable RCCL TL", when="@1.1:")
    variant("ucp", default=True, description="Enable UCP TL")

    conflicts("+cuda", when="@:1.0", msg="UCC CUDA TL added in version 1.1")
    conflicts("cuda@12:", when="@1.1", msg="UCC 1.1 supports CUDA <12")
    conflicts("~cuda", when="+nccl", msg="UCC NCCL TL requires CUDA")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("cuda", when="+nccl")
    depends_on("nccl", when="+nccl")
    depends_on("rccl", when="+rccl")
    depends_on("ucx", when="+ucp")

    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")()

    def configure_args(self):
        args = []
        args.extend(self.with_or_without("cuda", activation_value="prefix"))
        args.extend(self.with_or_without("nccl", activation_value="prefix"))
        args.extend(self.with_or_without("rccl", activation_value="prefix"))
        args.extend(self.with_or_without("ucx", variant="ucp", activation_value="prefix"))
        return args
