# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Meme(AutotoolsPackage):
    """The MEME Suite allows the biologist to discover novel motifs in
    collections of unaligned nucleotide or protein sequences, and to perform a
    wide variety of other motif-based analyses."""

    homepage = "http://meme-suite.org"
    url      = "http://meme-suite.org/meme-software/4.11.4/meme_4.11.4.tar.gz"

    version('4.12.0', sha256='49ff80f842b59d328588acfcd1d15bf94c55fed661d22b0f95f37430cc363a06')
    version('4.11.4', sha256='3e869ff57e327a9c8615dbef784e3f1095f7f7a0120cecd55efe10c3f2ee8eb3')

    variant('mpi', default=True, description='Enable MPI support')
    variant('image-magick', default=False, description='Enable image-magick for png output')

    depends_on('zlib', type=('link'))
    depends_on('libgcrypt', type=('link'))
    depends_on('perl', type=('build', 'run'))
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('mpi', when='+mpi')
    depends_on('imagemagick', type=('build', 'run'), when='+image-magick')
    depends_on('perl-xml-parser', type=('build', 'run'))

    def configure_args(self):
        spec = self.spec
        # have meme build its own versions of libxml2/libxslt, see #6736
        args = ['--enable-build-libxml2', '--enable-build-libxslt']
        if '~mpi' in spec:
            args += ['--enable-serial']
        return args
