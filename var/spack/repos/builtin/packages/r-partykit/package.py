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


class RPartykit(RPackage):
    """A toolkit with infrastructure for representing, summarizing, and
    visualizing tree-structured regression and classification models. This
    unified infrastructure can be used for reading/coercing tree models from
    different sources ('rpart', 'RWeka', 'PMML') yielding objects that share
    functionality for print()/plot()/predict() methods. Furthermore, new and
    improved reimplementations of conditional inference trees (ctree()) and
    model-based recursive partitioning (mob()) from the 'party' package are
    provided based on the new infrastructure."""

    homepage = "http://partykit.r-forge.r-project.org/partykit"
    url      = "https://cran.r-project.org/src/contrib/partykit_1.1-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/partykit"

    version('1.1-1', '8fcb31d73ec1b8cd3bcd9789639a9277')

    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-formula', type=('build', 'run'))
