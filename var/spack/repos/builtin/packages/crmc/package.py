# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Crmc(CMakePackage):
    """CRMC (Cosmic Ray Monte Carlo package). CRMC is a package providing
       a common interface to access the output from event generators used
       to model the secondary particle production in hadronic collisons."""

    homepage = "https://web.ikp.kit.edu/rulrich/crmc.html"
    # Original URL has non-recognized certificate + is password-protected
    # url = "https://devel-ik.fzk.de/wsvn/mc/crmc/tags/crmc.v1.7.0/?op=dl"
    url = "https://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/crmc.v1.7.0.tar.gz"

    # Version 1.7.0 has issues linking phojet, devs contacted but no response
    # version('1.7.0', sha256='59086f4e654d775a4f6c3974ae89bbfd995391c4677f266881604878b47563d1')
    version('1.6.0', sha256='ae2ba5aa2a483d20aa60bef35080f555b365715d1a8fae54b473c275813345c1')
    version('1.5.7', sha256='ec7456c08b60a40665e9ff31d6029e0151b0cdf2ca98bd09a8b570b1e33f6053')
    version('1.5.6', sha256='a546a9352dcbdb8a1df3d63530eacf16f8b64a190e224b72afd434f78388a8a0')
    version('1.5.4', sha256='0021517314da0d8bc97209a9398295bf11072e435db9f2e59f283987015f03dc', deprecated=True)
    version('1.5.3', sha256='20cb98ea9f63a8f20f0170ba039df38a1985ec649d88dd488711b1a106c70b02', deprecated=True)
    version('1.4',   sha256='69c5e89953dcbbe4d14c541c0f76ae98a414b90c2838f3c9cac9fcfb4237de40', deprecated=True)
    version('1.3',   sha256='cc42ee2b1da3e76eb93fecaabe7ed39e4b0af37aa40bb09527fd22042cd41e62', deprecated=True)
    version('1.2',   sha256='097ebbbef041f33236fa220dc29e71da4214b55d7265b68d27ce52ce8a8c9162', deprecated=True)
    version('1.0',   sha256='1b660546902b8ab72406248d032d02c6d51e8f085f493231ebe72bbc653cc22c', deprecated=True)

    depends_on('hepmc')
    depends_on('boost')
    depends_on('root')

    patch('crmc-1.6.0.patch', when='@1.6.0', level=0)
    patch('crmc-1.5.6.patch', when='@1.5.6:1.5.7', level=0)

    def cmake_args(self):
        args = ['-D__PYTHIA__=ON',
                '-D__SIBYLL__=ON',
                '-D__PHOJET__=ON',
                '-D__DPMJET__=ON',
                '-D__QGSJETII04__=ON',
                '-DCMAKE_CXX_FLAGS=-std=c++' +
                self.spec['root'].variants['cxxstd'].value]
        if self.spec.satisfies('@1.6.0:'):
            args.append('-D__HIJING__=ON')
        if self.spec.satisfies('%gcc@9:'):
            args.append('-DCMAKE_Fortran_FLAGS=-fallow-argument-mismatch')
        return args
