# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hdf5VolExternalPassthrough(CMakePackage):
    """Package for HDF5 external pass-through VOL."""

    homepage = "https://sdm.lbl.gov/"
    git      = "https://github.com/hpc-io/vol-external-passthrough.git"
    maintainers = ['hyoklee']

    version('default', branch='develop')
    depends_on('hdf5@develop-1.13')

    def cmake_args(self):
        """Populate cmake arguments for HDF5 DAOS."""
        args = [
            self.define('BUILD_SHARED_LIBS:BOOL', True),
            self.define('BUILD_TESTING:BOOL=ON', self.run_tests)
        ]
        return args
