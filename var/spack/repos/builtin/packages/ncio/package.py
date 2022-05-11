# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class Ncio(CMakePackage):
    """This is a library used by NCEP GSI system to read the GFS forecast
    files for use in data assimilation.

    This is part of NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-ncio"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-ncio/archive/refs/tags/v1.0.0.tar.gz"

    maintainers = ['edwardhartnett', 'kgerheiser', 'Hang-Lei-NOAA']

    version('1.1.0', sha256='9de05cf3b8b1291010197737666cede3d621605806379b528d2146c4f02d08f6')
    version('1.0.0', sha256='2e2630b26513bf7b0665619c6c3475fe171a9d8b930e9242f5546ddf54749bd4')

    depends_on('mpi')
    depends_on('netcdf-fortran')

    def setup_run_environment(self, env):
        lib = find_libraries('libncio', root=self.prefix, shared=False, recursive=True)
        env.set('NCIO_LIB', lib[0])
        env.set('NCIO_INC', join_path(self.prefix, 'include'))
        env.set('NCIO_LIBDIR', lib[0])
