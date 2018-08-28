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


class Cblas(Package):
    """The BLAS (Basic Linear Algebra Subprograms) are routines that
       provide standard building blocks for performing basic vector and
       matrix operations."""

    homepage = "http://www.netlib.org/blas/_cblas/"

    # tarball has no version, but on the date below, this MD5 was correct.
    version('2015-06-06', '1e8830f622d2112239a4a8a83b84209a',
            url='http://www.netlib.org/blas/blast-forum/cblas.tgz')

    depends_on('blas')
    parallel = False

    def patch(self):
        mf = FileFilter('Makefile.in')

        mf.filter('^BLLIB =.*', 'BLLIB = {0}'.format(
                  ' '.join(self.spec['blas'].libs.libraries)))
        mf.filter('^CC =.*', 'CC = cc')
        mf.filter('^FC =.*', 'FC = fc')

    def install(self, spec, prefix):
        make('all')
        mkdirp(prefix.lib)
        mkdirp(prefix.include)

        # Rename the generated lib file to libcblas.a
        install('lib/cblas_LINUX.a', prefix.lib.join('libcblas.a'))
        install('include/cblas.h', prefix.include)
        install('include/cblas_f77.h', prefix.include)
