# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RCatools(RPackage):
    """Contains several basic utility functions including: moving (rolling,
    running) window statistic functions, read/write for GIF and ENVI binary
    files, fast calculation of AUC, LogitBoost classifier, base64
    encoder/decoder, round-off-error-free sum and cumsum, etc."""

    homepage = "https://cran.r-project.org/package=caTools"
    url      = "https://cran.r-project.org/src/contrib/caTools_1.17.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/caTools"

    version('1.17.1', '5c872bbc78b177b306f36709deb44498')

    depends_on('r-bitops', type=('build', 'run'))
