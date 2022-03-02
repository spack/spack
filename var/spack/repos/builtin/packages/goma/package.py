# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Goma(CMakePackage):
    """A Full-Newton Finite Element Program for Free and Moving Boundary Problems with
       Coupled Fluid/Solid Momentum, Energy, Mass, and Chemical Species Transport """

    homepage = "https://www.gomafem.com"
    url = "https://github.com/goma/goma/archive/v7.0.0.tar.gz"
    git = "https://github.com/goma/goma.git"

    maintainers = ['wortiz']

    version('7.0.0', commit='5166896f273e5853e1f32885e20f68317b24979c')
    version('main', branch='main')
    version('develop', branch='develop')

    variant('MDE', default=27, description="Set internal maximum DOF per element")
    variant('MAX_PROB_VAR', default=15, description="Set internal maximum number of active equations")
    variant('MAX_CONC', default=4, description="Set internal maximum number of species")
    variant('MAX_EXTERNAL_FIELD', default=4, description="Set internal maximum number of external fields")

    variant('sparse', default=True, description="Build with legacy sparse solver")
    variant('metis', default=True, description="Build with metis decomposition")
    variant('petsc', default=True, description="Build with PETSc solver support")
    variant('omega-h', default=True, description="Build with Omega_h support")
    variant('suite-sparse', default=True, description="Build with UMFPACK support")
    variant('arpack-ng', default=True, description="Build with ARPACK support")

    depends_on('mpi')
    depends_on('sparse', when='+sparse')
    depends_on('metis', when='+metis')
    depends_on('trilinos+mpi+epetra+aztec+amesos+stratimikos+teko+mumps+superlu-dist~exodus')
    depends_on('petsc+hypre~exodusii+mpi', when='+petsc')
    depends_on('omega-h+mpi', when='+omega-h')
    depends_on('suite-sparse', when='+suite-sparse')
    depends_on('arpack-ng', when='+arpack-ng')
    depends_on('seacas+applications')

    def cmake_args(self):
        spec = self.spec

        args = []
        args.extend([
            '-DMDE=%s' % spec.variants['MDE'].value,
            '-DMAX_CONC=%s' % spec.variants['MAX_CONC'].value,
            '-DMAX_PROB_VAR=%s' % spec.variants['MAX_PROB_VAR'].value,
            '-DMAX_EXTERNAL_FIELD=%s' % spec.variants['MAX_EXTERNAL_FIELD'].value
        ])

        args.extend([
            '-DTrilinos_DIR=%s' % spec['trilinos'].prefix
        ])

        if '+petsc' in spec:
            args.extend([
                '-DENABLE_PETSC=ON'
            ])
        else:
            args.extend([
                '-DENABLE_PETSC=OFF'
            ])

        if '+metis' in spec:
            args.extend([
                '-DMETIS_PREFIX=%s' % spec['metis'].prefix
            ])
        else:
            args.extend([
                '-DENABLE_METIS=OFF'
            ])

        if '+suite-sparse' in spec:
            args.extend([
                '-DUMFPACK_DIR=%s' % spec['suite-sparse'].prefix
            ])
        else:
            args.extend([
                '-DENABLE_UMFPACK=OFF'
            ])

        if '+sparse' in spec:
            args.extend([
                '-DSparse_PREFIX=%s' % spec['sparse'].prefix
            ])
        else:
            args.extend([
                '-DENABLE_SPARSE=OFF'
            ])

        if '+omega-h' in spec:
            args.extend([
                '-DOmega_h_DIR=%s' % spec['omega-h'].prefix
            ])
        else:
            args.extend([
                '-DENABLE_OMEGA_H=OFF'
            ])

        if '+arpack-ng' in spec:
            args.extend([
                '-DARPACK_PREFIX=%s' % spec['arpack-ng'].prefix
            ])
        else:
            args.extend([
                '-DENABLE_ARPACK=OFF'
            ])

        return args
