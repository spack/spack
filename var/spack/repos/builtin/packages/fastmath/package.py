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
