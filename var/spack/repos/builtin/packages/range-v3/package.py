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


class RangeV3(CMakePackage):
    """Range library for C++11/14/17"""

    homepage = "https://github.com/ericniebler/range-v3"
    url      = "https://github.com/ericniebler/range-v3/archive/0.3.6.tar.gz"
    git      = "https://github.com/ericniebler/range-v3.git"

    version('develop', branch='master')
    version('0.3.6', sha256='ce6e80c6b018ca0e03df8c54a34e1fd04282ac1b068cd39e902e2e5201ac117f')
    version('0.3.5', sha256='0a0094b450fe17e1454468bef5b6bf60e73ef100aebe1663daf6fbdf2c353836')
    version('0.3.0', sha256='cc29fbed5b06b11e7f9a732f7e1211483ebbd3cfe29d86e40c93209014790d74')
    version('0.2.6', sha256='b1b448ead59bd726248bcb607b4a47335a00bed1c74630e09d550da3ff72d02c')
    version('0.2.5', sha256='4125089da83dec3f0ed676066f0cf583fe55dd9270bc62f1736907f57656ca7e')
    version('0.2.4', sha256='6fc4f9e80ee8eb22302db45c5648c665817aeeeee7f99b7effdf6a38a1be9a75')
    version('0.2.3', sha256='214a3f0ea70d479ca58f0af8938de49a9ed476564213431ab3b8e02a849b8098')
    version('0.2.2', sha256='01a7bee222570a55a79c84a54b2997ed718dac06f43a82122ff0150a11477f9d')
    version('0.2.1', sha256='25d5e3dad8052d668873e960bd78f068bebfba3bd28a278f805ea386f9438790')
    version('0.2.0', sha256='49b1a62a7a36dab582521c8034d8e736a8922af664d007c1529d3162b1294331')

    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cmake@3.6:', type='build')

    def cmake_args(self):
        args = [
            '-DRANGES_CXX_STD={0}'.format(self.spec.variants['cxxstd'].value)
        ]
        return args
