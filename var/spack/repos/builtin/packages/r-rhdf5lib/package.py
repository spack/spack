# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRhdf5lib(RPackage):
    """hdf5 library as an R package.

       Provides C and C++ hdf5 libraries."""

    homepage = "https://bioconductor.org/packages/Rhdf5lib"
    git      = "https://git.bioconductor.org/packages/Rhdf5lib.git"

    version('1.6.0', commit='6148d8554e777a2319cf6a9a213d29a69e77cba1')
    version('1.4.3', commit='f6be8c2659b2daa17541506058917b7981490d65')
    version('1.2.1', commit='dbf85dbedb736d5a696794d52875729c8514494e')
    version('1.0.0', commit='79608038c2016a518ba747fe6a2bf02ce53a75f9')

    depends_on('r@3.6.0:3.6.9', when='@1.6.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.4.3', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.2.1', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.0.0', type=('build', 'run'))
