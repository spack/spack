# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libssh2(CMakePackage):
    """libssh2 is a client-side C library implementing the SSH2 protocol"""

    homepage = "https://www.libssh2.org/"
    url      = "https://www.libssh2.org/download/libssh2-1.7.0.tar.gz"

    version('1.8.0', '3d1147cae66e2959ea5441b183de1b1c')
    version('1.7.0', 'b01662a210e94cccf2f76094db7dac5c')
    version('1.4.3', '071004c60c5d6f90354ad1b701013a0b')  # CentOS7

    variant('shared', default=True,
            description="Build shared libraries")

    depends_on('cmake@2.8.11:', type='build')
    depends_on('openssl')
    depends_on('zlib')
    depends_on('xz')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DBUILD_SHARED_LIBS=%s' % ('YES' if '+shared' in spec else 'NO')]
