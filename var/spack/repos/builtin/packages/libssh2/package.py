##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Libssh2(CMakePackage):
    """libssh2 is a client-side C library implementing the SSH2 protocol"""

    homepage = "https://www.libssh2.org/"
    url      = "https://www.libssh2.org/download/libssh2-1.7.0.tar.gz"

    version('1.7.0', 'b01662a210e94cccf2f76094db7dac5c')
    version('1.4.3', '071004c60c5d6f90354ad1b701013a0b') # CentOS7

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
