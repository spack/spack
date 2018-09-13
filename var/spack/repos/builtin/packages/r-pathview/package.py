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


class RPathview(RPackage):
    """Pathview is a tool set for pathway based data integration and
    visualization. It maps and renders a wide variety of biological data on
    relevant pathway graphs. All users need is to supply their data and
    specify the target pathway. Pathview automatically downloads the pathway
    graph data, parses the data file, maps user data to the pathway, and
    render pathway graph with the mapped data. In addition, Pathview also
    seamlessly integrates with pathway and gene set (enrichment) analysis
    tools for large-scale and fully automated analysis."""

    homepage = "https://www.bioconductor.org/packages/pathview/"
    git      = "https://git.bioconductor.org/packages/pathview.git"

    version('1.16.7', commit='fc560ed15ef7393a73d35e714716cc24dc835339')

    depends_on('r-keggrest', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-rgraphviz', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-kegggraph', type=('build', 'run'))
    depends_on('r-org-hs-eg-db', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.16.7')
