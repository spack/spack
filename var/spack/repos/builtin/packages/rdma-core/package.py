# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RdmaCore(CMakePackage):
    """RDMA core userspace libraries and daemons"""

    homepage = "https://github.com/linux-rdma/rdma-core"
    url      = "https://github.com/linux-rdma/rdma-core/releases/download/v17.1/rdma-core-17.1.tar.gz"

    version('20', sha256='bc846989f807cd2b03643927d2b99fbf6f849cb1e766ab49bc9e81ce769d5421')
    version('17.1', sha256='b47444b7c05d3906deb8771eec3e634984dd83f5e620d5e37d3a83f74f0cc1ba')
    version('13', sha256='e5230fd7cda610753ad1252b40a28b1e9cf836423a10d8c2525b081527760d97')

    depends_on('pkgconfig', type='build')
    depends_on('libnl')
    conflicts('platform=darwin', msg='rdma-core requires FreeBSD or Linux')
    conflicts('%intel', msg='rdma-core cannot be built with intel (use gcc instead)')

# NOTE: specify CMAKE_INSTALL_RUNDIR explicitly to prevent rdma-core from
#       using the spack staging build dir (which may be a very long file
#       system path) as a component in compile-time static strings such as
#       IBACM_SERVER_PATH.
    def cmake_args(self):
        cmake_args = ["-DCMAKE_INSTALL_SYSCONFDIR=" +
                      self.spec.prefix.etc,
                      "-DCMAKE_INSTALL_RUNDIR=/var/run"]
        return cmake_args
