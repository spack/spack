# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTclust(RPackage):
    """Provides functions for robust trimmed clustering."""

    homepage = "https://cloud.r-project.org/package=tclust"
    url      = "https://cloud.r-project.org/src/contrib/tclust_1.3-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tclust"

    version('1.4-1', sha256='4b0be612c8ecd7b4eb19a44ab6ac8f5d40515600ae1144c55989b6b41335ad9e')
    version('1.3-1',  '5415d74682588d4a6fb8ce166fc75661')
    version('1.2-7',  'e32cd02819682cc944c7baaac3b6f2b7')
    version('1.2-3',  '922abc1abd8da4c6ac9830e1f2f71e84')
    version('1.1-03', 'f1cc9278bdb068acce4623a9d98b7b62')
    version('1.1-02', '6f206501b0341fb5623208d145984f5a')

    depends_on('r@2.12.0:', type=('build', 'run'))
