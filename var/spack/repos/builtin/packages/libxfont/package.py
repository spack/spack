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
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('util-macros', type='build')
