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


class RErgm(RPackage):
    """An integrated set of tools to analyze and simulate networks based
       on exponential-family random graph models (ERGM). "ergm" is a
       part of the "statnet" suite of packages for network analysis."""

    homepage = "http://statnet.org"
    url      = "https://cran.r-project.org/src/contrib/ergm_3.7.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ergm"

    version('3.7.1', '431ae430c76b2408988f469831d80126')

    depends_on('r-robustbase@0.9-10:', type=('build', 'run'))
    depends_on('r-coda@0.18-1:', type=('build', 'run'))
    depends_on('r-trust', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-lpsolve', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-statnet-common@3.3:', type=('build', 'run'))
    depends_on('r-network@1.13:', type=('build', 'run'))
