# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Minimap2(MakefilePackage):
    """Minimap2 is a versatile sequence alignment program that aligns DNA or
       mRNA sequences against a large reference database."""

    homepage = "https://github.com/lh3/minimap2"
    url      = "https://github.com/lh3/minimap2/releases/download/v2.2/minimap2-2.2.tar.bz2"

    version('2.14', '9088b785bb0c33488ca3a27c8994648ce21a8be54cb117f5ecee26343facd03b')
    version('2.10', '52b36f726ec00bfca4a2ffc23036d1a2b5f96f0aae5a92fd826be6680c481c20') 
    version('2.2', '5b68e094f4fa3dfbd9b37d5b654b7715')

    depends_on('py-mappy', type=('build', 'run'))
    depends_on('zlib')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('minimap2', prefix.bin)
