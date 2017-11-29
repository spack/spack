##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Siesta(Package):
    """SIESTA performs electronic structure calculations and ab initio molecular
       dynamics simulations of molecules and solids."""

    homepage = "https://departments.icmab.es/leem/siesta/"
    url      = "https://launchpad.net/siesta/4.0/4.0.1/+download/siesta-4.0.1.tar.gz"

    version('4.0.1', '5cb60ce068f2f6e84fa9184ffca94c08')

    patch('configure.patch')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')
    depends_on('netcdf')
    depends_on('netcdf-fortran')

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):
        sh = which('sh')
        configure_args = ['--enable-mpi',
                          '--with-blas=%s' % spec['blas'].libs,
                          '--with-lapack=%s' % spec['lapack'].libs,
                          # need to include BLAS below because Intel MKL's
                          # BLACS depends on BLAS, otherwise the compiler
                          # test fails
                          '--with-blacs=%s' % (spec['scalapack'].libs +
                                               spec['blas'].libs),
                          '--with-scalapack=%s' % spec['scalapack'].libs,
                          '--with-netcdf=%s' % (spec['netcdf-fortran'].libs +
                                                spec['netcdf'].libs),
                          # need to specify MPIFC explicitly below, otherwise
                          # Intel's mpiifort is not found
                          'MPIFC=%s' % spec['mpi'].mpifc
                          ]
        with working_dir('Obj'):
            sh('../Src/configure', *configure_args)
            sh('../Src/obj_setup.sh')
        with working_dir('Obj_trans', create=True):
            sh('../Src/configure', *configure_args)
            sh('../Src/obj_setup.sh')

    def build(self, spec, prefix):
        with working_dir('Obj'):
            make(parallel=False)
        with working_dir('Obj_trans'):
            make('transiesta', parallel=False)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        with working_dir('Obj'):
            install('siesta', prefix.bin)
        with working_dir('Obj_trans'):
            install('transiesta', prefix.bin)
