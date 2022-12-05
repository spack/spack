# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MorphoKit(CMakePackage):
    """Higher-level library for reading / writing morphology files"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/morpho-kit"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/morpho-kit.git"

    submodules = True

    version('develop', branch='main')
    version('0.3.4', tag='v0.3.4')
    version('0.3.3', tag='0.3.3')
    version('0.3.2', tag='v0.3.2')
    version('0.3.1', tag='v0.3.1')
    version('0.3.0', tag='v0.3.0')
    version('0.2.0', tag='v0.2.0')

    depends_on('cmake@3.2:', type='build')
    depends_on('morphio@2.3.9:')
    depends_on('cli11', when='@0.3.3:')      # for utilities
    depends_on('libsonata', when='@0.3.3:')  # for utilities
    depends_on('highfive@2.4.0:', when='@0.3.3:')  # for utilities

    # The HighFive update is needed for paged HDF5 features. Unfortunately, the
    # page buffer is artificially unsupported in pHDF5. Hence, we depend on a
    # particular, patched version of HDF5.
    depends_on('highfive@2.6.0:', when='@0.3.5:')
    depends_on('hdf5@1.12.1:+page_buffer_patch', when='@0.3.5:')

    # MPI is needed for the morphology merger.
    depends_on('mpi', when='@0.3.5:')

    depends_on('boost', when='@0.2.0')

    patch('h5.patch', when='@0.3.2')

    def cmake_args(self):
        return [
            '-DBUILD_BINDINGS:BOOL=OFF',
        ]
