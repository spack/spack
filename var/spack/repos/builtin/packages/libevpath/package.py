##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Libevpath(CMakePackage):
    """EVpath is an event transport middleware layer designed to allow
    for the easy implementation of overlay networks, with
    active data processing, routing and management at all points
    in the overlay. EVPath is designed for high performance systems.
    """

    homepage = "https://github.com/GTkorvo/evpath"
    url = "https://github.com/GTkorvo/evpath/archive/v4.1.1.tar.gz"

    version('develop', git='https://github.com/GTkorvo/evpath.git',
            branch='master')
    version('4.2.1', 'f928dc0dee41668afc91634c7051ce1a')
    version('4.1.2', '1a187f55431c991ae7040e3ff041d75c')
    version('4.1.1', '65a8db820f396ff2926e3d31908d123d')

    depends_on('libffs')

    def cmake_args(self):
        args = ["-DENABLE_TESTING=0", "-DTARGET_CNL=1",
                "-DBUILD_SHARED_STATIC=STATIC"]
        return args
