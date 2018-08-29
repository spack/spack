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


class Clapack(MakefilePackage):
    """CLAPACK is a f2c'ed version of LAPACK.

       The CLAPACK library was built using a Fortran to C conversion utility
    called f2c.  The entire Fortran 77 LAPACK library is run through f2c to
    obtain C code, and then modified to improve readability.  CLAPACK's goal
    is to provide LAPACK for someone who does not have access to a Fortran
    compiler."""

    homepage = "http://www.netlib.org/clapack/"
    url      = "http://www.netlib.org/clapack/clapack.tgz"

    version('3.2.1', '040da31f3a7d4fbc9ac376c748d18d1f')

    variant('external-blas', default=True,
            description='Build with external BLAS (ATLAS here).')

    depends_on('atlas', when='+external-blas')

    def edit(self, spec, prefix):
        copy('make.inc.example', 'make.inc')
        if '+external-blas' in spec:
            make_inc = FileFilter('make.inc')
            make_inc.filter(r'^BLASLIB.*',
                            'BLASLIB = ../../libcblaswr.a -lcblas -latlas')
            makefile = FileFilter('Makefile')
            makefile.filter(r'^lib.*',
                            'lib: variants lapacklib tmglib')

    def build(self, spec, prefix):
        make('f2clib')
        make('cblaswrap' if '+external-blas' in spec else 'blaslib')
        make('lib')

    def install(self, spec, prefix):
        install_tree('.', prefix)
