# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fastmath(Package):
    """FASTMath is a suite of ~15 numerical libraries frequently used together
    in various SciDAC and CSE applications. The suite includes discretization
    libraries for structured, AMR and unstructured grids as well as solver
    libraries for ODE's, Time Integrators, Iterative, Non-Linear, and Direct
    Solvers."""

    homepage = "www.fastmath-scidac.org/"
    url = "https://github.com/citibeth/dummy/tarball/v1.0"

    version('1.0', 'e2b724dfcc31d735897971db91be89ff')

    # BundlePackage
    depends_on('boxlib dims=3')
    depends_on('chombo@3.2')
    depends_on('hypre~internal-superlu')
    depends_on('mesquite')
#    depends_on('ml-trilinos')  # hoping for stripped down install of just ml
#    depends_on('nox-trilinos')  # hoping for stripped down install of just nox
    depends_on('moab')
    depends_on('mpi')
    depends_on('arpack-ng')
    depends_on('petsc')
    depends_on('phasta')
    depends_on('pumi')
    depends_on('sundials')
    depends_on('superlu-dist')
    depends_on('trilinos')
    depends_on('zoltan')

    # Dummy install for now,  will be removed when metapackage is available
    def install(self, spec, prefix):
        # Prevent the error message
        #      ==> Error: Install failed for fastmath.  Nothing was installed!
        #      ==> Error: Installation process had nonzero exit code : 256
        with open(join_path(spec.prefix, 'bundle-package.txt'), 'w') as out:
            out.write('This is a bundle\n')
            out.close()
