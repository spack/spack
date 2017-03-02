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
import os
from spack import *


class Slepc(Package):
    """
    Scalable Library for Eigenvalue Problem Computations.
    """

    homepage = "http://www.grycap.upv.es/slepc"
    url = "http://slepc.upv.es/download/download.php?filename=slepc-3.6.2.tar.gz"

    version('3.7.3', '3ef9bcc645a10c1779d56b3500472ceb66df692e389d635087d30e7c46424df9')
    version('3.7.1', '670216f263e3074b21e0623c01bc0f562fdc0bffcd7bd42dd5d8edbe73a532c2')
    version('3.6.3', '384939d009546db37bc05ed81260c8b5ba451093bf891391d32eb7109ccff876')
    version('3.6.2', '2ab4311bed26ccf7771818665991b2ea3a9b15f97e29fd13911ab1293e8e65df')

    variant('arpack', default=True, description='Enables Arpack wrappers')

    # NOTE: make sure PETSc and SLEPc use the same python.
    depends_on('python@2.6:2.7', type='build')
    depends_on('petsc@3.7:', when='@3.7.1:')
    depends_on('petsc@3.6.3:3.6.4', when='@3.6.2:3.6.3')
    depends_on('arpack-ng~mpi', when='+arpack^petsc~mpi~int64')
    depends_on('arpack-ng+mpi', when='+arpack^petsc+mpi~int64')

    patch('install_name_371.patch', when='@3.7.1')

    def install(self, spec, prefix):
        if spec.satisfies('+arpack^petsc+int64'):
            raise RuntimeError('Arpack can not be used with 64bit integers.')

        # set SLEPC_DIR for installation
        # Note that one should set the current (temporary) directory instead
        # its symlink in spack/stage/ !
        os.environ['SLEPC_DIR'] = os.getcwd()

        options = []

        if '+arpack' in spec:
            options.extend([
                '--with-arpack-dir=%s' % spec['arpack-ng'].prefix.lib,
            ])
            if 'arpack-ng~mpi' in spec:
                options.extend([
                    '--with-arpack-flags=-larpack'
                ])
            else:
                options.extend([
                    '--with-arpack-flags=-lparpack,-larpack'
                ])

        configure('--prefix=%s' % prefix, *options)

        make('MAKE_NP=%s' % make_jobs, parallel=False)
        if self.run_tests:
            make('test', parallel=False)

        make('install', parallel=False)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # set up SLEPC_DIR for everyone using SLEPc package
        spack_env.set('SLEPC_DIR', self.prefix)
