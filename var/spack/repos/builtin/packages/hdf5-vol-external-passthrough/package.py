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

    patch('CMakeLists.patch',
          sha256='09876179329cbc7d925055c714cabe05511ba7a9a8e9d5e029cc9acfdac5ffa7')

    def cmake_args(self):
        """Populate cmake arguments for HDF5 DAOS."""

        args = [
            '-DBUILD_SHARED_LIBS:BOOL=ON',
            '-DBUILD_TESTING:BOOL=ON'
        ]
        return args
