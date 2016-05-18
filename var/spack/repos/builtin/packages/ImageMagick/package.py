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


class Imagemagick(Package):
    """ImageMagick is a image processing library"""
    homepage = "http://www.imagemagic.org"

    # -------------------------------------------------------------------------
    # ImageMagick does not keep around anything but *-10 versions, so
    # this URL may change.  If you want the bleeding edge, you can
    # uncomment it and see if it works but you may need to try to
    # fetch a newer version (-6, -7, -8, -9, etc.) or you can stick
    # wtih the older, stable, archived -10 versions below.
    #
    # TODO: would be nice if spack had a way to recommend avoiding a
    # TODO: bleeding edge version, but not comment it out.
    # -------------------------------------------------------------------------
    # version('6.9.0-6', 'c1bce7396c22995b8bdb56b7797b4a1b',
    # url="http://www.imagemagick.org/download/ImageMagick-6.9.0-6.tar.bz2")

    # -------------------------------------------------------------------------
    # *-10 versions are archived, so these versions should fetch reliably.
    # -------------------------------------------------------------------------
    version(
        '6.8.9-10',
        'aa050bf9785e571c956c111377bbf57c',
        url="http://sourceforge.net/projects/imagemagick/files/old-sources/6.x/6.8/ImageMagick-6.8.9-10.tar.gz/download")

    depends_on('jpeg')
    depends_on('libtool')
    depends_on('libpng')
    depends_on('freetype')
    depends_on('fontconfig')
    depends_on('libtiff')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
