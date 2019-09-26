# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPlotrix(RPackage):
    """Lots of plots, various labeling, axis and color scaling functions."""

    homepage = "https://cloud.r-project.org/package=plotrix"
    url      = "https://cloud.r-project.org/src/contrib/plotrix_3.6-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/plotrix"

    version('3.7-6', sha256='83d5f7574592953288b4fe39c4c0dd7670d097598ad7f6bddbb0687a32954e46')
    version('3.7-5', sha256='b22f3f9d93961d23ad46e41597d1e45d2665ced04dcad8c40f6806a67cded14c')
    version('3.6-4', 'efe9b9b093d8903228a9b56c46d943fa')
    version('3.6-3', '23e3e022a13a596e9b77b40afcb4a2ef')

    depends_on('r@3.5.0:', when='@3.7-6:', type=('build', 'run'))
