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


class RAbadata(RPackage):
    """Provides the data for the gene expression enrichment analysis
    conducted in the package 'ABAEnrichment'. The package includes three
    datasets which are derived from the Allen Brain Atlas: (1) Gene
    expression data from Human Brain (adults) averaged across donors,
    (2) Gene expression data from the Developing Human Brain pooled into
    five age categories and averaged across donors and (3) a developmental
    effect score based on the Developing Human Brain expression data.
    All datasets are restricted to protein coding genes."""

    homepage = "https://bioconductor.org/packages/ABAData/"
    url      = "https://bioconductor.org/packages/release/data/experiment/src/contrib/ABAData_1.6.0.tar.gz"

    version('1.6.0', '9adfb9fbb39ad05cf72852a229476fb7')
