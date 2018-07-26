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
import os


class Ftgl(AutotoolsPackage):
    """Library to use arbitrary fonts in OpenGL applications."""

    homepage = "http://ftgl.sourceforge.net/docs/html/"
    url      = "https://sourceforge.net/projects/ftgl/files/FTGL%20Source/2.1.2/ftgl-2.1.2.tar.gz/download"
    list_url = "https://sourceforge.net/projects/ftgl/files/FTGL%20Source/"
    list_depth = 1

    version('2.1.2', 'f81c0a7128192ba11e036186f9a968f2')

    # There is an unnecessary qualifier around, which makes modern GCC sad
    patch('remove-extra-qualifier.diff')

    # Ftgl does not come with a configure script
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    depends_on('pkgconfig', type='build')
    depends_on('gl')
    depends_on('glu')
    depends_on('freetype@2.0.9:')

    # Currently, "make install" will fail if the docs weren't built
    #
    # FIXME: Can someone with autotools experience fix the build system
    #        so that it doesn't fail when that happens?
    #
    depends_on('doxygen', type='build')

    @property
    @when('@2.1.2')
    def configure_directory(self):
        subdir = 'unix'
        if sys.platform == 'darwin':
            subdir = 'mac'
        return os.path.join(self.stage.source_path, subdir)
