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


class RGdsfmt(RPackage):
    """This package provides a high-level R interface to CoreArray Genomic
       Data Structure (GDS) data files, which are portable across platforms
       with hierarchical structure to store multiple scalable array-oriented
       data sets with metadata information. It is suited for large-scale
       datasets, especially for data which are much larger than the available
       random-access memory. The gdsfmt package offers the efficient
       operations specifically designed for integers of less than 8 bits,
       since a diploid genotype, like single-nucleotide polymorphism (SNP),
       usually occupies fewer bits than a byte. Data compression and
       decompression are available with relatively efficient random access.
       It is also allowed to read a GDS file in parallel with multiple R
       processes supported by the package parallel."""

    homepage = "http://bioconductor.org/packages/gdsfmt/"
    git      = "https://git.bioconductor.org/packages/gdsfmt.git"

    version('1.14.1', commit='15743647b7eea5b82d3284858b4591fb6e59959d')

    depends_on('r@3.4.0:3.4.9', when='@1.14.1')
