##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class Libffs(CMakePackage):
    """FFS is a middleware library for data communication,
    including representation, processing and marshaling
    that preserves the performance of traditional approaches
    while relaxing the requirement of a priori knowledge
    and providing complex run-time flexibility.
    """

    homepage = "http://www.cc.gatech.edu/systems/projects/FFS"
    url      = "https://github.com/GTkorvo/ffs/archive/v1.1.tar.gz"
    git      = "https://github.com/GTkorvo/ffs.git"

    version('develop', branch='master')
    version('1.5',   'c41c5f5f448b627740deecd695b7bbf8')
    version('1.1.1', 'aa1c8ad5cf35e8cf76735e3a60891509')
    version('1.1',   '561c6b3abc53e12b3c01192e8ef2ffbc')

    depends_on('flex', type='build', when='@:1.4')
    depends_on('bison', type='build', when='@:1.4')
    depends_on('gtkorvo-cercs-env', type='build', when='@:1.4')
    depends_on('gtkorvo-atl')
    depends_on('gtkorvo-dill')

    def cmake_args(self):
        args = ["-DTARGET_CNL=1"]
        if self.spec.satisfies('@1.5:'):
            args.append("-DBUILD_SHARED_LIBS=OFF")
        else:
            args.append("-DENABLE_BUILD_STATIC=STATIC")

        if self.run_tests:
            args.append('-DENABLE_TESTING=0')
        else:
            args.append('-DENABLE_TESTING=0')

        return args
