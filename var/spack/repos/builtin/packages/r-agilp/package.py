# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAgilp(RPackage):
    """Agilent expression array processing package."""

    homepage = "http://bioconductor.org/packages/agilp/"
    git      = "https://git.bioconductor.org/packages/agilp.git"

    version('3.8.0', commit='c772a802af1b4c0741f2edd78053a0425160ea53')

    depends_on('r@3.4.0:3.4.9', when='@3.8.0')
