# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Erfa(AutotoolsPackage):
    """ERFA (Essential Routines for Fundamental Astronomy)
    is a C library containing key algorithms for astronomy."""

    homepage = "https://github.com/liberfa/erfa"
    url      = "https://github.com/liberfa/erfa/releases/download/v1.7.0/erfa-1.7.0.tar.gz"

    version('1.7.2', sha256='b85ee6f723c8c01a7da85982a5f53838e8133f65ebf98ddf70a454e95cbaf96e')
    version('1.7.1', sha256='80239ae9ba4bf7f328f7f64baec7fc38e587058b3ef9cea9331c751de0b98783')
    version('1.7.0', sha256='f0787e30e848750c0cbfc14827de6fc7f69a2d5ef0fc653504e74b8967a764e0')
    version('1.4.0', sha256='035b7f0ad05c1191b8588191ba4b19ba0f31afa57ad561d33bd5417d9f23e460')
