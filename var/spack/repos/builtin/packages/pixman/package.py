# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
