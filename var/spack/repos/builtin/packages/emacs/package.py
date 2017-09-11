##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Emacs(AutotoolsPackage):
    """The Emacs programmable text editor."""

    homepage = "https://www.gnu.org/software/emacs"
    url      = "http://ftp.gnu.org/gnu/emacs/emacs-24.5.tar.gz"

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

    depends_on('pkg-config@0.9.0:', type='build')

    depends_on('ncurses')
    depends_on('zlib')
    depends_on('libtiff', when='+X')
    depends_on('libpng', when='+X')
    depends_on('libxpm', when='+X')
    depends_on('giflib', when='+X')
    depends_on('libx11', when='+X')
    depends_on('libxaw', when='+X toolkit=athena')
    depends_on('gtkplus+X', when='+X toolkit=gtk')

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

        return args
