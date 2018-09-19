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
import shutil


class Ghostscript(AutotoolsPackage):
    """An interpreter for the PostScript language and for PDF."""

    homepage = "http://ghostscript.com/"
    url = "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs921/ghostscript-9.21.tar.gz"

    version('9.21', '5f213281761d2750fcf27476c404d17f')
    version('9.18', '33a47567d7a591c00a253caddd12a88a')

    depends_on('pkgconfig', type='build')

    depends_on('freetype@2.4.2:')
    depends_on('jpeg')
    depends_on('lcms')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('zlib')
    depends_on('libxext')

    def url_for_version(self, version):
        baseurl = "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs{0}/ghostscript-{1}.tar.gz"
        return baseurl.format(version.joined, version.dotted)

    def patch(self):
        """Ghostscript comes with all of its dependencies vendored.
        In order to build with Spack versions of these dependencies,
        we have to remove these vendored dependencies.

        Note that this approach is also recommended by Linux from Scratch:
        http://www.linuxfromscratch.org/blfs/view/svn/pst/gs.html
        """
        directories = ['freetype', 'jpeg', 'lcms2', 'libpng', 'zlib']
        for directory in directories:
            shutil.rmtree(directory)

        filter_file('ZLIBDIR=src',
                    'ZLIBDIR={0}'.format(self.spec['zlib'].prefix.include),
                    'configure.ac', 'configure',
                    string=True)

    def configure_args(self):
        return [
            '--disable-compile-inits',
            '--enable-dynamic',
            '--with-system-libtiff',
        ]

    def build(self, spec, prefix):
        make()
        make('so')

    def install(self, spec, prefix):
        make('install')
        make('soinstall')
