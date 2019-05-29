# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fltk(Package):
    """FLTK (pronounced "fulltick") is a cross-platform C++ GUI toolkit for
       UNIX/Linux (X11), Microsoft Windows, and MacOS X. FLTK provides
       modern GUI functionality without the bloat and supports 3D
       graphics via OpenGL and its built-in GLUT emulation.

       FLTK is designed to be small and modular enough to be statically
       linked, but works fine as a shared library. FLTK also includes an
       excellent UI builder called FLUID that can be used to create
       applications in minutes.

    """
    homepage = 'http://www.fltk.org/'
    url = 'http://fltk.org/pub/fltk/1.3.3/fltk-1.3.3-source.tar.gz'

    version('1.3.3', '9ccdb0d19dc104b87179bd9fd10822e3')

    depends_on('libx11')

    patch('font.patch', when='@1.3.3')

    variant('shared', default=True,
            description='Enables the build of shared libraries')

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix,
                   '--enable-localjpeg',
                   '--enable-localpng',
                   '--enable-localzlib']

        if '+shared' in spec:
            options.append('--enable-shared')

        # FLTK needs to be built in-source
        configure(*options)
        make()
        make('install')
