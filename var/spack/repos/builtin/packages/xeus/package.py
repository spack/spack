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


class Xeus(CMakePackage):
    """QuantStack C++ implementation of Jupyter kernel protocol"""

    homepage = "https://xeus.readthedocs.io/en/latest/"
    url      = "https://github.com/QuantStack/xeus/archive/0.14.1.tar.gz"
    git      = "https://github.com/QuantStack/xeus.git"

    version('develop', branch='master')
    version('0.14.1', '315e0e5d919d8bf0c5a1a002169bd7e2')

    variant('examples', default=False, description="Build examples")

    conflicts('%gcc@:4.8')
    conflicts('%clang@:3.6')
    conflicts('%intel@:17')

    depends_on('zeromq@4.2.5:-libsodium')
    depends_on('cppzmq@4.3.0:')
    depends_on('cryptopp@7.0.0:')
    depends_on('xtl@0.4.0:')
    depends_on('nlohmann-json@3.2', when='@develop')
    depends_on('nlohmann-json@3.1.2', when='@0.14.1')
    depends_on('libuuid')

    def cmake_args(self):
        args = [
            '-DBUILD_EXAMPLES:BOOL=%s' % ('ON' if '+examples' in self.spec else 'OFF')
        ]

        return args
