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

class Libpng(Package):
    """libpng graphics file format"""
    homepage = "http://www.libpng.org/pub/png/libpng.html"
    url      = "http://download.sourceforge.net/libpng/libpng-1.6.16.tar.gz"

    version('1.6.16', '1a4ad377919ab15b54f6cb6a3ae2622d')
    version('1.6.15', '829a256f3de9307731d4f52dc071916d')
    version('1.6.14', '2101b3de1d5f348925990f9aa8405660')
    version('1.5.26', '3ca98347a5541a2dad55cd6d07ee60a9')
    version('1.4.19', '89bcbc4fc8b31f4a403906cf4f662330')
    version('1.2.56', '9508fc59d10a1ffadd9aae35116c19ee')

    depends_on('zlib')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
