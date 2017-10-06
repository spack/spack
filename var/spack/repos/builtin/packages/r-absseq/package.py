##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class RAbsseq(RPackage):
    """Inferring differential expression genes by absolute counts
    difference between two groups, utilizing Negative binomial
    distribution and moderating fold-change according to heterogeneity
    of dispersion across expression level."""

    homepage = "https://www.bioconductor.org/packages/ABSSeq/"
    url      = "https://www.bioconductor.org/packages/release/bioc/src/contrib/ABSSeq_1.22.8.tar.gz"

    version('1.22.8', 'bfdb1800f2e7c60dfa7f6b43026ec8f9')

    depends_on('r-locfit', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
