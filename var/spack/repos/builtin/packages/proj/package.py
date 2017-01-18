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


class Proj(AutotoolsPackage):
    """Cartographic Projections"""
    homepage = "https://github.com/OSGeo/proj.4/wiki"
    url      = "http://download.osgeo.org/proj/proj-4.9.2.tar.gz"

    version('4.9.2', '9843131676e31bbd903d60ae7dc76cf9')
    version('4.9.1', '3cbb2a964fd19a496f5f4265a717d31c')
    version('4.8.0', 'd815838c92a29179298c126effbb1537')
    version('4.7.0', '927d34623b52e0209ba2bfcca18fe8cd')
    version('4.6.1', '7dbaab8431ad50c25669fd3fb28dc493')
