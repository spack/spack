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


class RKegggraph(RPackage):
    """KEGGGraph is an interface between KEGG pathway and graph object as
    well as a collection of tools to analyze, dissect and visualize these
    graphs. It parses the regularly updated KGML (KEGG XML) files into graph
    models maintaining all essential pathway attributes. The package offers
    functionalities including parsing, graph operation, visualization and
    etc."""

    homepage = "https://www.bioconductor.org/packages/KEGGgraph/"
    git      = "https://git.bioconductor.org/packages/KEGGgraph.git"

    version('1.38.1', commit='dd31665beb36d5aad8ed09ed56c603633b6b2292')

    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.38.1')
