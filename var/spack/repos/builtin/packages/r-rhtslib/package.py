# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRhtslib(RPackage):
    """This package provides version 1.1 of the 'HTSlib' C library
    for high-throughput sequence analysis. The package is primarily
    useful to developers of other R packages who wish to make use
    of HTSlib. Motivation and instructions for use of this package
    are in the vignette, vignette(package="Rhtslib", "Rhtslib")."""

    homepage = "https://www.bioconductor.org/packages/Rhtslib/"
    git      = "https://git.bioconductor.org/packages/Rhtslib.git"

    version('1.8.0', commit='3b5493473bed42958614091c58c739932ffcfa79')

    depends_on('r@3.4.0:3.4.9', when='@1.8.0')
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('autoconf@2.67:', type='build')
