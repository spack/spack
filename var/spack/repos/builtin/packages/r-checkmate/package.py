# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCheckmate(RPackage):
    """Tests and assertions to perform frequent argument checks.
    A substantial part of the package was written in C to
    minimize any worries about execution time overhead."""

    homepage = "https://cran.r-project.org/package=checkmate"
    url      = "https://cran.rstudio.com/src/contrib/checkmate_1.8.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/checkmate"

    version('1.8.4', '00bd2c464386614da208f82c4b21910b')

    depends_on('r-backports', type=('build', 'run'))
