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


class GtkorvoCercsEnv(CMakePackage):
    """A utility library used by some GTkorvo packages."""

    homepage = "https://github.com/GTkorvo/cercs_env"
    url      = "https://github.com/GTkorvo/cercs_env/archive/v1.0.tar.gz"
    git      = "https://github.com/GTkorvo/cercs_env.git"

    version('develop', branch='master')
    version('1.0', '08f0532d0c2f7bc9b53dfa7a1c40ea4d')

    def cmake_args(self):
        args = ["-DENABLE_TESTING=0", "-DENABLE_SHARED_STATIC=STATIC"]
        return args
