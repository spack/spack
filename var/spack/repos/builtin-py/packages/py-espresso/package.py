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


class PyEspresso(CMakePackage):
    """ESPResSo is a highly versatile software package for performing and
       analyzing scientific Molecular Dynamics many-particle simulations of
       coarse-grained atomistic or bead-spring models as they are used in
       soft matter research in physics, chemistry and molecular biology. It
       can be used to simulate systems such as polymers, liquid crystals,
       colloids, polyelectrolytes, ferrofluids and biological systems, for
       example DNA and lipid membranes. It also has a DPD and lattice
       Boltzmann solver for hydrodynamic interactions, and allows several
       particle couplings to the LB fluid.
    """
    homepage = "http://espressomd.org/"
    git      = "https://github.com/espressomd/espresso.git"

    version('develop', branch='python')

    depends_on("cmake@3.0:", type='build')
    depends_on("mpi")
    depends_on("boost+serialization+filesystem+system+python+mpi")
    extends("python")
    depends_on("py-cython@0.23:", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("fftw")
