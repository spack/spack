# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fiat(CMakePackage):
    """FIAT (Fortran IFS and Arpege Toolkit) is a collection of selected
    Fortran utility libraries, extracted from the IFS/Arpege model."""

    homepage = "https://github.com/ecmwf-ifs/fiat"
    git = "https://github.com/ecmwf-ifs/fiat.git"

    maintainers = ['climbfuji']

    version('develop', branch='develop', no_cache=True, preferred=True)
    version('main', branch='main', no_cache=True, preferred=False)

    variant('mpi', default=True, description='Use MPI?')
    variant('openmp', default=True, description='Use OpenMP?')
    variant('fckit', default=True, description='Use fckit?')
    #variant('dr_hook_multi_precision_handles', default=False,
    #    description='Use deprecated single precision handles for DR_HOOK?')
    #variant('warnings', default=True, description='Enable compiler warnings')

    depends_on('ecbuild', type=('build'))
    depends_on('mpi', when='+mpi')
    depends_on('eckit', when='+fckit')
    depends_on('fckit', when='+fckit')

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_OMP', 'openmp'),
            self.define_from_variant('ENABLE_MPI', 'mpi'),
            self.define_from_variant('ENABLE_FCKIT', 'fckit')
            #self.define_from_variant('ENABLE_DR_HOOK_MULTI_PRECISION_HANDLES',
            #   'dr_hook_multi_precision_handles')
            #self.define_from_variant('ENABLE_WARNINGS, 'warnings')
        ]

        return args
