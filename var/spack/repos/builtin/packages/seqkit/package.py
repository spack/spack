# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Seqkit(Package):
    """A cross-platform and ultrafast toolkit for FASTA/Q file manipulation
    in Golang."""

    homepage = "http://bioinf.shenwei.me/seqkit"
    url      = "https://github.com/shenwei356/seqkit/releases/download/v0.10.1/seqkit_linux_amd64.tar.gz"

    version('0.15.0', sha256='bf305e7d5b4fbe14a6e87ebf6aa454117dd3cf030cb9473d01161c0a1987a182')
    version('0.14.0', sha256='77e6dcbd7b00100f32efa7410bb00700576cfc7ceec69c8ab4b378f584d4e9c6')
    version('0.13.2', sha256='53703542d44a5e758eaf34b55d18f70cfe23e9b5b78fd7c1c0202dee9a65bed0')
    version('0.13.1', sha256='53d4b06240be2292251b9304d405a22c9f32cc6fa2cd59d2bb6cc35bd73f57f7')
    version('0.13.0', sha256='cf8ed8742ca6379a50489bc86e2c48f804455212d2be1c306c076cd79d2b832d')
    version('0.12.1', sha256='bee5fe0fc3589155fd1cb8bf3bd7fb39fca14cb20196e0156ef9f97800c61be6')
    version('0.12.0', sha256='7d8a044fc07fce9f1af8e486df38500309cf68dd872b90e7404e184674cb5733')
    version('0.11.0', sha256='1e4e93d5521a109551f64176fb7c9b1445497ab14d1bbee42a7c6b5c4530749b')
    version('0.10.1', sha256='82f1c86dc4bd196403a56c2bf3ec063e5674a71777e68d940c4cc3d8411d2e9d')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('seqkit', prefix.bin)
