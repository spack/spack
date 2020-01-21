# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bwa(Package):
    """Burrow-Wheeler Aligner for pairwise alignment between DNA sequences."""

    homepage = "http://github.com/lh3/bwa"
    url      = "https://github.com/lh3/bwa/releases/download/v0.7.15/bwa-0.7.15.tar.bz2"

    version('0.7.17', sha256='de1b4d4e745c0b7fc3e107b5155a51ac063011d33a5d82696331ecf4bed8d0fd')
    version('0.7.15', sha256='2f56afefa49acc9bf45f12edb58e412565086cc20be098b8bf15ec07de8c0515')
    version('0.7.13', sha256='559b3c63266e5d5351f7665268263dbb9592f3c1c4569e7a4a75a15f17f0aedc')
    version('0.7.12', sha256='285f55b7fa1f9e873eda9a9b06752378a799ecdecbc886bbd9ba238045bf62e0',
            url='https://github.com/lh3/bwa/archive/0.7.12.tar.gz')

    depends_on('zlib')

    def install(self, spec, prefix):
        filter_file(r'^INCLUDES=',
                    "INCLUDES=-I%s" % spec['zlib'].prefix.include, 'Makefile')
        filter_file(r'^LIBS=', "LIBS=-L%s " % spec['zlib'].prefix.lib,
                    'Makefile')
        make()

        mkdirp(prefix.bin)
        install('bwa', join_path(prefix.bin, 'bwa'))
        set_executable(join_path(prefix.bin, 'bwa'))
        mkdirp(prefix.doc)
        install('README.md', prefix.doc)
        install('NEWS.md', prefix.doc)
        mkdirp(prefix.man.man1)
        install('bwa.1', prefix.man.man1)
