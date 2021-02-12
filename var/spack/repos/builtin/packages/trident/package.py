# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Trident(Package):
    """Trident is a fully supported open source project maintained by
    NetApp. It has been designed from the ground up to help you meet
    the sophisticated persistence demands of your containerized
    applications."""

    homepage = "https://netapp-trident.readthedocs.io"
    url      = "https://github.com/NetApp/trident/archive/v20.01.1.tar.gz"

    version('21.01.0', sha256='548c21836c48ba73447b87b4c1764e04db33504997423ccb1c7f322663d11b35')
    version('20.10.1', sha256='7f42f4e4744b09f75def48092eda6c31c60eba5ba995b7bebb844a6eb4a0b242')
    version('20.10.0', sha256='81ef93e3170484f3ec17c4cb4e11456c69b8ab501d307b39938e10715926e2a3')
    version('20.07.1', sha256='95bec84aa94443329cf87d8dec79d46a7435923c40e481d3c3c35afd7d19cfd2')
    version('20.07.0', sha256='8f76c1d62554e70b022bd4f6271ada91fc28470dc78e54f01d21a796dccf665d')
    version('20.04.0', sha256='5e410f52bfa38dc50c375dd8132091c7861d2321fb934e22f7d67e228df2047b')
    version('20.01.1', sha256='02ba92e569916b98fb1b563c5ef03a94fd7981c3ac1ecb47e69ebb45471dc976')
    version('20.01.0', sha256='5de190579acf62f5e9945dfd45aeb21989272c4972e85cb10256b7ec605c29c7')

    depends_on('go', type='build')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        go = which('go')
        go('build', '-o', prefix.bin)
        with working_dir('cli'):
            go('build', '-o', prefix.bin.tridentctl)
