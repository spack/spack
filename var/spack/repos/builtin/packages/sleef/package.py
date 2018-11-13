# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sleef(CMakePackage):
    """SIMD Library for Evaluating Elementary Functions,
    vectorized libm and DFT."""

    homepage = "http://sleef.org"
    url      = "https://github.com/shibatch/sleef/archive/3.2.tar.gz"

    version('3.2', '459215058f2c8d55cd2b644d56c8c4f0')
