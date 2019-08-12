# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RProtgenerics(RPackage):
    """S4 generic functions needed by Bioconductor proteomics packages."""

    homepage = "https://bioconductor.org/packages/ProtGenerics/"
    git      = "https://git.bioconductor.org/packages/ProtGenerics.git"

    version('1.8.0', commit='b2b3bb0938e20f58fca905f6870de7dbc9dfd7a3')

    depends_on('r@3.4.0:3.4.9', when='@1.8.0')
