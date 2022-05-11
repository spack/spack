# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RIca(RPackage):
    """Independent Component Analysis.

    Independent Component Analysis (ICA) using various algorithms: FastICA,
    Information-Maximization (Infomax), and Joint Approximate Diagonalization
    of Eigenmatrices (JADE)."""

    cran = "ica"

    version('1.0-2', sha256='e721596fc6175d3270a60d5e0b5b98be103a8fd0dd93ef16680af21fe0b54179')
    version('1.0-1', sha256='98559a8bb12dd134a40ce8fd133803e2a38456b45d0e2a507d66022a8e2274ae')
    version('1.0-0', sha256='9ff4ec7f4525bdce9d7859b22a1a170a1f6f9f7fb9f3d0b537dcaec77cd83d01')
