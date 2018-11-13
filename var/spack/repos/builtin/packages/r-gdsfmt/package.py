# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
