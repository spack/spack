##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

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
