# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAnnotationforge(RPackage):
    """Provides code for generating Annotation packages and
    their databases. Packages produced are intended to be used
    with AnnotationDbi."""

    homepage = "https://www.bioconductor.org/packages/AnnotationForge/"
    git      = "https://git.bioconductor.org/packages/AnnotationForge.git"

    version('1.18.2', commit='44ca3d4ef9e9825c14725ffdbbaa57ea059532e1')

    depends_on('r@3.4.0:3.4.9', when='@1.18.2')
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
