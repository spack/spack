# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Swfft(MakefilePackage):
    """A stand-alone version of HACC's distributed-memory, pencil-decomposed,
    parallel 3D FFT."""

    homepage = "https://xgitlab.cels.anl.gov/hacc/SWFFT"
    url      = "https://xgitlab.cels.anl.gov/api/v4/projects/hacc%2FSWFFT/repository/archive.tar.gz?sha=v1.0"
    git      = "https://xgitlab.cels.anl.gov/hacc/SWFFT.git"

    version('1.0', '0fbc34544b97ba9c3fb19ef2d7a0f076')
    version('develop', branch='master')

    depends_on('mpi')
    depends_on('fftw')

    tags = ['proxy-app', 'ecp-proxy-app']

    @property
    def build_targets(self):
        targets = []
        spec = self.spec

        targets.append('DFFT_MPI_CC=%s' % spec['mpi'].mpicc)
        targets.append('DFFT_MPI_CXX=%s' % spec['mpi'].mpicxx)
        targets.append('DFFT_MPI_F90=%s' % spec['mpi'].mpifc)

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('build/CheckDecomposition', prefix.bin)
        install('build/TestDfft', prefix.bin)
