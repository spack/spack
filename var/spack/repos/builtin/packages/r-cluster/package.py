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


class RCluster(RPackage):
    """Methods for Cluster analysis. Much extended the original from Peter
    Rousseeuw, Anja Struyf and Mia Hubert, based on Kaufman and Rousseeuw
    (1990) "Finding Groups in Data"."""

    homepage = "https://cran.r-project.org/web/packages/cluster/index.html"
    url      = "https://cran.rstudio.com/src/contrib/cluster_2.0.7-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/cluster"

    version('2.0.7-1', 'a37add21b91d3e4f3883d005331e0d45')
    version('2.0.5', '7330f209ebce960bdee1a6d6679cb85a')
    version('2.0.4', 'bb4deceaafb1c42bb1278d5d0dc11e59')
