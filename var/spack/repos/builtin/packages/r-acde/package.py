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


class RAcde(RPackage):
    """This package provides a multivariate inferential analysis method
    for detecting differentially expressed genes in gene expression data.
    It uses artificial components, close to the data's principal
    components but with an exact interpretation in terms of differential
    genetic expression, to identify differentially expressed genes while
    controlling the false discovery rate (FDR). The methods on this
    package are described in the vignette or in the article
    'Multivariate Method for Inferential Identification of
    Differentially Expressed Genes in Gene Expression Experiments' by
    J. P. Acosta, L. Lopez-Kleine and S. Restrepo
    (2015, pending publication)."""

    homepage = "https://www.bioconductor.org/packages/acde/"
    url      = "https://www.bioconductor.org/packages/release/bioc/src/contrib/acde_1.6.0.tar.gz"

    version('1.6.0', 'e92ce91f75bab3bb1d79995bec1b42cc')

    depends_on('r-boot', type=('build', 'run'))
