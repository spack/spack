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


class Uberftp(AutotoolsPackage):
    """UberFTP is an interactive (text-based) client for GridFTP"""

    homepage = "http://toolkit.globus.org/grid_software/data/uberftp.php"
    url      = "https://github.com/JasonAlt/UberFTP/archive/Version_2_8.tar.gz"

    version('2_8', 'bc7a159955a9c4b9f5f42f3d2b8fc830')
    version('2_7', 'faaea2d6e1958c1105cfc9147824e03c')
    version('2_6', '784210976f259f9d19c0798c19778d34')

    depends_on('globus-toolkit')
