# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Stream(MakefilePackage):
    """The STREAM benchmark is a simple synthetic benchmark program that
    measures sustainable memory bandwidth (in MB/s) and the corresponding
    computation rate for simple vector kernels."""

    homepage = "https://www.cs.virginia.edu/stream/ref.html"
    git      = "https://github.com/jeffhammond/STREAM.git"

    version('5.10')

    variant('openmp', default=False, description='Build with OpenMP support')
    variant('STREAM_ARRAY_SIZE', default=2500000000, description='Please note that this is system specific setting, please modify it if you want to compile it with different STREAM ARRAY SIZE other than "2500000000". Currently this variant has effect only with AOCC compiler.General recommendation is that STREAM_ARRAY_SIZE must be at least 4x the size of the sum of all the last-level caches in the system')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')

        # Use the Spack compiler wrappers
        makefile.filter('CC = .*', 'CC = cc')
        makefile.filter('FC = .*', 'FC = f77')

        if self.compiler.name == 'aocc':
            omp_flag = self.compiler.openmp_flag
            array_size = self.spec.variants['STREAM_ARRAY_SIZE'].value
            loc_flags = "-O3 -mcmodel=large -DSTREAM_TYPE=double \
                         -mavx2 -DSTREAM_ARRAY_SIZE={} \
                         -DNTIMES=10 -ffp-contract=fast \
                         -march=znver2 \
                         -fnt-store {}".format(array_size, omp_flag)
            cflags = loc_flags
            fflags = loc_flags
        else:
            cflags = '-O2'
            fflags = '-O2'

        if '+openmp' in self.spec and self.compiler.name != 'aocc':
            cflags += ' ' + self.compiler.openmp_flag
            fflags += ' ' + self.compiler.openmp_flag

        # Set the appropriate flags for this compiler
        makefile.filter('CFLAGS = .*', 'CFLAGS = {0}'.format(cflags))
        makefile.filter('FFLAGS = .*', 'FFLAGS = {0}'.format(fflags))

    def install(self, spec, prefix):
        # Manual installation
        mkdir(prefix.bin)
        install('stream_c.exe', prefix.bin)
        install('stream_f.exe', prefix.bin)
