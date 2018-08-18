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
import os
import sys
from spack import *


class Slepc(Package):
    """Scalable Library for Eigenvalue Problem Computations."""

    homepage = "http://www.grycap.upv.es/slepc"
    url      = "http://slepc.upv.es/download/distrib/slepc-3.6.2.tar.gz"
    git      = "https://bitbucket.org/slepc/slepc.git"

    version('develop', branch='master')
    version('3.9.1', 'e174ea7c127d9161eef976b0288f0c56d443a58d6ab2dc8af1e8bd66f156ce17')
    version('3.9.0', '1f3930db56b4065aaf214ea758ddff1a70bf19d45544cbdfd19d2787db4bfe0b')
    version('3.8.2', '1e7d20d20eb26da307d36017461fe4a55f40e947e232739179dbe6412e22ed13')
    version('3.8.0', 'c58ccc4e852d1da01112466c48efa41f0839649f3a265925788237d76cd3d963')
    version('3.7.4', '2fb782844e3bc265a8d181c3c3e2632a4ca073111c874c654f1365d33ca2eb8a')
    version('3.7.3', '3ef9bcc645a10c1779d56b3500472ceb66df692e389d635087d30e7c46424df9')
    version('3.7.1', '670216f263e3074b21e0623c01bc0f562fdc0bffcd7bd42dd5d8edbe73a532c2')
    version('3.6.3', '384939d009546db37bc05ed81260c8b5ba451093bf891391d32eb7109ccff876')
    version('3.6.2', '2ab4311bed26ccf7771818665991b2ea3a9b15f97e29fd13911ab1293e8e65df')

    variant('arpack', default=True, description='Enables Arpack wrappers')
    variant('blopex', default=False, description='Enables BLOPEX wrappers')

    # NOTE: make sure PETSc and SLEPc use the same python.
    depends_on('python@2.6:2.8', type='build')
    # Cannot mix release and development versions of SLEPc and PETSc:
    depends_on('petsc@develop', when='@develop')
    depends_on('petsc@3.9:3.9.99', when='@3.9:3.9.99')
    depends_on('petsc@3.8:3.8.99', when='@3.8:3.8.99')
    depends_on('petsc@3.7:3.7.7', when='@3.7.1:3.7.4')
    depends_on('petsc@3.6.3:3.6.4', when='@3.6.2:3.6.3')
    depends_on('arpack-ng~mpi', when='+arpack^petsc~mpi~int64')
    depends_on('arpack-ng+mpi', when='+arpack^petsc+mpi~int64')

    patch('install_name_371.patch', when='@3.7.1')

    # Arpack can not be used with 64bit integers.
    conflicts('+arpack', when='^petsc+int64')

    resource(name='blopex',
             url='http://slepc.upv.es/download/external/blopex-1.1.2.tar.gz',
             sha256='0081ee4c4242e635a8113b32f655910ada057c59043f29af4b613508a762f3ac',
             destination=join_path('installed-arch-' + sys.platform + '-c-opt',
                                   'externalpackages'),
             when='+blopex')

    def install(self, spec, prefix):
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

        # It isn't possible to install BLOPEX separately and link to it;
        # BLOPEX has to be downloaded with SLEPc at configure time
        if '+blopex' in spec:
            options.append('--download-blopex')

        configure('--prefix=%s' % prefix, *options)

        make('MAKE_NP=%s' % make_jobs, parallel=False)
        if self.run_tests:
            make('test', parallel=False)

        make('install', parallel=False)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # set up SLEPC_DIR for everyone using SLEPc package
        spack_env.set('SLEPC_DIR', self.prefix)
