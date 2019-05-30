# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Seqtk(Package):
    """Toolkit for processing sequences in FASTA/Q formats."""

    homepage = "https://github.com/lh3/seqtk"
    url      = "https://github.com/lh3/seqtk/archive/v1.1.tar.gz"

    version('1.3', sha256='5a1687d65690f2f7fa3f998d47c3c5037e792f17ce119dab52fff3cfdca1e563')
    version('1.2', '255ffe05bf2f073dc57abcff97f11a37')
    version('1.1', 'ebf5cc57698a217150c2250494e039a2')

    depends_on('zlib')

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)
        install('seqtk', prefix.bin)
        set_executable(join_path(prefix.bin, 'seqtk'))
