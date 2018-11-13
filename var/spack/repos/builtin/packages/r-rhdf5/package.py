# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRhdf5(RPackage):
    """This R/Bioconductor package provides an interface between HDF5
    and R. HDF5's main features are the ability to store and access very
    large and/or complex datasets and a wide variety of metadata on mass
    storage (disk) through a completely portable file format. The rhdf5
    package is thus suited for the exchange of large and/or complex
    datasets between R and other software package, and for letting R
    applications work on datasets that are larger than the available RAM."""

    homepage = "https://www.bioconductor.org/packages/rhdf5/"
    git      = "https://git.bioconductor.org/packages/rhdf5.git"

    version('2.20.0', commit='37b5165325062728bbec9167f89f5f4b794f30bc')

    depends_on('r@3.4.0:3.4.9', when='@2.20.0')
    depends_on('r-zlibbioc', type=('build', 'run'))
