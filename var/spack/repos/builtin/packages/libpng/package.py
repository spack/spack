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


class Libpng(AutotoolsPackage):
    """libpng is the official PNG reference library."""

    homepage = "http://www.libpng.org/pub/png/libpng.html"
    url      = "http://download.sourceforge.net/libpng/libpng-1.6.26.tar.gz"

    version('1.6.26', '236cd975520fc1f34cc0b8f0e615f7a0')
    version('1.6.24', '65213080dd30a9b16193d9b83adc1ee9')
    # -- Security vulnerabilities have been found in 1.6.19 an older
    version('1.5.13', '9c5a584d4eb5fe40d0f1bc2090112c65') # CentOS7
    version('1.2.56', '9508fc59d10a1ffadd9aae35116c19ee') # Required for qt@3

    depends_on('zlib@1.0.4:')  # 1.2.5 or later recommended
