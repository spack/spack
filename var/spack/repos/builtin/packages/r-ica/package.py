# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIca(RPackage):
    """Independent Component Analysis (ICA) using various algorithms: FastICA,
    Information-Maximization (Infomax), and Joint Approximate Diagonalization
    of Eigenmatrices (JADE)."""

    homepage = "https://cloud.r-project.org/package=ica"
    url      = "https://cloud.r-project.org/src/contrib/ica_1.0-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ica"

    version('1.0-2', sha256='e721596fc6175d3270a60d5e0b5b98be103a8fd0dd93ef16680af21fe0b54179')
    version('1.0-1', '15c8d5afeec2804beec55dd14abc585d')
    version('1.0-0', '3ade2b3b00eb39c348d802f24d2afd1d')
