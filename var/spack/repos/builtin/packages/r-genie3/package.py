# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGenie3(RPackage):
    """This package implements the GENIE3 algorithm for inferring gene
    regulatory networks from expression data."""

    homepage = "https://bioconductor.org/packages/GENIE3/"
    git      = "https://git.bioconductor.org/packages/GENIE3.git"

    version('1.2.0', commit='cafe6a1a85095cda6cc3c812eb6f53501fcbaf93')

    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@1.2.0')
