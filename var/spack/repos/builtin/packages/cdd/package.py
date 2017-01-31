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


class Cdd(Package):
    """The program cdd+ (cdd, respectively) is a C++ (ANSI C)
    implementation of the Double Description Method [MRTT53] for
    generating all vertices (i.e. extreme points) and extreme rays of
    a general convex polyhedron given by a system of linear
    inequalities"""
    homepage = "https://www.inf.ethz.ch/personal/fukudak/cdd_home/cdd.html"
    url      = "http://www.cs.mcgill.ca/~fukuda/download/cdd/cdd-061a.tar.gz"

    version('0.61a', '22c24a7a9349dd7ec0e24531925a02d9')

    depends_on("libtool", type="build")

    patch("Makefile.spack.patch")

    def url_for_version(self, version):
        url = "http://www.cs.mcgill.ca/~fukuda/download/cdd/cdd-{0}.tar.gz"
        return url.format(version.joined)

    def install(self, spec, prefix):
        # The Makefile isn't portable; use our own instead
        makeargs = ["-f", "Makefile.spack", "PREFIX=%s" % prefix]
        make(*makeargs)
        make("install", *makeargs)
