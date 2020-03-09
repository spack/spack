# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Globalarrays(AutotoolsPackage):
    """Global Arrays (GA) is a Partitioned Global Address Space (PGAS)
    programming model. It provides primitives for one-sided communication
    (Get, Put, Accumulate) and Atomic Operations (read increment).
    It supports blocking and non-blocking primtives, and supports location
    consistency."""

    homepage = "http://hpc.pnl.gov/globalarrays/"
    url = "https://github.com/GlobalArrays/ga/releases/download/v5.7/ga-5.7.tar.gz"

    version('5.7',   sha256='3ed1ab47adfda7bceb7beca12fc05a2e1631732f0e55bbaf9036dad4e3da4774')
    version('5.6.5', sha256='17a7111dfe67d44cf0888c7b79abd48bf4968874f26b3f16cce9fd04e2c72bb9')
    version('5.6.4', sha256='3daf742053502755c0b581041a56f8f7086af05980c7146d194b0fd6526ee14f')
    version('5.6.3', sha256='e8818825d4f72c8433f416a9ae2bba203a521e9bc73d80f96c2250deaef4bc40')
    version('5.6.2', sha256='3eb1c92d41235f3386e0215f04aaab1aae30a2bce191f9fb6436b2cd8b9544ba')
    version('5.6.1', sha256='b324deed49f930f55203e1d18294ce07dd02680b9ac0728ebc54f94a12557ebc')
    version('5.6',   sha256='a228dfbae9a6cfaae34694d7e56f589ac758e959b58f4bc49e6ef44058096767')

    variant('int64', default=False, description='Compile with 64 bit indices support')
    variant('blas', default=False, description='Enable BLAS')
    variant('lapack', default=False, description='Enable LAPACK')
    variant('scalapack', default=False, description='Enable SCALAPACK')
    variant('armci', values=('mpi-ts', 'mpi-pr', 'mpi3', 'openib', 'ofi'),
            default='mpi-ts', description='ARMCI runtime')

    depends_on('mpi')
    depends_on('blas', when='+blas')
    depends_on('lapack', when='+lapack')
    depends_on('scalapack', when='+scalapack')

    conflicts('+lapack', when='~blas')
    conflicts('+scalapack', when='~blas')
    conflicts('+scalapack', when='~lapack')

    def configure_args(self):
        args = ['--with-mpi']

        if '+blas' in self.spec:
            if '+int64' in self.spec:
                args.append('--with-blas8')
            else:
                args.append('--with-blas')

        if '+lapack' in self.spec:
            args.append('--with-lapack')

        if '+scalapack' in self.spec:
            if '+int64' in self.spec:
                args.append('--with-scalapack8')
            else:
                args.append('--with-scalapack')

        args.append('--with-' + self.spec.variants['armci'].value)

        return args
