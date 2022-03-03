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

    # Problem size variants
    variant('max_conc', default='4', values=('4', '8', '10', '15', '20'),
            description="Set internal maximum number of species")
    variant('max_external_field', default='4', values=('4', '8', '10', '15', '20'),
            description="Set internal maximum number of external fields")
    variant('max_prob_var', default='15', values=('10', '15', '20', '25', '28', '34', '40', '46', '64'),
            description="Set internal maximum number of active equations")
    variant('mde', default='27', values=('8', '9', '10', '16', '20', '27', '54'),
            description="Set internal maximum DOF per element")

    # Floating point checks
    variant('check_finite', default=True, description="Enable finite computation check")
    variant('fpe', default=False, description="Enable floating point exception")

    # Optional third party libraries
    variant('arpack-ng', default=True, description="Build with ARPACK support")
    variant('metis', default=True, description="Build with metis decomposition")
    variant('omega-h', default=True, description="Build with Omega_h support")
    variant('petsc', default=True, description="Build with PETSc solver support")
    variant('sparse', default=True, description="Build with legacy sparse solver")
    variant('suite-sparse', default=True, description="Build with UMFPACK support")

    # Required dependencies
    depends_on('mpi')
    depends_on('seacas+applications')
    depends_on('trilinos+mpi+epetra+aztec+amesos+stratimikos+teko+mumps+superlu-dist+ml~exodus')

    # Optional dependencies
    depends_on('arpack-ng', when='+arpack-ng')
    depends_on('metis', when='+metis')
    depends_on('omega-h+mpi', when='+omega-h')
    depends_on('petsc+hypre+mpi~exodusii', when='+petsc')
    depends_on('sparse', when='+sparse')
    depends_on('suite-sparse', when='+suite-sparse')

    def cmake_args(self):
        args = []

        # Problem sizes
        args.append(self.define_from_variant('MAX_CONC', 'max_conc'))
        args.append(
            self.define_from_variant('MAX_EXTERNAL_FIELD', 'max_external_field'))
        args.append(self.define_from_variant('MAX_PROB_VAR', 'max_prob_var'))
        args.append(self.define_from_variant('MDE', 'mde'))

        # Floating point error checks
        args.append(self.define_from_variant('CHECK_FINITE', 'check_finite'))
        args.append(self.define_from_variant('FP_EXCEPT', 'fpe'))

        # Configure optional libraries
        args.append(self.define_from_variant('ENABLE_ARPACK', 'arpack-ng'))
        args.append(self.define_from_variant('ENABLE_OMEGA_H', 'omega-h'))
        args.append(self.define_from_variant('ENABLE_PETSC', 'petsc'))
        args.append(self.define_from_variant('ENABLE_SPARSE', 'sparse'))
        args.append(self.define_from_variant('ENABLE_METIS', 'metis'))
        args.append(self.define_from_variant('ENABLE_UMFPACK', 'suite-sparse'))

        return args
