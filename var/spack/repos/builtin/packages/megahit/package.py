# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Megahit(MakefilePackage):
    """MEGAHIT: An ultra-fast single-node solution for
    large and complex metagenomics assembly via succinct de Bruijn graph"""

    homepage = "https://github.com/voutcn/megahit"
    url      = "https://github.com/voutcn/megahit/archive/v1.1.3.tar.gz"

    version('1.1.4', sha256='ecd64c8bfa516ef6b19f9b2961ede281ec814db836f1a91953c213c944e1575f')
    version('1.1.3', '2962a781a22c0884fa97b95f740ed2fe')

    depends_on('zlib')

    patch('amd.patch', when='target=aarch64:')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('megahit', prefix.bin)
        install('megahit_asm_core', prefix.bin)
        install('megahit_sdbg_build', prefix.bin)
        install('megahit_toolkit', prefix.bin)
