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


class Libtiff(AutotoolsPackage):
    """LibTIFF - Tag Image File Format (TIFF) Library and Utilities."""

    homepage = "http://www.simplesystems.org/libtiff/"
    url      = "http://download.osgeo.org/libtiff/tiff-4.0.9.tar.gz"

    version('4.0.9', '54bad211279cc93eb4fca31ba9bfdc79')
    version('4.0.8', '2a7d1c1318416ddf36d5f6fa4600069b')
    version('4.0.7', '77ae928d2c6b7fb46a21c3a29325157b')
    version('4.0.6', 'd1d2e940dea0b5ad435f21f03d96dd72')
    version('4.0.3', '051c1068e6a0627f461948c365290410')
    version('3.9.7', '626102f448ba441d42e3212538ad67d2')

    depends_on('jpeg')
    depends_on('zlib')
    depends_on('xz')
