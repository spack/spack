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


class Glvis(MakefilePackage):
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

    version('develop', git='https://github.com/glvis/glvis', branch='master')

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
            values=('xwd', 'png', 'tiff'),
            description='Backend used for screenshots')
    variant('fonts', default=True,
            description='Use antialiased fonts via freetype & fontconfig')

    depends_on('mfem@develop', when='@develop')
    depends_on('mfem@3.3', when='@3.3')
    depends_on('mfem@3.2', when='@3.2')
    depends_on('mfem@3.1', when='@3.1')

    depends_on('gl')
    depends_on('glu')
    depends_on('libx11')

    depends_on('libpng', when='screenshots=png')
    depends_on('libtiff', when='screenshots=tiff')
    depends_on('freetype', when='+fonts')
    depends_on('fontconfig', when='+fonts')

    def edit(self, spec, prefix):

        def yes_no(s):
            return 'YES' if self.spec.satisfies(s) else 'NO'

        mfem = spec['mfem']
        config_mk = mfem.package.config_mk

        pkgs_libs = [('glu', 'libGLU'), ('gl', 'libGL'), ('libx11', 'libX11')]
        search_dirs = ['lib64', 'lib']
        gl_libs = LibraryList([])
        for pkg, lib in pkgs_libs:
            for dir in search_dirs:
                lib = find_libraries([lib], join_path(spec[pkg].prefix, dir),
                                     shared=True, recursive=False)
                if lib:
                    break
            if not lib:
                raise InstallError('Library \'%s\' not found' % lib)
            gl_libs += lib

        args = ['CC={0}'.format(env['CC']),
                'PREFIX={0}'.format(prefix.bin),
                'MFEM_DIR={0}'.format(mfem.prefix),
                'CONFIG_MK={0}'.format(config_mk),
                'GL_OPTS=-I{0} -I{1} -I{2}'.format(
                    spec['libx11'].prefix.include,
                    spec['gl'].prefix.include,
                    spec['glu'].prefix.include),
                'GL_LIBS={0}'.format(gl_libs.ld_flags)]

        if 'screenshots=png' in spec:
            args += [
                'USE_LIBPNG=YES', 'USE_LIBTIFF=NO',
                'PNG_OPTS=-DGLVIS_USE_LIBPNG -I{0}'.format(
                    spec['libpng'].prefix.include),
                'PNG_LIBS={0}'.format(spec['libpng'].libs.ld_flags)]
        elif 'screenshots=tiff' in spec:
            args += [
                'USE_LIBPNG=NO', 'USE_LIBTIFF=YES',
                'TIFF_OPTS=-DGLVIS_USE_LIBTIFF -I{0}'.format(
                    spec['libtiff'].prefix.include),
                'TIFF_LIBS={0}'.format(spec['libtiff'].libs.ld_flags)]
        else:
            args += ['USE_LIBPNG=NO', 'USE_LIBTIFF=NO']

        args.append('USE_FREETYPE={0}'.format(yes_no('+fonts')))
        if '+fonts' in spec:
            args += [
                'FT_OPTS=-DGLVIS_USE_FREETYPE -I{0} -I{1}'.format(
                    spec['freetype'].prefix.include.freetype2,
                    spec['fontconfig'].prefix.include),
                'FT_LIBS={0} {1}'.format(
                    spec['freetype'].libs.ld_flags,
                    spec['fontconfig'].libs.ld_flags)]

        self.build_targets = args
        self.install_targets += args
