# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Modeltest(Package):
    """ModelTest-NG is a tool for selecting the best-fit model of evolution
    for DNA and protein alignments. ModelTest-NG supersedes jModelTest and
    ProtTest in one single tool, with graphical and command console
    interfaces.
    """

    homepage = "https://github.com/ddarriba/modeltest/"
    url      = "https://github.com/ddarriba/modeltest/files/3790700/modeltest-ng-0.1.6-static-linux64.tar.gz"

    version('0.1.6-static', sha256='9b9436c7faad536f519cb9e659059e42ca19909c85cbe9c021c508cb99ad1cf7')
    version('0.1.5-static', sha256='e791a3c17a24c05a5d8ec734c492e0ac1a2a1aa5c9733fde2a8ccdef9634366a')
    version('0.1.4-static', sha256='1581d7a62ef15ea59df0929bf8dfe03fc511561827f7d4e2f9f167f0e2f3552f')
    version('0.1.3-static', sha256='f616ef126b20c03a2075eada2498d4d09576f4bfb2382a10ac0143e49b25bacb')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('modeltest-ng-static', prefix.bin)
