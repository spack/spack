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


class PyCvxopt(PythonPackage):
    """CVXOPT is a free software package for convex optimization based on the
    Python programming language."""

    homepage = "http://cvxopt.org/"
    url      = "https://pypi.io/packages/source/c/cvxopt/cvxopt-1.1.9.tar.gz"

    import_modules = ['cvxopt']

    version('1.1.9', 'a56e7b23d76c2b5aaf3bea2a7c245ea7')

    variant('gsl',   default=False, description='Use GSL random number generators for constructing random matrices')
    variant('fftw',  default=False, description='Install the cvxopt.fftw interface to FFTW')
    variant('glpk',  default=False, description='Enable support for the linear programming solver GLPK')
    # variant('mosek', default=False, description='Enable support for the linear, second-order cone, and quadratic programming solvers in MOSEK')  # noqa: flake8
    variant('dsdp',  default=False, description='Enable support for the semidefinite programming solver DSDP')

    # Required dependencies
    depends_on('python@2.7:')
    depends_on('py-setuptools', type='build')
    depends_on('blas')
    depends_on('lapack')
    depends_on('suite-sparse')

    # Optional dependencies
    depends_on('gsl',       when='+gsl')
    depends_on('fftw',      when='+fftw')
    depends_on('glpk',      when='+glpk')
    # depends_on('mosek@8:',  when='+mosek')
    depends_on('dsdp@5.8:', when='+dsdp')

    def setup_environment(self, spack_env, run_env):
        spec = self.spec

        # BLAS/LAPACK Libraries

        # Default names of BLAS and LAPACK libraries
        spack_env.set('CVXOPT_BLAS_LIB', ';'.join(spec['blas'].libs.names))
        spack_env.set('CVXOPT_LAPACK_LIB', ';'.join(spec['lapack'].libs.names))

        # Directory containing BLAS and LAPACK libraries
        spack_env.set('CVXOPT_BLAS_LIB_DIR', spec['blas'].libs.directories[0])

        # SuiteSparse Libraries

        # Directory containing SuiteSparse libraries
        spack_env.set('CVXOPT_SUITESPARSE_LIB_DIR',
                      spec['suite-sparse'].libs.directories[0])

        # Directory containing SuiteSparse header files
        spack_env.set('CVXOPT_SUITESPARSE_INC_DIR',
                      spec['suite-sparse'].headers.directories[0])

        # GSL Libraries

        if '+gsl' in spec:
            spack_env.set('CVXOPT_BUILD_GSL', 1)

            # Directory containing libgsl
            spack_env.set('CVXOPT_GSL_LIB_DIR',
                          spec['gsl'].libs.directories[0])

            # Directory containing the GSL header files
            spack_env.set('CVXOPT_GSL_INC_DIR',
                          spec['gsl'].headers.directories[0])
        else:
            spack_env.set('CVXOPT_BUILD_GSL', 0)

        # FFTW Libraries

        if '+fftw' in spec:
            spack_env.set('CVXOPT_BUILD_FFTW', 1)

            # Directory containing libfftw3
            spack_env.set('CVXOPT_FFTW_LIB_DIR',
                          spec['fftw'].libs.directories[0])

            # Directory containing fftw.h
            spack_env.set('CVXOPT_FFTW_INC_DIR',
                          spec['fftw'].headers.directories[0])
        else:
            spack_env.set('CVXOPT_BUILD_FFTW', 0)

        # GLPK Libraries

        if '+glpk' in spec:
            spack_env.set('CVXOPT_BUILD_GLPK', 1)

            # Directory containing libglpk
            spack_env.set('CVXOPT_GLPK_LIB_DIR',
                          spec['glpk'].libs.directories[0])

            # Directory containing glpk.h
            spack_env.set('CVXOPT_GLPK_INC_DIR',
                          spec['glpk'].headers.directories[0])
        else:
            spack_env.set('CVXOPT_BUILD_GLPK', 0)

        # DSDP Libraries

        if '+dsdp' in spec:
            spack_env.set('CVXOPT_BUILD_DSDP', 1)

            # Directory containing libdsdp
            spack_env.set('CVXOPT_DSDP_LIB_DIR',
                          spec['dsdp'].libs.directories[0])

            # Directory containing dsdp5.h
            spack_env.set('CVXOPT_DSDP_INC_DIR',
                          spec['dsdp'].headers.directories[0])

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        """Test that the installation was successful."""
        python('-m', 'unittest', 'discover', '-s', 'tests')
