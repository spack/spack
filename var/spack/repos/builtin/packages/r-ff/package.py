# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFf(RPackage):
    """memory-efficient storage of large data on disk and
    fast access functions."""

    homepage = "http://ff.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/ff_2.2-13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ff"

    version('2.2-14', sha256='1c6307847275b1b8ad9e2ffdce3f4df3c9d955dc2e8a45e3fd7bfd2b0926e2f0')
    version('2.2-13', '4adf8840d24cb6e2927a3ef885c86fcd')

    depends_on('r@2.10.1:', type=('build', 'run'))
    depends_on('r-bit@1.1-13:', type=('build', 'run'))
