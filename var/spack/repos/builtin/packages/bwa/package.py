# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bwa(Package):
    """Burrow-Wheeler Aligner for pairwise alignment between DNA sequences."""

    homepage = "http://github.com/lh3/bwa"
    url      = "https://github.com/lh3/bwa/releases/download/v0.7.15/bwa-0.7.15.tar.bz2"

    version('0.7.17', '82cba7ef695538e6a38b9d4156837381')
    version('0.7.16a', 'c5115c9a5ea0406848500e4b23a7708c')
    version('0.7.15', 'fcf470a46a1dbe2f96a1c5b87c530554')
    version('0.7.13', 'f094f609438511766c434178a3635ab4')
    version('0.7.12', 'e24a587baaad411d5da89516ad7a261a',
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
