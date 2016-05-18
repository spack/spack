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
    Scalable Library for Eigenvalue Computations.
    """

    homepage = "http://www.grycap.upv.es/slepc"
    url = "http://slepc.upv.es/download/download.php?filename=slepc-3.6.2.tar.gz"

    version('3.6.2', '2ab4311bed26ccf7771818665991b2ea3a9b15f97e29fd13911ab1293e8e65df')

    variant('arpack', default=False, description='Enables Arpack wrappers')

    depends_on('petsc')
    depends_on('arpack-ng~mpi',when='+arpack^petsc~mpi')
    depends_on('arpack-ng+mpi',when='+arpack^petsc+mpi')

    def install(self, spec, prefix):
        # set SLEPC_DIR for installation
        os.environ['SLEPC_DIR'] = self.stage.source_path

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
        #FIXME:
        # make('test')
        make('install')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # set up SLEPC_DIR for everyone using SLEPc package
        spack_env.set('SLEPC_DIR', self.prefix)
