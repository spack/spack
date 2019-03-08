# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class GhostscriptFonts(Package):
    """Ghostscript Fonts"""

    homepage = "http://ghostscript.com/"
    url = "https://www.imagemagick.org/download/delegates/ghostscript-fonts-std-8.11.tar.gz"

    version('8.11', '6865682b095f8c4500c54b285ff05ef6')

    def install(self, spec, prefix):
        fdir = join_path(prefix.share, 'font')
        mkdirp(fdir)
        files = glob.glob('*')
        for f in files:
            if not f.startswith('spack-build'):
                install(f, fdir)
