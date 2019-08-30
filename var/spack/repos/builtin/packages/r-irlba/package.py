# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIrlba(RPackage):
    """Fast and memory efficient methods for truncated singular and eigenvalue
    decompositions and principal component analysis of large sparse or dense
    matrices."""

    homepage = "https://cloud.r-project.org/package=irlba"
    url      = "https://cloud.r-project.org/src/contrib/irlba_2.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/irlba"

    version('2.3.3', sha256='6ee233697bcd579813bd0af5e1f4e6dd1eea971e8919c748408130d970fef5c0')
    version('2.3.2', sha256='3fdf2d8fefa6ab14cd0992740de7958f9f501c71aca93229f5eb03c54558fc38')
    version('2.1.2', '290940abf6662ed10c0c5a8db1bc6e88')
    version('2.0.0', '557674cf8b68fea5b9f231058c324d26')

    depends_on('r-matrix', type=('build', 'run'))
