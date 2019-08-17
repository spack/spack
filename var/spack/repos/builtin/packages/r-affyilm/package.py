# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffyilm(RPackage):
    """affyILM is a preprocessing tool which estimates gene
    expression levels for Affymetrix Gene Chips. Input from
    physical chemistry is employed to first background subtract
    intensities before calculating concentrations on behalf
    of the Langmuir model."""

    homepage = "https://www.bioconductor.org/packages/affyILM/"
    git      = "https://git.bioconductor.org/packages/affyILM.git"

    version('1.28.0', commit='307bee3ebc599e0ea4a1d6fa8d5511ccf8bef7de')

    depends_on('r@3.4.0:3.4.9', when='@1.28.0')
    depends_on('r-gcrma', type=('build', 'run'))
    depends_on('r-affxparser', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
