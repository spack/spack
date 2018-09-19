##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Mbedtls(CMakePackage):
    """mbed TLS (formerly known as PolarSSL) makes it trivially easy for
       developers to include cryptographic and SSL/TLS capabilities in
       their (embedded) products, facilitating this functionality with a
       minimal coding footprint.

    """
    homepage = "https://tls.mbed.org"
    url      = "https://github.com/ARMmbed/mbedtls/archive/mbedtls-2.2.1.tar.gz"

    version('2.3.0', '98158e1160a0825a3e8db38881a177a0')
    version('2.2.1', '73a38f96898d6d03e32f55dd9f9a67be')
    version('2.2.0', 'eaf4586c1ef93ae872e606b6c1203942')
    version('2.1.4', '40cdf67b6c6d92c9cbcfd552d39ea3ae')
    version('2.1.3', '7eb4cf1dfa68578a2c8dbd0b6fa752dd')
    version('1.3.16', '4144d7320c691f721aeb9e67a1bc38e0')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release', 'Coverage', 'ASan', 'ASanDbg',
                    'MemSan', 'MemSanDbg', 'Check', 'CheckFull'))

    depends_on('cmake@2.6:', type='build')
