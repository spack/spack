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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install maple
#
# You can edit this file again by typing:
#
#     spack edit maple
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Maple(Package):
    """Maple: this software makes it possible to work on numerical quantities
(integer, real, complex) as well as with polynomials, functions, series.

Maple can derive, integrate and solve linear equation systems. It can invert
matrices and perform asymptotic expansions and resolutions of differential
equations in symbolic form. The Maple system also offers numerous functions
in numerical arithmetic and in combinatorics.

Maple is an interpreted language."""

    homepage = "https://www.maplesoft.com/products/Maple/"
    url      = "fakeurl.tar.gz"

    version('2017')

    def install(self, spec, prefix):
        pass

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', '/ssoft/spack/external/Maple/2017/bin')
        run_env.prepend_path('LD_LIBRARY_PATH',
                             '/ssoft/spack/external/Maple/2017/lib')
        run_env.prepend_path('MANPATH', '/ssoft/spack/external/Maple/2017/man')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        pass
