# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Hdf5VolExternalPassthrough(CMakePackage):
    """Package for HDF5 external pass-through VOL."""

    homepage = "https://sdm.lbl.gov/"
    url      = "https://github.com/hpc-io/vol-external-passthrough/archive/refs/tags/v1.0.tar.gz"
    git      = "https://github.com/hpc-io/vol-external-passthrough.git"
    maintainers = ['hyoklee']

    version('develop', branch='develop')
    version('1.0', sha256='99a06d1c31451f8f0c8c10fec112410cda1f951f0eda1bd0ca999d6b35cf7740')
    depends_on('hdf5@1.13.0:')

    def cmake_args(self):
        args = [
            self.define('BUILD_SHARED_LIBS:BOOL', True),
            self.define('BUILD_TESTING:BOOL=ON', self.run_tests)
        ]
        return args
