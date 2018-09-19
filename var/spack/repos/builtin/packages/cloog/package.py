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


class Cloog(Package):
    """CLooG is a free software and library to generate code for
    scanning Z-polyhedra. That is, it finds a code (e.g. in C,
    FORTRAN...) that reaches each integral point of one or more
    parameterized polyhedra."""

    homepage = "http://www.cloog.org"
    url      = "http://www.bastoul.net/cloog/pages/download/count.php3?url=./cloog-0.18.1.tar.gz"
    list_url = "http://www.bastoul.net/cloog/pages/download"

    version('0.18.1', 'e34fca0540d840e5d0f6427e98c92252')
    version('0.18.0', 'be78a47bd82523250eb3e91646db5b3d')
    version('0.17.0', '0aa3302c81f65ca62c114e5264f8a802')

    depends_on("gmp")
    depends_on("isl")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-osl=no",
                  "--with-isl=%s" % spec['isl'].prefix,
                  "--with-gmp=%s" % spec['gmp'].prefix)
        make()
        make("install")
