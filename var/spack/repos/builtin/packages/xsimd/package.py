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


class Xsimd(CMakePackage):
    """C++ wrappers for SIMD intrinsics"""

    homepage = "http://quantstack.net/xsimd"
    url      = "https://github.com/QuantStack/xsimd/archive/3.1.0.tar.gz"
    git      = "https://github.com/QuantStack/xsimd.git"

    maintainers = ['ax3l']

    version('develop', branch='master')
    version('4.0.0', '4186ec94985daa3fc284d9d0d4aa03e8')
    version('3.1.0', '29c1c525116cbda28f610e2bf24a827e')

    depends_on('googletest', type='test')

    # C++14 support
    conflicts('%gcc@:4.8')
    conflicts('%clang@:3.6')
    # untested: conflicts('%intel@:15')
    # untested: conflicts('%pgi@:14')

    def cmake_args(self):
        args = [
            '-DBUILD_TESTS:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF')
        ]

        return args
