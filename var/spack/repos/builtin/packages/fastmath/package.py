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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install fastmath
#
# You can edit this file again by typing:
#
#     spack edit fastmath
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import os
from os.path import join as pjoin

class Fastmath(Package):
    """FASTMath is a suite of ~15 numerical libraries frequently used together
    in various SciDAC and CSE applications. The suite includes discretization
    libraries for structured, AMR and unstructured settings as well as solver
    libraries for ODE's, Time Integrators, Iterative, Non-Linear, and Direct
    Solvers."""

    homepage = "www.fastmath-scidac.org/"

    version('1.0', 'bf5b7a996baebe97d6bf1801604a7e7b')

    depends_on('boxlib') # how do we say 3D boxlib?
#    depends_on('boxlib+dims=3') # how do we say 3D boxlib?
#    depends_on('chombo')
    depends_on('hypre~internal-superlu')
#    depends_on('mesquite')
#    depends_on('ml-from-trilinos')
#    depends_on('nox-from-trilinos')
    depends_on('moab')
    depends_on('mpi')
    depends_on('parpack') # we need parpack ng
    depends_on('petsc')
#    depends_on('phasta')
#    depends_on('pumi')
    depends_on('sundials')
    depends_on('superlu-dist')
    depends_on('zoltan')

    def url_for_version(self, version):
        print __file__
        dummy_tar_path =  os.path.abspath(pjoin(os.path.split(__file__)[0]))
        dummy_tar_path = pjoin(dummy_tar_path,"fastmath.tar.gz")
        url      = "file://" + dummy_tar_path
        return url

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install')
