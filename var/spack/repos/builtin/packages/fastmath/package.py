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
from spack import *
import os


class Fastmath(MakefilePackage):
    """FASTMath is a suite of ~15 numerical libraries frequently used together
    in various SciDAC and CSE applications. The suite includes discretization
    libraries for structured, AMR and unstructured grids as well as solver
    libraries for ODE's, Time Integrators, Iterative, Non-Linear, and Direct
    Solvers."""

    homepage = "www.fastmath-scidac.org/"

    version('1.0', 'cd5006bbe9a39c1bf252b9b8b5e5bdcd')

    depends_on('boxlib dims=3')  # how do we say 3D boxlib?
    depends_on('chombo')
    depends_on('hypre~internal-superlu')
    depends_on('mesquite')
#    depends_on('ml-trilinos')  # hoping for stripped down install of just ml
#    depends_on('nox-trilinos')  # hoping for stripped down install of just nox
    depends_on('moab')
    depends_on('mpi')
    depends_on('parpack')  # we need parpack ng
    depends_on('petsc')
    depends_on('phasta')
    depends_on('pumi')
    depends_on('sundials')
    depends_on('superlu-dist')
    depends_on('trilinos')
    depends_on('zoltan')

    def url_for_version(self, version):
        return "file://%s/fastmath.tar.gz" % os.getcwd()
