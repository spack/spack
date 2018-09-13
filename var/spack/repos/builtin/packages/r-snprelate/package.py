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


class RSnprelate(RPackage):
    """Genome-wide association studies (GWAS) are widely used to investigate
       the genetic basis of diseases and traits, but they pose many
       computational challenges. We developed an R package SNPRelate to
       provide a binary format for single-nucleotide polymorphism (SNP) data
       in GWAS utilizing CoreArray Genomic Data Structure (GDS) data files.
       The GDS format offers the efficient operations specifically designed
       for integers with two bits, since a SNP could occupy only two bits.
       SNPRelate is also designed to accelerate two key computations on SNP
       data using parallel computing for multi-core symmetric multiprocessing
       computer architectures: Principal Component Analysis (PCA) and
       relatedness analysis using Identity-By-Descent measures. The SNP GDS
       format is also used by the GWASTools package with the support of S4
       classes and generic functions. The extended GDS format is implemented
       in the SeqArray package to support the storage of single nucleotide
       variations (SNVs), insertion/deletion polymorphism (indel) and
       structural variation calls."""

    homepage = "https://bioconductor.org/packages/SNPRelate"
    git      = "https://git.bioconductor.org/packages/SNPRelate.git"

    version('1.12.2', commit='dce2e2b6f36483a9f905bb5df6ae834a9f1136fe')

    depends_on('r@3.4.0:3.4.9', when='@1.12.2')
    depends_on('r-gdsfmt@1.8.3:', type=('build', 'run'))
