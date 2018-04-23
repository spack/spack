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
