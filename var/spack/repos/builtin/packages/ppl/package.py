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


class Ppl(Package):
    """The Parma Polyhedra Library (PPL) provides numerical
    abstractions especially targeted at applications in the field of
    analysis and verification of complex systems. These abstractions
    include convex polyhedra, some special classes of polyhedra shapes
    that offer interesting complexity/precision tradeoffs, and grids
    which represent regularly spaced points that satisfy a set of
    linear congruence relations. The library also supports finite
    powersets and products of polyhedra and grids, a mixed integer
    linear programming problem solver using an exact-arithmetic
    version of the simplex algorithm, a parametric integer programming
    solver, and primitives for termination analysis via the automatic
    synthesis of linear ranking functions."""

    homepage = "http://bugseng.com/products/ppl/"
    url      = "http://bugseng.com/products/ppl/download/ftp/releases/1.1/ppl-1.1.tar.gz"

    version('1.1', '4f2422c0ef3f409707af32108deb30a7')

    depends_on("gmp")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-gmp=%s" % spec['gmp'].prefix)
        make()
        make("install")
