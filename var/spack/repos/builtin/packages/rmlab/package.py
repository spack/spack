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


class Rmlab(CMakePackage):
    """C++ File API for the reMarkable tablet"""

    homepage = "https://github.com/ax3l/lines-are-beautiful"
    git      = "https://github.com/ax3l/lines-are-beautiful.git"

    maintainers = ['ax3l']

    version('develop', branch='develop')

    variant('png', default=True,
            description='Enable PNG conversion support')

    # modern CMake
    depends_on('cmake@3.7.0:', type='build')
    # C++11
    conflicts('%gcc@:4.7')
    conflicts('%intel@:15')
    conflicts('%pgi@:14')

    depends_on('pngwriter@0.6.0:', when='+png')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DRmlab_USE_PNG={0}'.format(
                'ON' if '+png' in spec else 'OFF')
        ]
        return args
