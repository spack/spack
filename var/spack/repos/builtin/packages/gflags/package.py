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


class Gflags(CMakePackage):
    """The gflags package contains a C++ library that implements
    commandline flags processing. It includes built-in support for
    standard types such as string and the ability to define flags
    in the source file in which they are used. Online documentation
    available at: https://gflags.github.io/gflags/"""

    homepage = "https://gflags.github.io/gflags"
    url      = "https://github.com/gflags/gflags/archive/v2.1.2.tar.gz"

    version('2.1.2', 'ac432de923f9de1e9780b5254884599f')

    depends_on('cmake@2.8.12:', type='build')

    def cmake_args(self):
        return ['-DBUILD_SHARED_LIBS=ON']
