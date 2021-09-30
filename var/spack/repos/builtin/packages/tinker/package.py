# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Tinker(MakefilePackage):
    """The Tinker molecular modeling software is a complete and general
       package for molecular mechanics and dynamics, with some special
       features for biopolymers.
    """

    homepage = "https://dasher.wustl.edu/tinker/"
    url      = "https://dasher.wustl.edu/tinker/downloads/tinker-8.7.1.tar.gz"

    version('8.7.1', sha256='0d6eff8bbc9be0b37d62b6fd3da35bb5499958eafe67aa9c014c4648c8b46d0f')

    depends_on('fftw-api@3')
    depends_on('fftw~mpi+openmp', when='^fftw')
    # Needs https://github.com/spack/spack/pull/25461 to be merged first
    # depends_on('armpl threads=openmp', when='^armpl')

    # Just building the OpenMP version (for now) in source directory
    build_directory = 'source'

    def edit(self, spec, prefix):
        # Copy the Makefile in the source folder for editing
        copy(
            join_path(self.stage.source_path, 'make', 'Makefile'),
            join_path(self.stage.source_path, 'source', 'Makefile')
        )

        # Locate the new Makefile for modification
        makefile = FileFilter(join_path('source', 'Makefile'))

        # Need to update directories
        makefile.filter(
            r'^\s*TINKERDIR\s*=.*',
            'TINKERDIR = {0}'.format(self.stage.source_path))
        makefile.filter(
            r'^\s*BINDIR\s*=.*',
            'BINDIR = {0}'.format(self.prefix.bin))

        # Use Spack FFTW - with OpenMP support
        makefile.filter(
            r'^\s*FFTWDIR\s*=.*',
            'FFTWDIR = {0}'.format(spec['fftw-api'].prefix))
        makefile.filter(
            r'^\s*FFTW_LIBS\s*=.*',
            'FFTW_LIBS = {0}'.format(spec['fftw-api:openmp'].libs.ld_flags))
        makefile.filter(
            r'^\s*OPTFLAGS\s*=.*',
            'OPTFLAGS = -O3 {0}'.format(self.compiler.openmp_flag))

        # Set Fortran compiler
        makefile.filter(r'^\s*F77\s*=.*', 'F77 = {0}'.format(spack_f77))

        # Tidy up flags
        makefile.filter(r'^\s*LIBDIR\s*=.*', 'LIBDIR = -L.')
        makefile.filter(r'^\s*RANLIB\s*=.*', 'RANLIB = ranlib')
        makefile.filter(r'^\s*LINKFLAGS\s*=.*', 'LINKFLAGS = $(OPTFLAGS)')

        # Ensure the install directory exists
        mkdir(prefix.bin)
