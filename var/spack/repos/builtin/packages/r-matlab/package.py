# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMatlab(RPackage):
    """MATLAB emulation package.

    Emulate MATLAB code using R."""

    cran = "matlab"

    version('1.0.2', sha256='a23dec736c51ae1864c1a53caac556a2f98e8020138a3b121badb0f5b7984154')

    depends_on('r@2.15:', type=('build', 'run'))
