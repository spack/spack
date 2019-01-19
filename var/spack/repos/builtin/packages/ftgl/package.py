# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
