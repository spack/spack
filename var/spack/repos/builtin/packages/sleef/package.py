# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sleef(CMakePackage):
    """SIMD Library for Evaluating Elementary Functions,
    vectorized libm and DFT."""

    homepage = "http://sleef.org"
    url      = "https://github.com/shibatch/sleef/archive/3.2.tar.gz"

    version('3.5.1', sha256='415ee9b1bcc5816989d3d4d92afd0cd3f9ee89cbd5a33eb008e69751e40438ab')
    version('3.5.0', sha256='6b952560cec091477affcb18baf06bf50cef9f932ff6aba491a744ee8e77ffea')
    version('3.2', sha256='3130c5966e204e6d6a3ace81e543d12b5b21f60897f1c185bfa587c1bd77bee2')
