##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Glvis(Package):
    """GLVis: an OpenGL tool for visualization of FEM meshes and functions"""

    homepage = "http://glvis.org/"
    url      = "https://github.com/GLvis/glvis/archive/v3.3.tar.gz"

    # glvis (like mfem) is downloaded from a URL shortener at request
    # of upstream author Tzanio Kolev <tzanio@llnl.gov>.  See here:
    # https://github.com/mfem/mfem/issues/53
    #
    # The following procedure should be used to verify security when a
    # new version is added:
    #
    # 1. Verify that no checksums on old versions have changed.
    #
    # 2. Verify that the shortened URL for the new version is listed at:
    #    http://glvis.org/download/
    #
    # 3. Use http://getlinkinfo.com or similar to verify that the
    #    underling download link for the latest version comes has the
    #    prefix: http://glvis.github.io/releases
    #
    # If this quick verification procedure fails, additional discussion
    # will be required to verify the new version.

    version('3.3',
            '1201a76d1b0c38240186c06f6478de77',
            url='http://goo.gl/C0Oadw',
            extension='.tar.gz')

    version('3.2',
            '4575a03a50d4730c07b5d4018e936707',
            url='http://goo.gl/hzupg1',
            extension='.tar.gz')

    version('3.1',
            '3ce8a53209c6593e066e568dbbf2bbf6',
            url='http://goo.gl/gQZuu9',
            extension='tar.gz')

    variant('screenshots',
            default='png',
            values=('none', 'png', 'tiff'),
            description='Backend used for screenshots (none = disabled)')
    variant('fonts', default=True,
            description='Build with font support via freetype & fontconfig')

    depends_on('mfem@3.1', when='@3.1')
    depends_on('mfem@3.2', when='@3.2')
    depends_on('mfem@3.3', when='@3.3')

    depends_on('gl')
    depends_on('glu')
    depends_on('libx11')

    depends_on('libpng', when='screenshots=png')
    depends_on('libtiff', when='screenshots=tiff')
    depends_on('freetype', when='+fonts')
    depends_on('fontconfig', when='+fonts')

    def install(self, spec, prefix):

        def yes_no(s):
            return 'YES' if self.spec.satisfies(s) else 'NO'

        mfem_prefix = self.spec['mfem'].prefix
        config_mk_prefix = mfem_prefix
        if spec.satisfies('^mfem@3.3.2', strict=True):
            config_mk_prefix = join_path(config_mk_prefix, 'share', 'mfem')

        args = ['PREFIX={0}'.format(prefix),
                'MFEM_DIR={0}'.format(mfem_prefix),
                'CONFIG_MK={0}'.format(
                    join_path(config_mk_prefix, 'config.mk')),
                'GL_OPTS=-I{0} -I{1}'.format(self.spec['gl'].prefix.include,
                                             self.spec['glu'].prefix.include),
                'GL_LIBS=-L{0} -lx11 -L{1} -lGL -L{2} -lGLU'.format(
                    self.spec['libx11'].prefix.lib,
                    self.spec['gl'].prefix.lib,
                    self.spec['glu'].prefix.lib)]

        args.append('USE_LIBPNG={0}'.format(yes_no('screenshots=png')))
        if self.spec.satisfies('+png'):
            args.append('PNG_OPTS=-DGLVIS_USE_LIBPNG -I{0}'.format(
                spec['libpng'].prefix.include))
            args.append('PNG_LIBS={0}'.format(
                spec['libpng'].libs.ld_flags))

        args.append('USE_LIBTIFF={0}'.format(yes_no('screenshots=tiff')))
        if self.spec.satisfies('+tiff'):
            args.append('TIFF_OPTS=-DGLVIS_USE_LIBTIFF -I{0}'.format(
                spec['libtiff'].prefix.include))
            args.append('TIFF_LIBS={0}'.format(
                spec['libtiff'].libs.ld_flags))

        args.append('USE_FREETYPE={0}'.format(yes_no('+fonts')))
        if self.spec.satisfies('+fonts'):
            args.append('FT_OPTS=-DGLVIS_USE_FREETYPE -I{0} -I{1}'.format(
                spec['freetype'].prefix.include.freetype2,
                spec['fontconfig'].prefix.include))
            args.append('FT_LIBS={0} {1}'.format(
                spec['freetype'].libs.ld_flags,
                spec['fontconfig'].libs.ld_flags))
        make(*args)
        make('install', *args)

        # Before this line, glvis is installed in a bare directory, so make the
        # install prefix tree look like the Filesystem Hierarchy Standard by
        # moving prefix.glvis to prefix.bin.glvis.
        mkdirp(prefix.bin)
        mv = which('mv')
        mv(prefix.glvis, prefix.bin.glvis)
