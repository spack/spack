# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RInteractivedisplaybase(RPackage):
    """The interactiveDisplayBase package contains the the basic methods
       needed to generate interactive Shiny based display methods for
       Bioconductor objects."""

    homepage = "https://bioconductor.org/packages/interactiveDisplayBase/"
    git      = "https://git.bioconductor.org/packages/interactiveDisplayBase.git"

    version('1.14.0', commit='e2ccc7eefdd904e3b1032dc6b3f4a28d08c1cd40')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.14.0')
