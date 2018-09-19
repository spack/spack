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


class Lcms(AutotoolsPackage):
    """Little cms is a color management library. Implements fast
       transforms between ICC profiles. It is focused on speed, and is
       portable across several platforms (MIT license)."""

    homepage = "http://www.littlecms.com"
    url      = "http://downloads.sourceforge.net/project/lcms/lcms/2.9/lcms2-2.9.tar.gz"

    version('2.9', '8de1b7724f578d2995c8fdfa35c3ad0e')
    version('2.8', '87a5913f1a52464190bb655ad230539c')
    version('2.6', 'f4c08d38ceade4a664ebff7228910a33')

    depends_on('jpeg')
    depends_on('libtiff')
    depends_on('zlib')
