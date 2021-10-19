# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BigdftSuite(Package):
    """BigDFT: electronic structure calculation based on Daubechies wavelets."""

    homepage = "https://bigdft.org/"
    url      = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.1/bigdft-suite-1.9.1.tar.gz"
    git      = "https://gitlab.com/l_sim/bigdft-suite.git"

    version('1.9.1', sha256='3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41')
    version('1.9.0', sha256='4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8')
    version('1.8.3', sha256='f112bb08833da4d11dd0f14f7ab10d740b62bc924806d77c985eb04ae0629909')
    version('1.8.2', sha256='042e5a3b478b1a4c050c450a9b1be7bcf8e13eacbce4759b7f2d79268b298d61')
    version('1.8.1', sha256='e09ff0ba381f6ffbe6a3c0cb71db5b73117874beb41f22a982a7e5ba32d018b3')

    depends_on('bigdft-futile@1.9.1',    when='@1.9.1')
    depends_on('bigdft-futile@1.9.0',    when='@1.9.0')
    depends_on('bigdft-futile@1.8.3',    when='@1.8.3')
    depends_on('bigdft-futile@1.8.2',    when='@1.8.2')
    depends_on('bigdft-futile@1.8.1',    when='@1.8.1')
    depends_on('bigdft-atlab@1.9.1',     when='@1.9.1')
    depends_on('bigdft-atlab@1.9.0',     when='@1.9.0')
    depends_on('bigdft-atlab@1.8.3',     when='@1.8.3')
    depends_on('bigdft-psolver@1.9.1',   when='@1.9.1')
    depends_on('bigdft-psolver@1.9.0',   when='@1.9.0')
    depends_on('bigdft-psolver@1.8.3',   when='@1.8.3')
    depends_on('bigdft-psolver@1.8.2',   when='@1.8.2')
    depends_on('bigdft-psolver@1.8.1',   when='@1.8.1')
    depends_on('bigdft-libabinit@1.9.1', when='@1.9.1')
    depends_on('bigdft-libabinit@1.9.0', when='@1.9.0')
    depends_on('bigdft-libabinit@1.8.3', when='@1.8.3')
    depends_on('bigdft-libabinit@1.8.2', when='@1.8.2')
    depends_on('bigdft-libabinit@1.8.1', when='@1.8.1')
    depends_on('bigdft-chess@1.9.1',     when='@1.9.1')
    depends_on('bigdft-chess@1.9.0',     when='@1.9.0')
    depends_on('bigdft-chess@1.8.3',     when='@1.8.3')
    depends_on('bigdft-chess@1.8.2',     when='@1.8.2')
    depends_on('bigdft-chess@1.8.1',     when='@1.8.1')
    depends_on('py-bigdft@1.9.1',        when='@1.9.1')
    depends_on('py-bigdft@1.9.0',        when='@1.9.0')
    depends_on('bigdft-core@1.9.1',      when='@1.9.1')
    depends_on('bigdft-core@1.9.0',      when='@1.9.0')
    depends_on('bigdft-core@1.8.3',      when='@1.8.3')
    depends_on('bigdft-core@1.8.2',      when='@1.8.2')
    depends_on('bigdft-core@1.8.1',      when='@1.8.1')
    depends_on('bigdft-spred@1.9.1',     when='@1.9.1')
    depends_on('bigdft-spred@1.9.0',     when='@1.9.0')
    depends_on('bigdft-spred@1.8.3',     when='@1.8.3')
    depends_on('bigdft-spred@1.8.2',     when='@1.8.2')
    depends_on('bigdft-spred@1.8.1',     when='@1.8.1')

    phases = ['install']

    def install(self, spec, prefix):
        install_tree(spec['bigdft-futile'].prefix,    prefix)
        install_tree(spec['bigdft-psolver'].prefix,   prefix)
        install_tree(spec['bigdft-libabinit'].prefix, prefix)
        install_tree(spec['bigdft-chess'].prefix,     prefix)
        install_tree(spec['bigdft-core'].prefix,      prefix)
        install_tree(spec['bigdft-spred'].prefix,     prefix)
        if spec.satisfies('@1.9.0:'):
            install_tree(spec['py-bigdft'].prefix,    prefix)
        if spec.satisfies('@1.8.3:'):
            install_tree(spec['bigdft-atlab'].prefix, prefix)
