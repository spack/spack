# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import sys


class Emacs(AutotoolsPackage):
    """The Emacs programmable text editor."""

    homepage = "https://www.gnu.org/software/emacs"
    url      = "https://ftpmirror.gnu.org/emacs/emacs-24.5.tar.gz"

    version('26.1', '544d2ab5eb142e9ca69adb023d17bf4b')
    version('25.3', '74ddd373dc52ac05ca7a8c63b1ddbf58')
    version('25.2', '0a36d1cdbba6024d4dbbac027f87995f')
    version('25.1', '95c12e6a9afdf0dcbdd7d2efa26ca42c')
    version('24.5', 'd74b597503a68105e61b5b9f6d065b44')

    variant('X', default=False, description="Enable an X toolkit")
    variant(
        'toolkit',
        default='gtk',
        values=('gtk', 'athena'),
        description="Select an X toolkit (gtk, athena)"
    )
    variant('tls', default=False, description="Build Emacs with gnutls")

    depends_on('pkgconfig', type='build')

    depends_on('ncurses')
    depends_on('pcre')
    depends_on('zlib')
    depends_on('libtiff', when='+X')
    depends_on('libpng', when='+X')
    depends_on('libxpm', when='+X')
    depends_on('giflib', when='+X')
    depends_on('libx11', when='+X')
    depends_on('libxaw', when='+X toolkit=athena')
    depends_on('gtkplus', when='+X toolkit=gtk')
    depends_on('gnutls', when='+tls')

    def setup_environment(self, spack_env, run_env):
        # building emacs requires c11 - gcc supports it with -std=c11
        # icc probably supports it with -std=c++11 (not exactly the same,
        # but should work)
        # NOTE: this is the wrong way to acheive this: (see
        # http://spack.readthedocs.io/en/latest/packaging_guide.html?highlight=CFLAGS#compiler-flags )
        # but it worked, I got emacs to build, and after 3 days of fighting 
        # in rabbit holes to acheive that, I'm scared to change it. So leaving
        # the proven solution as a comment: 
        #if self.compiler.name == 'gcc':
        #    spack_env.set('CFLAGS','-std=c11')
        # Now here's a more "correct" solution:
        spack_env.append_flags('CFLAGS','-std=c11')


    def configure_args(self):
        spec = self.spec

        toolkit = spec.variants['toolkit'].value
        if '+X' in spec:
            args = [
                '--with-x',
                '--with-x-toolkit={0}'.format(toolkit)
            ]
        else:
            args = ['--without-x']

        # building emacs requires c++11. how to tell spack to add the 
        # appropriate flag depending on the compiler used? dammit why 
        # must everything be "guess the magic incantation"?!?!?
        # something like this from fftw might work:
        #   options.insert(0, 'CFLAGS=' + self.compiler.openmp_flag)
        # .. except for -std=c11 (for gnu - or whatever the compiler c11
        # flag is. Just hardcode it for now
        #    options.insert(0, 'CFLAGS=-std=c11')
        # On OS X/macOS, do not build "nextstep/Emacs.app", because
        # doing so throws an error at build-time
        if sys.platform == 'darwin':
            args.append('--without-ns')

        if '+tls' in spec:
            args.append('--with-gnutls')
        else:
            args.append('--without-gnutls')

        return args
