##############################################################################
# Copyright (c) 2016, Lawrence Livermore National Security, LLC.
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


class Icebin(CMakePackage):
    """Regridding/Coupling library for GCM + Ice Sheet Model"""

    homepage = "https://github.com/citibeth/icebin"
    url         = "https://github.com/citibeth/icebin/tarball/v0.1.0"

    maintainers = ['citibeth']

    version('0.1.5', 'a209c4cd4502b9ded7525ebaa7c6107f')
    version('0.1.4', '5c8ecd778255f2972c0caa3a9f5d82ea')
    version('0.1.3', '98d9b28ef8f8a145a7eed2cb1e92e7e4')
    version('0.1.2', '68673158b46b6e88aea6bc4595444adb')
    version('0.1.1', '986b8b51a2564f9c52156a11642e596c')
    version('0.1.0', '1c2769a0cb3531e4086b885dc7a6fd27')

    version('develop',
        git='https://github.com/citibeth/icebin.git',
        branch='develop')

    variant('python', default=True, description='Build Python extension (requires Python, Numpy)')
    variant('gridgen', default=True, description='Build grid generators (requires CGAL, GMP, MPFR)')
    variant('coupler', default=False, description='Build the GCM couplers (requires MPI)')
    variant('pism', default=False, description='Build coupling link with PISM (requires PISM, PETSc)')
    variant('modele', default=False, description='Build coupling link with ModelE (no exta requirements')
    variant('doc', default=False, description='Build documentation')

    extends('python', when='+python')

    depends_on('everytrace')

    depends_on('python@3:', when='+python')
    depends_on('py-cython', when='+python')
    depends_on('py-numpy', when='+python')

    depends_on('cgal', when='+gridgen')
    depends_on('gmp', when='+gridgen')
    depends_on('mpfr', when='+gridgen')

    depends_on('mpi', when='+coupler')
    depends_on('pism~python', when='+coupler+pism')
    depends_on('petsc', when='+coupler+pism')

    depends_on('boost+filesystem+date_time+mpi')
    depends_on('blitz')
    depends_on('netcdf-cxx4')
    depends_on('ibmisc+proj+blitz+netcdf+boost+udunits2+python')
    depends_on('proj')
    depends_on('eigen')

    depends_on('cmake@3.1:', type='build')
    depends_on('doxygen', type='build', when='+doc')

    # Command line parsing
    depends_on('tclap', when='+modele')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DBUILD_PYTHON=%s' % ('YES' if '+python' in spec else 'NO'),
            '-DBUILD_GRIDGEN=%s' % ('YES' if '+gridgen' in spec else 'NO'),
            '-DBUILD_COUPLER=%s' % ('YES' if '+coupler' in spec else 'NO'),
            '-DBUILD_MODELE=%s' % ('YES' if '+modele' in spec else 'NO'),
            '-DUSE_PISM=%s' % ('YES' if '+pism' in spec else 'NO'),
            '-DBUILD_DOCS=%s' % ('YES' if '+doc' in spec else 'NO')]

    def setup_environment(self, spack_env, run_env):
        """Add <prefix>/bin to the module; this is not the default if we
        extend python."""
        run_env.prepend_path('PATH', join_path(self.prefix, 'bin'))
