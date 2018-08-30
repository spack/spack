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


class Libevpath(CMakePackage):
    """EVpath is an event transport middleware layer designed to allow
    for the easy implementation of overlay networks, with
    active data processing, routing and management at all points
    in the overlay. EVPath is designed for high performance systems.
    """

    homepage = "https://github.com/GTkorvo/evpath"
    url      = "https://github.com/GTkorvo/evpath/archive/v4.1.1.tar.gz"
    git      = "https://github.com/GTkorvo/evpath.git"

    version('develop', branch='master')
    version('4.4.0', 'd8630eb358ec90ae2d188e0e6c74022a')
    version('4.2.4', '757ce010a6b7564dc62d3c79edd861d5')
    version('4.2.1', 'f928dc0dee41668afc91634c7051ce1a')
    version('4.1.2', '1a187f55431c991ae7040e3ff041d75c')
    version('4.1.1', '65a8db820f396ff2926e3d31908d123d')

    variant('enet_transport', default=False, description='Build an ENET transport for EVpath')

    depends_on('gtkorvo-enet', when='@4.4.0: +enet_transport')
    depends_on('gtkorvo-enet@1.3.13', when='@:4.2.4 +enet_transport')
    depends_on('libffs')

    def cmake_args(self):
        args = ["-DTARGET_CNL=1"]
        if self.spec.satisfies('@4.4.0:'):
            args.append("-DBUILD_SHARED_LIBS=OFF")
        else:
            args.append("-DENABLE_BUILD_STATIC=STATIC")

        if self.run_tests:
            args.append('-DENABLE_TESTING=1')
        else:
            args.append('-DENABLE_TESTING=0')

        return args
