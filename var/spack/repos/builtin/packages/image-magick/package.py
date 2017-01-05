##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class ImageMagick(Package):
    """ImageMagick is a software suite to create, edit, compose,
    or convert bitmap images."""

    homepage = "http://www.imagemagick.org"
    url = "https://github.com/ImageMagick/ImageMagick/archive/7.0.2-7.tar.gz"

    version('7.0.2-7', 'c59cdc8df50e481b2bd1afe09ac24c08')
    version('7.0.2-6', 'aa5689129c39a5146a3212bf5f26d478')

    depends_on('jpeg')
    depends_on('pango')
    depends_on('libtool', type='build')
    depends_on('libpng')
    depends_on('freetype')
    depends_on('fontconfig')
    depends_on('libtiff')
    depends_on('ghostscript')
    depends_on('ghostscript-fonts')

    def url_for_version(self, version):
        return "https://github.com/ImageMagick/ImageMagick/archive/{0}.tar.gz".format(version)

    def install(self, spec, prefix):
        gs_font_dir = join_path(spec['ghostscript-fonts'].prefix.share, "font")
        configure('--prefix={0}'.format(prefix),
                  '--with-gs-font-dir={0}'.format(gs_font_dir))
        make()
        make('check')
        make('install')
