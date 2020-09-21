# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySentryPython(PythonPackage):
    """The new Python SDK for Sentry.io"""

    homepage = "https://github.com/getsentry/sentry-python"
    url      = "https://github.com/getsentry/sentry-python/archive/0.17.6.tar.gz"

    version('0.17.6', sha256='1a086486ff9da15791f294f6e9915eb3747d161ef64dee2d038a4d0b4a369b24')
    version('0.17.5', sha256='02f2a72698453f722b102562eb6430d2a82d6c6c40f2b991ed69e7628142de6a')
    version('0.17.4', sha256='a16caf9ce892623081cbb9a95f6c1f892778bb123909b0ed7afdfb52ce7a58a1')
    version('0.17.3', sha256='0af429c221670e602f960fca85ca3f607c85510a91f11e8be8f742a978127f78')
    version('0.17.2', sha256='bbfe5633aee4dacb53d79d303ab6bfacf1749fb717750c112fb1658e5accce0d')
    version('0.17.1', sha256='2c770e7bf72d6419bb82b3bb950f3789fc24bd6a0ba191369607a96289acd63b')
    version('0.17.0', sha256='09cbc253c827a88064c5ed548d24fb4294568bfe9b1816a857fa5a423d4ce762')
    version('0.16.5', sha256='e12eb1c2c01cd9e9cfe70608dbda4ef451f37ef0b7cbb92e5d43f87c341d6334')
    version('0.16.4', sha256='5f3d96ebd1cf758216552c1a0dc2ca1a000af19a4f9b4a3f4c237c7069fde1d4')
    version('0.16.3', sha256='21b17d6aa064c0fb703a7c00f77cf6c9c497cf2f83345c28892980a5e742d116')

    depends_on('python@2.7,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
