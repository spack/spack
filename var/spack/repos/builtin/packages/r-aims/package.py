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


class RAims(RPackage):
    """This package contains the AIMS implementation. It contains
    necessary functions to assign the five intrinsic molecular
    subtypes (Luminal A, Luminal B, Her2-enriched, Basal-like,
    Normal-like). Assignments could be done on individual samples
    as well as on dataset of gene expression data."""

    homepage = "http://bioconductor.org/packages/AIMS/"
    git      = "https://git.bioconductor.org/packages/AIMS.git"

    version('1.8.0', commit='86b866c20e191047492c51b43e3f73082c3f8357')

    depends_on('r@3.4.0:3.4.9', when='@1.8.0')
    depends_on('r-e1071', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
