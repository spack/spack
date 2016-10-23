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

class Glint2(CMakePackage):
    """Regridding/Coupling library for GCM + Ice Sheet Model"""

    homepage = "https://github.com/citibeth/icebin"
    url         = "https://github.com/citibeth/icebin/tarball/v0.1.0"

    version('0.1.0', '1c2769a0cb3531e4086b885dc7a6fd27')
    version('glint2', git='https://github.com/citibeth/icebin.git', branch='glint2')

    variant('python', default=True, description='Build Python extension (requires Python, Numpy)')
    variant('coupler', default=True, description='Build the GCM coupler (requires MPI)')
    variant('pism', default=False, description='Build coupling link with PISM (requires PISM, PETSc)')

    extends('python', when='+python')

#    depends_on('everytrace+fortran', when='~coupler')
    depends_on('everytrace+mpi+fortran')

    depends_on('python@3:', when='+python')
    depends_on('py-cython', when='+python')
    depends_on('py-numpy', when='+python')

    depends_on('cgal')
    depends_on('gmp')
    depends_on('mpfr')

    depends_on('mpi', when='+coupler')
    depends_on('pism@glint2~python', when='+coupler+pism')
    depends_on('petsc@3.4.5~superlu-dist', when='+coupler+pism')

    depends_on('boost+filesystem+date_time')
    depends_on('blitz')
    depends_on('netcdf-cxx')
    depends_on('netcdf-fortran')
    depends_on('proj')
    depends_on('eigen')
    depends_on('galahad')

    # Build dependencies
    depends_on('cmake', type='build')
    depends_on('doxygen', type='build')


    # Dummy dependency to work around Spack bug
    depends_on('openblas')

    def configure_args(self):
        spec = self.spec
        return [
            '-DUSE_PYTHON=%s' % ('YES' if '+python' in spec else 'NO'),
            '-DUSE_PISM=%s' % ('YES' if '+pism' in spec else 'NO'),
            '-DUSE_EVERYTRACE=YES',
            '-DPETSC_DIR=%s' % spec['petsc'].prefix]

    def setup_environment(self, spack_env, env):
        """Add <prefix>/bin to the module; this is not the default if we
        extend python."""
        env.prepend_path('PATH', join_path(self.prefix, 'bin'))
