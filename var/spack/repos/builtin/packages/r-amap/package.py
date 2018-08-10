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


class RAmap(RPackage):
    """Tools for Clustering and Principal Component Analysis
       (With robust methods, and parallelized functions)."""

    homepage = "http://mulcyber.toulouse.inra.fr/projects/amap/"
    url      = "https://cran.rstudio.com/src/contrib/amap_0.8-16.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/amap/"

    version('0.8-16', sha256='d3775ad7f660581f7d2f070e426be95ae0d6743622943e6f5491988e5217d4e2')

    depends_on('r@2.10.0:', type=('build', 'run'))
