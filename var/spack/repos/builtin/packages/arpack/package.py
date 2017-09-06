##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Arpack(Package):
    """A collection of Fortran77 subroutines designed to solve large scale
    eigenvalue problems."""

    homepage = "http://www.caam.rice.edu/software/ARPACK/"
    url      = "http://www.caam.rice.edu/software/ARPACK/SRC/arpack96.tar.gz"

    version('96', 'fffaa970198b285676f4156cebc8626e')

    depends_on('blas')
    depends_on('lapack')

    def patch(self):
        makefile = FileFilter('ARmake.inc')

        # Section 1: Paths and Libraries

        # Change the build directory
        makefile.filter('^home.*', 'home = %s' % os.getcwd())

        # Use external BLAS/LAPACK
        makefile.filter('^BLASdir.*',
                        'BLASdir = %s'   % self.spec['blas'].prefix)
        makefile.filter('^LAPACKdir.*',
                        'LAPACKdir = %s' % self.spec['lapack'].prefix)

        # Do not include the platform in the library name
        makefile.filter('^PLAT.*', 'PLAT = ')
        makefile.filter('^ARPACKLIB.*', 'ARPACKLIB = $(home)/libarpack.a')

        # Section 2: Compilers

        # Be sure to use the Spack compiler wrapper
        makefile.filter('^FC.*', 'FC = {0}'.format(os.environ['F77']))
        makefile.filter(
            '^FFLAGS.*', 'FFLAGS = -O2 -g {0}'.format(self.compiler.pic_flag)
        )

        if not which('ranlib'):
            makefile.filter('^RANLIB.*', 'RANLIB = touch')

    def install(self, spec, prefix):
        with working_dir('SRC'):
            make('all')

        mkdir(prefix.lib)
        install('libarpack.a', prefix.lib)
