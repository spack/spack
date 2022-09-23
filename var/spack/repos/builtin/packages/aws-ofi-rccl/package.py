# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

#, ROCmPackage
class AwsOfiRccl(AutotoolsPackage):
    """AWS OFI RCCL is a plug-in which enables EC2 developers to use
    libfabric as a network provider while running AMD's RCCL based
    applications."""

    homepage = "https://github.com/ROCmSoftwarePlatform/aws-ofi-rccl"
    git = "https://github.com/ROCmSoftwarePlatform/aws-ofi-rccl.git"
    url = "https://github.com/ROCmSoftwarePlatform/aws-ofi-rccl.git"
    tags = ["rocm"]

    maintainers = ["bvanessen"]

    version("cxi", branch="cxi", default=True)
    version("master", branch="master")

    variant("enable-trace", default=False, description="Enable printing trace messages")
    variant("disable-tests", default=False, description="Disable build of tests")
    
    depends_on("libfabric")
    depends_on("hip")
    depends_on("rccl")
    depends_on("mpi")
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    def configure_args(self):
        spec = self.spec
        args = []

        args.extend(
            [
                "--with-libfabric={0}".format(spec["libfabric"].prefix),
                "--with-hip={0}".format(spec["hip"].prefix),
                "--with-rccl={0}".format(spec["rccl"].prefix),
                "--with-mpi={0}".format(spec["mpi"].prefix),
            ]
        )

        if "+enable-trace" in self.spec:
            args.append("--enable-trace")

        if "+disable-tests" in self.spec:
            args.append("--disable-tests")

        return args
