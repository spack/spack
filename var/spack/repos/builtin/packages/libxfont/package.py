# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxfont(AutotoolsPackage):
    """libXfont provides the core of the legacy X11 font system, handling the
    index files (fonts.dir, fonts.alias, fonts.scale), the various font file
    formats, and rasterizing them.   It is used by the X servers, the
    X Font Server (xfs), and some font utilities (bdftopcf for instance),
    but should not be used by normal X11 clients.  X11 clients access fonts
    via either the new API's in libXft, or the legacy API's in libX11."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXfont"
    url      = "https://www.x.org/archive/individual/lib/libXfont-1.5.2.tar.gz"

    version('1.5.2', 'e8c616db0e59df4614980915e79bb05e')

    depends_on('libfontenc')
    depends_on('freetype')

    depends_on('xtrans', type='build')
    depends_on('xproto', type='build')
    depends_on('fontsproto@2.1.3:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
