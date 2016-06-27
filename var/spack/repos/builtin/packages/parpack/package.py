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
import os
import shutil

class Parpack(Package):
    """ARPACK is a collection of Fortran77 subroutines designed to solve large
       scale eigenvalue problems."""

    homepage = "http://www.caam.rice.edu/software/ARPACK/download.html"
    url      = "http://www.caam.rice.edu/software/ARPACK/SRC/parpack96.tar.Z"

    version('96', 'a175f70ff71837a33ff7e4b0b6054f43')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')

    def patch(self):
        # Filter the CJ makefile to make a spack one.
        shutil.move('ARMAKES/ARmake.CJ', 'ARmake.inc')
        mf = FileFilter('ARmake.inc')

        # Be sure to use Spack F77 wrapper
        mf.filter('^FC.*',     'FC = f77')
        mf.filter('^FFLAGS.*', 'FFLAGS = -O2 -g')

        # Set up some variables.
        mf.filter('^PLAT.*',      'PLAT = ')
        mf.filter('^home.*',      'home = %s' % os.getcwd())
        mf.filter('^BLASdir.*',   'BLASdir = %s' % self.spec['blas'].prefix)
        mf.filter('^LAPACKdir.*', 'LAPACKdir = %s' % self.spec['lapack'].prefix)
        mf.filter('^MAKE.*',      'MAKE = make')

        # build the library in our own prefix.
        mf.filter('^ARPACKLIB.*', 'PARPACKLIB = %s/libparpack.a' % os.getcwd())


    def install(self, spec, prefix):
        with working_dir('PARPACK/SRC/MPI'):
            make('all')

        mkdirp(prefix.lib)
        install('libparpack.a', prefix.lib)
