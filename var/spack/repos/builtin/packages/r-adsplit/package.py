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


class RAdsplit(RPackage):
    """This package implements clustering of microarray gene expression
    profiles according to functional annotations. For each term genes
    are annotated to, splits into two subclasses are computed and a
    significance of the supporting gene set is determined."""

    homepage = "https://www.bioconductor.org/packages/adSplit/"
    git      = "https://git.bioconductor.org/packages/adSplit.git"

    version('1.46.0', commit='7e81a83f34d371447f491b3a146bf6851e260c7c')

    depends_on('r@3.4.0:3.4.9', when='@1.46.0')
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-kegg-db', type=('build', 'run'))
    depends_on('r-multtest', type=('build', 'run'))
