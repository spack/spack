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


class Xtensor(CMakePackage):
    """Multi-dimensional arrays with broadcasting and lazy computing"""

    homepage = "http://quantstack.net/xtensor"
    url      = "https://github.com/QuantStack/xtensor/archive/0.13.1.tar.gz"
    git      = "https://github.com/QuantStack/xtensor.git"

    maintainers = ['ax3l']

    version('develop', branch='master')
    version('0.15.1', 'c24ecc406003bd1ac22291f1f7cac29a')
    version('0.13.1', '80e7e33f05066d17552bf0f8b582dcc5')

    variant('xsimd', default=True,
            description='Enable SIMD intrinsics')

    depends_on('xtl')
    depends_on('xtl@0.4.0:0.4.99', when='@0.15.1:')
    depends_on('xtl@0.3.3:0.3.99', when='@0.13.1')
    depends_on('xsimd@4.0.0', when='@0.15.1 +xsimd')
    depends_on('xsimd@3.1.0', when='@0.13.1 +xsimd')

    # C++14 support
    conflicts('%gcc@:4.8')
    conflicts('%clang@:3.5')
    # untested: conflicts('%intel@:15')
    # untested: conflicts('%pgi@:14')
