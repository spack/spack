# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RScaledmatrix(RPackage):
    """Creating a DelayedMatrix of Scaled and Centered Values.

    Provides delayed computation of a matrix of scaled and centered values.
    The result is equivalent to using the scale() function but avoids explicit
    realization of a dense matrix during block processing. This permits greater
    efficiency in common operations, most notably matrix multiplication."""

    bioc = "ScaledMatrix"

    version('1.2.0', commit='d0573e14ca537b40ade7dd1c9cf0cadae60d4349')

    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-delayedarray', type=('build', 'run'))
