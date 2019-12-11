# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import sys
import os

class Libnetworkit(Package):
    """NetworKit is a growing open-source toolkit for large-scale network analysis. Its aim is to provide tools for the analysis of large networks in the size range from thousands to billions of edges. For this purpose, it implements efficient graph algorithms, many of them parallel to utilize multicore architectures. These are meant to compute standard measures of network analysis, such as degree sequences, clustering coefficients, and centrality measures. In this respect, NetworKit is comparable to packages such as NetworkX, albeit with a focus on parallelism and scalability."""

    homepage = "https://networkit.github.io/"
    git      = "https://github.com/networkit/networkit.git"
    version('6.0', tag='6.0', submodules=True)

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('gtest', default=False, description='Enables the build with gtest support')
    variant('doc', default=False, description='Enables the build with sphinx documentation')

    depends_on('cmake', type='build')
    depends_on('git', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('py-sphinx', when='+doc', type='build')

    @when('@6.0')
    def install(self, spec, prefix):
        source_directory = self.stage.source_path
        build_directory = join_path(source_directory, 'build')

        options = std_cmake_args[:]
        
        if '+gtest' in spec:
            options.append('-DNETWORKIT_BUILD_TESTS=ON')

        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make('install')

            # install headers
            source_folder_base = join_path(source_directory, 'networkit/cpp')
            source_folders = ['.',
                    'algebraic',
                    'algebraic/algorithms',
                    'auxiliary',
                    'base',
                    'centrality',
                    'clique',
                    'coarsening',
                    'community',
                    'components',
                    'correlation',
                    'distance',
                    'dynamics',
                    'edgescores',
                    'flow',
                    'generators',
                    'generators/quadtree',
                    'geometric',
                    'global',
                    'graph',
                    'independentset',
                    'io',
                    'layout',
                    'linkprediction',
                    'matching',
                    'numerics',
                    'numerics/LAMG',
                    'overlap',
                    'randomization',
                    'scd',
                    'scoring',
                    'simulation',
                    'sparsification',
                    'structures',
                    'viz']
            networkit_dist = join_path(prefix.include, 'networkit')
            mkdirp(networkit_dist)

            for folder in source_folders:
                header_folder = join_path(source_folder_base, folder)
                headers = glob.glob(join_path(header_folder, '*.hpp'))
                for hfile in headers:
                    mkdirp(join_path(networkit_dist, folder))
                    install(hfile, join_path(networkit_dist, folder))


    @property
    def libs(self):
        return find_libraries(['libnetworkit'], root=self.prefix.lib)

