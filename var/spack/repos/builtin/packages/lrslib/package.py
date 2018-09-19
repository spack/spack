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


class Lrslib(Package):
    """lrslib Ver 6.2 is a self-contained ANSI C implementation of the
    reverse search algorithm for vertex enumeration/convex hull
    problems and comes with a choice of three arithmetic packages"""
    homepage = "http://cgm.cs.mcgill.ca/~avis/C/lrs.html"
    url      = "http://cgm.cs.mcgill.ca/~avis/C/lrslib/archive/lrslib-062.tar.gz"

    version('6.2', 'be5da7b3b90cc2be628dcade90c5d1b9')
    version('6.1', '0b3687c8693cd7d1f234a3f65e147551')
    version('6.0', 'd600a2e62969ad03f7ab2f85f1b3709c')
    version('5.1', 'cca323eee8bf76f598a13d7bf67cc13d')
    version('4.3', '86dd9a45d20a3a0069f77e61be5b46ad')

    # Note: lrslib can also be built with Boost, and probably without gmp

    # depends_on("boost")
    depends_on("gmp")
    depends_on("libtool", type="build")

    patch("Makefile.spack.patch")

    def url_for_version(self, version):
        url = "http://cgm.cs.mcgill.ca/~avis/C/lrslib/archive/lrslib-0{0}.tar.gz"
        return url.format(version.joined)

    def install(self, spec, prefix):
        # The Makefile isn't portable; use our own instead
        makeargs = ["-f", "Makefile.spack",
                    "PREFIX=%s" % prefix,
                    # "BOOST_PREFIX=%s" % spec["boost"].prefix,
                    "GMP_PREFIX=%s" % spec["gmp"].prefix]
        make(*makeargs)
        make("install", *makeargs)
