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


class Brigand(Package):
    """Brigand Meta-programming library"""

    homepage = "https://github.com/edouarda/brigand"
    url      = "https://github.com/edouarda/brigand/archive/1.0.0.tar.gz"
    git      = "https://github.com/edouarda/brigand.git"

    version('master', branch='master')
    version('1.3.0', '0bea9713b3b712229aed289e218d577b')
    version('1.2.0', '32c0f73e7e666d33ff123334f5c9c92f')
    version('1.1.0', '073b7c8e2cbda3a81bbeb1ea5b9ca0eb')
    version('1.0.0', 'eeab3d437090f0bb7bc4eb69a5cd9c49')

    def install(self, spec, prefix):
        install_tree('include', prefix.include)
