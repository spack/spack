# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cosbench(Package):
    """
    COSBench is a benchmarking tool to measure the performance of
    Cloud Object Storage services. Object storage is an emerging
    technology that is different from traditional file systems
    (e.g., NFS) or block device systems (e.g., iSCSI). Amazon S3
    and Openstack* swift are well-known object storage solutions
    """

    homepage = "https://github.com/intel-cloud/cosbench"
    url      = "https://github.com/intel-cloud/cosbench/releases/download/v0.4.2.c4/0.4.2.c4.zip"

    version('0.4.2.c4', sha256='abe837ffce3d6f094816103573433f5358c0b27ce56f414a60dceef985750397')
    version('0.4.2.c2', sha256='b9cd93721af6b5d5b6b04644edb2ad130c7adf887478ecee9dbfb3065a7bc1dc')
    version('0.4.2',    sha256='9e82518d4fac3c23cfac47c8a571d4a61bf8e5f11286606c79a0f923e983dc61')
    version('0.4.1.0',  sha256='a044cd232b3cc376802aa6a4a697988ec690a8b1d70040641710066acd322c5a')
    version('0.4.0.1',  sha256='384e4de218a9a61040f45cf9aa0a555e88ff25fb2b5cd11c540627cd604b4961')

    def install(self, spec, prefix):
        copy_tree('.', prefix)
