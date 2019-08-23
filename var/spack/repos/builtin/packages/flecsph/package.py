# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install flecsph-git
#
# You can edit this file again by typing:
#
#     spack edit flecsph-git
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Flecsph(CMakePackage):
    """FleCSPH is a multi-physics compact application that exercises FleCSI 
    parallel data structures for tree-based particle methods. In particular, 
    FleCSPH implements a smoothed-particle hydrodynamics (SPH) solver for 
    the solution of Lagrangian problems in astrophysics and cosmology. FleCSPH 
    includes support for gravitational forces using the fast multipole method 
    (FMM)."""

    homepage = "http://flecsi.lanl.com"
    git      = "https://github.com/laristra/flecsph.git"

    version('develop',branch='master',submodules=True)
    
    depends_on('cmake@3.1:', type='build')
    depends_on('boost@1.59.0: cxxstd=11 +program_options')
    depends_on('mpi')
    depends_on('hdf5@1.10.5 +mpi')
    depends_on('flecsi@flecsph backend=mpi')
    depends_on('gsl')

    def cmake_args(self):
        options = ['-DCMAKE_BUILD_TYPE=debug']
        options.append('-DENABLE_MPI=ON') 
        options.append('-DENABLE_OPENMP=ON')
        options.append('-DENABLE_CLOG=ON')
        options.append('-DCXX_CONFORMANCE_STANDARD=c++17')
        return options  
