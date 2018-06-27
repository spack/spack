##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import sys


class Pixman(AutotoolsPackage):
    """The Pixman package contains a library that provides low-level
    pixel manipulation features such as image compositing and
    trapezoid rasterization."""

    homepage = "http://www.pixman.org"
    url      = "http://cairographics.org/releases/pixman-0.32.6.tar.gz"

    version('0.34.0', 'e80ebae4da01e77f68744319f01d52a3')
    version('0.32.6', '3a30859719a41bd0f5cccffbfefdd4c2')

    depends_on('pkgconfig', type='build')
    depends_on('libpng')

    # As discussed here:
    # https://bugs.freedesktop.org/show_bug.cgi?id=104886
    # __builtin_shuffle was removed in clang 5.0.
    # From version 9.1 apple-clang is based on clang 5.0.
    # Patch is obtained from above link.
    patch('clang.patch', when='%clang@9.1.0-apple:')

    @run_before('build')
    def patch_config_h_for_intel(self):
        config_h = join_path(self.stage.source_path, 'config.h')

        # Intel disguises itself as GNU, but doesn't implement
        # the same builtin functions. This causes in this case
        # a positive detection of GCC vector extensions, which
        # is bound to fail at compile time because Intel has no
        # __builtin_shuffle. See also:
        #
        # https://software.intel.com/en-us/forums/intel-c-compiler/topic/758013
        #
        if '%intel' in self.spec:
            filter_file(
                '#define HAVE_GCC_VECTOR_EXTENSIONS /\*\*/',
                '/* #undef HAVE_GCC_VECTOR_EXTENSIONS */',
                config_h
            )

    def configure_args(self):
        args = [
            '--enable-libpng',
            '--disable-gtk',
        ]

        if sys.platform == 'darwin':
            args.append('--disable-mmx')

        return args
