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


class Bliss(Package):
    """bliss: A Tool for Computing Automorphism Groups and Canonical
    Labelings of Graphs"""

    homepage = "http://www.tcs.hut.fi/Software/bliss/"
    url = "http://www.tcs.hut.fi/Software/bliss/bliss-0.73.zip"

    version('0.73', '72f2e310786923b5c398ba0fc40b42ce')

    # Note: Bliss can also be built without gmp, but we don't support this yet

    depends_on("gmp")
    depends_on("libtool", type='build')

    patch("Makefile.spack.patch")

    def install(self, spec, prefix):
        # The Makefile isn't portable; use our own instead
        makeargs = ["-f", "Makefile.spack",
                    "PREFIX=%s" % prefix, "GMP_PREFIX=%s" % spec["gmp"].prefix]
        make(*makeargs)
        make("install", *makeargs)
