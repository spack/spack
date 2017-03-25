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


class PyTuiview(PythonPackage):
    """TuiView is a lightweight raster GIS with powerful raster attribute
    table manipulation abilities.
    """

    homepage = "https://bitbucket.org/chchrsc/tuiview"
    url      = "https://bitbucket.org/chchrsc/tuiview/get/tuiview-1.1.7.tar.gz"

    version('1.1.7', '4b3b38a820cc239c8ab4a181ac5d4c30')

    depends_on("py-pyqt", type=('build', 'run'))
    depends_on("py-numpy", type=('build', 'run'))
    depends_on("gdal")
