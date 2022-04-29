# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class BigdftSuite(BundlePackage):
    """BigDFT-suite: the complete suite of BigDFT for electronic structure calculation
       based on Daubechies wavelets."""

    homepage = "https://bigdft.org/"
    url      = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.2/bigdft-suite-1.9.2.tar.gz"
    git      = "https://gitlab.com/l_sim/bigdft-suite.git"

    version('develop', branch='devel')
    version('1.9.2',   sha256='dc9e49b68f122a9886fa0ef09970f62e7ba21bb9ab1b86be9b7d7e22ed8fbe0f')
    version('1.9.1',   sha256='3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41')
    version('1.9.0',   sha256='4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8')
    version('1.8.3',   sha256='f112bb08833da4d11dd0f14f7ab10d740b62bc924806d77c985eb04ae0629909')
    version('1.8.2',   sha256='042e5a3b478b1a4c050c450a9b1be7bcf8e13eacbce4759b7f2d79268b298d61')
    version('1.8.1',   sha256='e09ff0ba381f6ffbe6a3c0cb71db5b73117874beb41f22a982a7e5ba32d018b3')

    depends_on('python@:2.8', type=('run'), when="@:1.8.3")
    depends_on('python@3.0:', type=('run'), when="@1.9.0:")
    depends_on('python@3.0:', type=('run'), when="@develop")

    for vers in ['1.8.1', '1.8.2', '1.8.3', '1.9.0', '1.9.1', '1.9.2', 'develop']:
        depends_on('bigdft-futile@{0}'.format(vers),    when='@{0}'.format(vers))
        depends_on('bigdft-psolver@{0}'.format(vers),   when='@{0}'.format(vers))
        depends_on('bigdft-libabinit@{0}'.format(vers), when='@{0}'.format(vers))
        depends_on('bigdft-chess@{0}'.format(vers),     when='@{0}'.format(vers))
        depends_on('bigdft-core@{0}'.format(vers),      when='@{0}'.format(vers))
        depends_on('bigdft-spred@{0}'.format(vers),     when='@{0}'.format(vers))
    for vers in ['1.8.3', '1.9.0', '1.9.1', '1.9.2', 'develop']:
        depends_on('bigdft-atlab@{0}'.format(vers),     when='@{0}'.format(vers))
    for vers in ['1.9.0', '1.9.1', '1.9.2', 'develop']:
        depends_on('py-bigdft@{0}'.format(vers),        when='@{0}'.format(vers))
