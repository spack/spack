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

# TODO: Add support for a C++11 enabled installation that filters out the
# TODO: "C++11-Disabled" flag (but only if the spec compiler supports C++11).

# TODO: Add support for parallel installation that uses MPI.

# TODO: Create installation options for NetCDF that support larger page size
# TODO: suggested by Exodus (see the repository "README" file).

class Exodusii(Package):
    """Exodus II is a C++/Fortran library developed to store and retrieve data for
       finite element analyses. It's used for preprocessing (problem definition),
       postprocessing (results visualization), and data transfer between codes.
       An Exodus II data file is a random access, machine independent, binary
       file that is written and read via C, C++, or Fortran API routines."""

    homepage = "https://github.com/gsjaardema/seacas"
    url      = "https://github.com/gsjaardema/seacas/archive/master.zip"

    version('2016-02-08', git='https://github.com/gsjaardema/seacas.git', commit='dcf3529')

    # TODO: Make this a build dependency once build dependencies are supported
    # (see: https://github.com/LLNL/spack/pull/378).
    depends_on('cmake@2.8.7:')
    depends_on('hdf5~shared~mpi')
    depends_on('netcdf~mpi')

    patch('exodus-cmake.patch')

    def patch(self):
        ff = FileFilter('cmake-exodus')

        ff.filter('CMAKE_INSTALL_PREFIX:PATH=${ACCESS}',
            'CMAKE_INSTALL_PREFIX:PATH=%s' % self.spec.prefix, string=True)
        ff.filter('NetCDF_DIR:PATH=${TPL}',
            'NetCDF_DIR:PATH=%s' % self.spec['netcdf'].prefix, string=True)
        ff.filter('HDF5_ROOT:PATH=${TPL}',
            'HDF5_ROOT:PATH=%s' % self.spec['hdf5'].prefix, string=True)

    def install(self, spec, prefix):
        mkdirp('build')
        cd('build')

        cmake_exodus = Executable('../cmake-exodus')
        cmake_exodus()

        make()
        make('install')
