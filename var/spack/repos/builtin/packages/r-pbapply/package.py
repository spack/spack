# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPbapply(RPackage):
    """A lightweight package that adds progress bar to vectorized R
    apply functions."""

    homepage = "https://cloud.r-project.org/package=pbapply"
    url      = "https://cloud.r-project.org/src/contrib/pbapply_1.3-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pbapply"

    version('1.4-1', sha256='b3633349181db944e1dfc4422b4728a6562e454117a232cbb51633906cd27cad')
    version('1.3-4', sha256='cdfdaf9b8aecbe48daac858aecaf65a766b74a363d1eb7cd6ebf27c0549f6552')
    version('1.3-3', '570db6795179a1439c174be881c77d18')
    version('1.3-2', 'd72a777bfe4a28ba4e1585e31680f82e')
    version('1.3-1', '13d64dead441426aa96a3bf3fde29daf')
    version('1.3-0', 'a3f93cd05054657a01893a3817fa1f08')
    version('1.2-2', '23e2bfe531c704b79308b0b5fbe1ace8')

    depends_on('r@3.2.0:', type=('build', 'run'))
