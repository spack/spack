# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffypdnn(RPackage):
    """The package contains functions to perform the PDNN method
    described by Li Zhang et al."""

    homepage = "https://www.bioconductor.org/packages/affypdnn/"
    git      = "https://git.bioconductor.org/packages/affypdnn.git"

    version('1.50.0', commit='97ff68e9f51f31333c0330435ea23b212b3ed18a')

    depends_on('r@3.4.0:3.4.9', when='@1.50.0')
    depends_on('r-affy', type=('build', 'run'))
