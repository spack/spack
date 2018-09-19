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


class GtkorvoAtl(CMakePackage):
    """Libatl provides a library for the creation and manipulation of
    lists of name/value pairs using an efficient binary representation.
    """

    homepage = "https://github.com/GTkorvo/atl"
    url      = "https://github.com/GTkorvo/atl/archive/v2.1.tar.gz"
    git      = "https://github.com/GTkorvo/atl.git"

    version('develop', branch='master')
    version('2.2', 'f0e3581e4b4c6943bf4b203685630564')
    version('2.1', 'b2324ff041bccba127330a0e1b241978')

    depends_on('gtkorvo-cercs-env')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('@2.2:'):
            args.append("-DBUILD_SHARED_LIBS=OFF")
        else:
            args.append("-DENABLE_BUILD_STATIC=STATIC")

        if self.run_tests:
            args.append('-DENABLE_TESTING=1')
        else:
            args.append('-DENABLE_TESTING=0')

        return args
