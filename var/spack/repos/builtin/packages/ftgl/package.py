# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ftgl(AutotoolsPackage):
    """Library to use arbitrary fonts in OpenGL applications."""

    homepage = "http://ftgl.sourceforge.net/docs/html/"
    url      = "https://sourceforge.net/projects/ftgl/files/FTGL%20Source/2.1.2/ftgl-2.1.2.tar.gz/download"
    list_url = "https://sourceforge.net/projects/ftgl/files/FTGL%20Source/"
    list_depth = 1

    version('2.1.3-rc5', sha256='5458d62122454869572d39f8aa85745fc05d5518001bcefa63bd6cbb8d26565b')

    patch('ftgl-2.1.3-rc5-ldflags.patch')

    def patch(self):
        filter_file('SUBDIRS = src test demo docs',
                    'SUBDIRS = src test demo', 'Makefile.am')
        filter_file('SUBDIRS = src test demo docs',
                    'SUBDIRS = src test demo', 'Makefile.in')

    # Ftgl does not come with a configure script
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    depends_on('pkgconfig', type='build')
    depends_on('gl')
    depends_on('glu')
    depends_on('freetype@2.0.9:')

    def configure_args(self):
        args = ['--enable-shared', '--disable-static',
                '--with-gl-inc={0}'.format(
                    self.spec['gl'].prefix.include),
                '--with-gl-lib={0}'.format(
                    self.spec['gl'].prefix.lib),
                '--with-freetype={0}'.format(
                    self.spec['freetype'].prefix),
                '--with-glut-inc={0}'.format(
                    self.spec['glu'].prefix.include),
                '--with-glut-lib={0}'.format(
                    self.spec['glu'].prefix.lib),
                '--with-x']
        return args
