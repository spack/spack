##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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


class Vc(CMakePackage):
    """SIMD Vector Classes for C++"""

    homepage = "https://github.com/VcDevel/Vc"
    url      = "https://github.com/VcDevel/Vc/archive/1.3.0.tar.gz"

    version('1.3.0', '77efc1c16691c7925d4b58f9b30cf03b')
    version('1.2.0', 'a5236df286b845d2fee5ef1e4d27549f')
    version('1.1.0', 'e354c1e3ea1d674b6f2af9c6fd230d81')

    variant('debug', default=False)

    def build_type(self):
        spec = self.spec
        if '+debug' in spec:
            return 'Debug'
        else:
            return 'Release'
