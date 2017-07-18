##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class RDiagrammer(RPackage):
    """Create graph diagrams and flowcharts using R."""

    homepage = "https://github.com/rich-iannone/DiagrammeR"
    url      = "https://cran.r-project.org/src/contrib/DiagrammeR_0.9.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/DiagrammeR"

    version('0.9.0', '111c20b06f4df3223a98b575c3917143')
    version('0.8.4', '9ee295c744f5d4ba9a84289ca7bdaf1a')

    depends_on('r-dplyr@0.5.0:', type=('build', 'run'), when=('@0.9.0:'))
    depends_on('r-htmlwidgets@0.8:', type=('build', 'run'))
    depends_on('r-igraph@1.0.1:', type=('build', 'run'))
    depends_on('r-influencer@0.1.0:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', type=('build', 'run'), when=('@0.9.0:'))
    depends_on('r-rcolorbrewer@1.1-2:', type=('build', 'run'), when=('@0.9.0:'))
    depends_on('r-rstudioapi@0.6:', type=('build', 'run'))
    depends_on('r-rgexf@0.15.3:', type=('build', 'run'), when=('@0.9.0:'))
    depends_on('r-scales@0.4.1:', type=('build', 'run'))
    depends_on('r-stringr@1.1.0:', type=('build', 'run'))
    depends_on('r-tibble@1.2:', type=('build', 'run'), when=('@0.9.0:'))
    depends_on('r-viridis@0.3.4:', type=('build', 'run'), when=('@0.9.0:'))
    depends_on('r-visnetwork@1.0.2:', type=('build', 'run'))
