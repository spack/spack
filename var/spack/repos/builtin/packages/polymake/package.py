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


class Polymake(Package):
    """polymake is open source software for research in polyhedral geometry"""
    homepage = "https://polymake.org/doku.php"
    url      = "https://polymake.org/lib/exe/fetch.php/download/polymake-3.0r1.tar.bz2"

    version('3.0r2', '08584547589f052ea50e2148109202ab')
    version('3.0r1', '63ecbecf9697c6826724d8a041d2cac0')

    # Note: Could also be built with nauty instead of bliss

    depends_on("bliss")
    depends_on("boost")
    depends_on("cddlib")
    depends_on("gmp")
    depends_on("lrslib")
    depends_on("mpfr")
    depends_on("ppl")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-bliss=%s" % spec["bliss"].prefix,
                  "--with-boost=%s" % spec["boost"].prefix,
                  "--with-cdd=%s" % spec["cddlib"].prefix,
                  "--with-gmp=%s" % spec["gmp"].prefix,
                  "--with-lrs=%s" % spec["lrslib"].prefix,
                  "--with-mpfr=%s" % spec["mpfr"].prefix,
                  "--with-ppl=%s" % spec["ppl"].prefix)
        make()
        make("install")
