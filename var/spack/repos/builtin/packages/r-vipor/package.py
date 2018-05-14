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


class RVipor(RPackage):
    """Plot Categorical Data Using Quasirandom Noise and Density Estimates"""

    homepage = "https://cran.r-project.org/package=vipor"
    url      = "https://cran.r-project.org/src/contrib/vipor_0.4.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/vipor"

    version('0.4.5', 'd08bc95b3aaf1574bf41b7eb41b67ce4')
    version('0.4.4', '834212e3971787809ba9737744d54dee')

    depends_on('r@3.0.0:', type=('build', 'run'))
