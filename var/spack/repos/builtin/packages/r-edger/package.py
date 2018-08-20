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


class REdger(RPackage):
    """Differential expression analysis of RNA-seq expression profiles with
       biological replication. Implements a range of statistical methodology
       based on the negative binomial distributions, including empirical Bayes
       estimation, exact tests, generalized linear models and quasi-likelihood
       tests. As well as RNA-seq, it be applied to differential signal analysis
       of other types of genomic data that produce counts, including ChIP-seq,
       SAGE and CAGE."""

    homepage = "https://bioconductor.org/packages/edgeR/"
    git      = "https://git.bioconductor.org/packages/edgeR.git"

    version('3.22.3', commit='e82e54afc9398ac54dc4caba0f7ae5c43e572203')
    version('3.18.1', commit='101106f3fdd9e2c45d4a670c88f64c12e97a0495')

    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-locfit', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@3.22.3')
    depends_on('r@3.4.0:3.4.9', when='@3.18.1')
