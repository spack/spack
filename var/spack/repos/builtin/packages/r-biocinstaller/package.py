# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBiocinstaller(RPackage):
    """This package is used to install and update Bioconductor, CRAN,
    and (some) github packages."""

    homepage = "https://bioconductor.org/packages/BiocInstaller/"
    git      = "https://git.bioconductor.org/packages/BiocInstaller.git"

    version('1.26.1', commit='9049b82a77aefa98e3f8e4dd7068317505d70e98')

    depends_on('r@3.4.0:3.4.9', when='@1.26.1')
