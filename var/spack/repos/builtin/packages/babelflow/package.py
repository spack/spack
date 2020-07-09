# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Babelflow(CMakePackage):
    """BabelFlow is an Embedded Domain Specific Language to describe
       algorithms using a task graph abstraction which allows them to be 
       executed on top of one of several available runtime systems."""

    homepage = "https://github.com/sci-visus/BabelFlow"
    url      = "https://github.com/sci-visus/BabelFlow/archive/ascent.zip"

    maintainers = ['spetruzza']

    version('develop',
            git='https://github.com/sci-visus/BabelFlow.git',
            branch='ascent',
            commit='62e0eae8b2ff28094ec03f0c2496e579dda794ab',
            submodules=True,
            preferred=True)

    depends_on('mpi')

    variant("shared", default=True, description="Build Babelflow as shared libs")

    def cmake_args(self):
      args = []

      #args.append('-DMPI_C_COMPILER='+self.spec['mpi'].mpicc)
      #args.append('-DMPI_CXX_COMPILER='+self.spec['mpi'].mpicxx)

      return args
  
    def cmake_install(self, spec, prefix):
        #print(cmake_cache_entry("MPI_C_COMPILER",spec['mpi'].mpicc))
        
        if "+shared" in spec:
            cmake_args.append('-DBUILD_SHARED_LIBS=ON')
        else:
            cmake_args.append('-DBUILD_SHARED_LIBS=OFF')
            
        make()
        make('install')
