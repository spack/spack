# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ImageMagick(AutotoolsPackage):
    """ImageMagick is a software suite to create, edit, compose,
    or convert bitmap images."""

    homepage = "http://www.imagemagick.org"
    url = "https://github.com/ImageMagick/ImageMagick/archive/7.0.2-7.tar.gz"

    version('7.0.5-9', '0bcde35180778a61367599e46ff40cb4')
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

    def configure_args(self):
        spec = self.spec
        gs_font_dir = join_path(spec['ghostscript-fonts'].prefix.share, "font")
        return [
            '--with-gs-font-dir={0}'.format(gs_font_dir)
        ]
