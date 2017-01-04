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
from os import environ


class Zlib(AutotoolsPackage):
    """A free, general-purpose, legally unencumbered lossless
       data-compression library."""

    homepage = "http://zlib.net"

    url = "https://downloads.sourceforge.net/project/libpng/zlib/1.2.10/zlib-1.2.10.tar.gz"

    version('1.2.10', 'd9794246f853d15ce0fcbf79b9a3cf13', url="http://downloads.sourceforge.net/project/libpng/zlib/1.2.10/zlib-1.2.10.tar.gz")
    version('1.2.9', '44d667c142d7cda120332623eab69f40', url="https://downloads.sourceforge.net/project/libpng/zlib/1.2.8/zlib-1.2.8.tar.gz")
    version('1.2.7', '60df6a37c56e7c1366cca812414f7b85', url="https://downloads.sourceforge.net/project/libpng/zlib/1.2.7/zlib-1.2.7.tar.gz")
    version('1.2.6', '618e944d7c7cd6521551e30b32322f4a', url="https://downloads.sourceforge.net/project/libpng/zlib/1.2.6/zlib-1.2.6.tar.gz")
    version('1.2.5', 'c735eab2d659a96e5a594c9e8541ad63', url="https://downloads.sourceforge.net/project/libpng/zlib/1.2.5/zlib-1.2.5.tar.gz")
    version('1.2.4', '47f6ed51b3c83a8534f9228531effa18', url="https://downloads.sourceforge.net/project/libpng/zlib/1.2.4/zlib-1.2.4.tar.gz")
    version('1.2.3', 'debc62758716a169df9f62e6ab2bc634', url="https://downloads.sourceforge.net/project/libpng/zlib/1.2.3/zlib-1.2.3.tar.gz")
    version('1.2.2', '68bd51aaa6558c3bc3fd4890e53413de', url="https://downloads.sourceforge.net/project/libpng/zlib/1.2.2/zlib-1.2.2.tar.gz")
    version('1.2.1', 'ef1cb003448b4a53517b8f25adb12452', url="https://downloads.sourceforge.net/project/libpng/zlib/1.2.1/zlib-1.2.1.tar.gz")
    version('1.1.4', 'abc405d0bdd3ee22782d7aa20e440f08', url="https://downloads.sourceforge.net/project/libpng/zlib/1.1.4/zlib-1.1.4.tar.gz")
    version('1.1.3', 'ada18615d2a66dee4d6f5ff916ecd4c6', url="https://downloads.sourceforge.net/project/libpng/zlib/1.1.3/zlib-1.1.3.tar.gz")


    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')

    def configure(self, spec, prefix):

        if '+pic' in spec:
            environ['CFLAGS'] = self.compiler.pic_flag

        config_args = ['--prefix', prefix]
        configure(*config_args)
