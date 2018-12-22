# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAnnotationfilter(RPackage):
    """This package provides class and other infrastructure to implement
       filters for manipulating Bioconductor annotation resources. The
       filters will be used by ensembldb, Organism.dplyr, and other
       packages."""

    homepage = "https://bioconductor.org/packages/AnnotationFilter/"
    git      = "https://git.bioconductor.org/packages/AnnotationFilter.git"

    version('1.0.0', commit='a9f79b26defe3021eea60abe16ce1fa379813ec9')

    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.0.0')
