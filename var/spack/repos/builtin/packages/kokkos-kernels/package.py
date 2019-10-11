# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class KokkosKernels(MakefilePackage):
    """Kokkos C++ Performance Portability Programming EcoSystem: Math Kernels -
    Provides BLAS, Sparse BLAS and Graph Kernels."""

    homepage = "https://github.com/kokkos/kokkos-kernels"
    url      = "https://github.com/kokkos/kokkos-kernels/archive/2.7.00.tar.gz"

    version('2.7.00', 'dfb21f26da9f1f976d84826a1510d91e')
    version('2.6.00', 'ef8ba7509d82417dbc82a2f021886949')
    version('2.5.00', '94f4bd78b36b9c53c18df3ccfd552041')
    version('develop', git='https://github.com/kokkos/kokkos-kernels',
            branch='develop')

    # make sure kokkos kernels version matches kokkos
    depends_on('kokkos@2.5.00', when='@2.5.00')
    depends_on('kokkos@2.6.00', when='@2.6.00')
    depends_on('kokkos@2.7.00', when='@2.7.00')
    depends_on('kokkos@develop', when='@develop')

    patch('makefile.patch')

    def edit(self, spec, prefix):
        makefile = FileFilter("src/Makefile")
        makefile.filter('CXX = .*', 'CXX = ' + env['CXX'])

    def build(self, spec, prefix):
        with working_dir('build', create=True):
            makefile_path = '%s%s' % (self.stage.source_path, '/src/Makefile')
            copy(makefile_path, 'Makefile')
            make_args = [
                'KOKKOSKERNELS_INSTALL_PATH=%s' % prefix,
                'KOKKOSKERNELS_PATH=%s' % self.stage.source_path,
                'KOKKOS_PATH=%s' % spec['kokkos'].prefix
            ]

            make('build', *make_args)

    def install(self, spec, prefix):
        with working_dir('build', create=False):
            make_args = [
                'KOKKOSKERNELS_INSTALL_PATH=%s' % prefix,
                'KOKKOSKERNELS_PATH=%s' % self.stage.source_path,
                'KOKKOS_PATH=%s' % spec['kokkos'].prefix
            ]
            make('install', *make_args)
