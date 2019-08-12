# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxfont2(AutotoolsPackage):
    """libXfont provides the core of the legacy X11 font system, handling the
    index files (fonts.dir, fonts.alias, fonts.scale), the various font file
    formats, and rasterizing them.   It is used by the X servers, the
    X Font Server (xfs), and some font utilities (bdftopcf for instance),
    but should not be used by normal X11 clients.  X11 clients access fonts
    via either the new API's in libXft, or the legacy API's in libX11."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXfont"
    url      = "https://www.x.org/archive/individual/lib/libXfont2-2.0.1.tar.gz"

    version('2.0.1', '6ae5ae1f9fb1213b04f14a802a1d721c')

    depends_on('libfontenc')
    depends_on('freetype')

    depends_on('xtrans', type='build')
    depends_on('xproto', type='build')
    depends_on('fontsproto@2.1.3:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
