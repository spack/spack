# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBiocmanager(RPackage):
    """BiocManager: Access the Bioconductor Project Package Repository"""

    homepage = "https://cloud.r-project.org/package=BiocManager"
    url      = "https://cloud.r-project.org/src/contrib/BiocManager_1.30.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/BiocManager"

    version('1.30.4', sha256='50093f5c8ed8fba6e68bc715784b713887bdad3538fbb92f152dcc1eaf39ba4f')

    depends_on('r@3.5.0:', type=('build', 'run'))
