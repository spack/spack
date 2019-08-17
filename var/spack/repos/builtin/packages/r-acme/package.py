# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAcme(RPackage):
    """ACME (Algorithms for Calculating Microarray Enrichment) is a set
    of tools for analysing tiling array ChIP/chip, DNAse hypersensitivity,
    or other experiments that result in regions of the genome showing
    "enrichment". It does not rely on a specific array technology
    (although the array should be a "tiling" array), is very general
    (can be applied in experiments resulting in regions of enrichment),
    and is very insensitive to array noise or normalization methods.
    It is also very fast and can be applied on whole-genome tiling array
    experiments quite easily with enough memory."""

    homepage = "https://www.bioconductor.org/packages/ACME/"
    git      = "https://git.bioconductor.org/packages/ACME.git"

    version('2.32.0', commit='76372255d7714a0c8128a11c028bf70214dac407')

    depends_on('r@3.4.0:3.4.9', when='@2.32.0')
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
