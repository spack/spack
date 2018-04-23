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
import os


class Dsdp(MakefilePackage):
    """The DSDP software is a free open source implementation of an
    interior-point method for semidefinite programming. It provides primal and
    dual solutions, exploits low-rank structure and sparsity in the data, and
    has relatively low memory requirements for an interior-point method. It
    allows feasible and infeasible starting points and provides approximate
    certificates of infeasibility when no feasible solution exists."""

    homepage = "http://www.mcs.anl.gov/hs/software/DSDP/"
    url      = "http://www.mcs.anl.gov/hs/software/DSDP/DSDP5.8.tar.gz"

    version('5.8', '37c15a3c6c3f13e31262f65ac4364b5e')

    depends_on('blas')
    depends_on('lapack')

    patch('malloc.patch')

    build_targets = ['dsdpapi']

    def edit(self, spec, prefix):
        make_include = FileFilter('make.include')

        # STEP 1: Set DSDPROOT.
        make_include.filter('^#DSDPROOT.*=.*',
                            'DSDPROOT = {0}'.format(os.getcwd()))

        # STEP 2: Set the name of the C compiler.
        make_include.filter('^CC.*=.*', 'CC = {0}'.format(spack_cc))

        # STEP 5:
        # Location of BLAS AND LAPACK libraries.
        # Also include the math library and other libraries needed to
        # link the BLAS to the C files that call them.
        lapackblas = spec['lapack'].libs + spec['blas'].libs
        make_include.filter('^LAPACKBLAS.*=.*',
                            'LAPACKBLAS = {0}'.format(
                                lapackblas.link_flags + ' -lm'))

    def install(self, spec, prefix):
        # Manual installation
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
