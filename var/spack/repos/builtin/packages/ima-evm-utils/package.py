# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ImaEvmUtils(AutotoolsPackage):
    """IMA/EVM control utilities."""

    homepage = "http://linux-ima.sourceforge.net"
    url      = "http://sourceforge.net/projects/linux-ima/files/ima-evm-utils/ima-evm-utils-1.2.1.tar.gz"

    version('1.3.1', sha256='5304271f31a3601a2af5984942d9bd6c7532597c5a97250c9a4524074fc39925')
    version('1.3',   sha256='62e90e8dc6b131a4f34a356114cdcb5bef844f110abbdd5d8b53c449aecc609f')
    version('1.2.1', sha256='ad8471b58c4df29abd51c80d74b1501cfe3289b60d32d1b318618a8fd26c0c0a')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
