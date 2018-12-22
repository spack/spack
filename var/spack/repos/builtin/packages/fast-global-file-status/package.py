# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FastGlobalFileStatus(AutotoolsPackage):
    """provides a scalable mechanism to retrieve such information of a file,
       including its degree of distribution or replication and consistency."""

    homepage = "https://github.com/LLNL/FastGlobalFileStatus"
    url = 'https://github.com/LLNL/FastGlobalFileStatus/files/2271592/fastglobalfilestatus-1.1.tar.gz'

    version('1.1', 'c3d764c47a60310823947c489cd0f2df')

    depends_on('mrnet')
    depends_on('mount-point-attributes')
    depends_on('mpi')

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-mpa=%s"   % spec['mount-point-attributes'].prefix,
            "--with-mrnet=%s"       % spec['mrnet'].prefix
        ]
        return args
