# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Librom(CMakePackage):
    """libROM is a free, lightweight, scalable C++ library for data-driven
       physical simulation methods from the intrusive projection-based reduced
       order models to non-intrusive black-box approaches."""

    homepage = "https://github.com/LLNL/libROM"
    git      = "https://github.com/LLNL/libROM.git"

    maintainers = ['chldkdtn']

    version('develop', branch='master')
    variant('mfem', default=False, description="Enable MFEM support.")
    variant('shared', default=True,
            description="Enables the build of shared libraries.")

    depends_on('lapack')
    depends_on('scalapack')
    depends_on('mpi')
    depends_on('hypre@develop', when='+mfem')
    depends_on('metis', when='+mfem')
    depends_on('parmetis', when='+mfem')
    depends_on('mfem@develop', when='+mfem')
    depends_on('hdf5@1.8.12')
    depends_on('zlib')

    def cmake_args(self):
        args = []
        if self.spec.variants['mfem'].value:  # True if +mfem
            args = ['-DUSE_MFEM=On']
        if not self.spec.variants['shared'].value:
            args = ['-DBUILD_STATIC=On']
        return args

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        install(join_path(self.build_directory, 'lib', 'libROM.so'),
                prefix.lib)

        mkdirp(prefix.include)
        install_tree('lib', prefix.include)

        mkdirp(prefix.bin)
        install_tree(join_path(self.build_directory, 'tests'),
                     join_path(prefix.bin, 'tests'))
        if self.spec.variants['mfem'].value:  # True if +mfem
            install_tree(join_path(self.build_directory, 'examples'),
                         join_path(prefix.bin, 'examples'))
