# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Megadock(MakefilePackage, CudaPackage):
    """an ultra-high-performance protein-protein docking for
       heterogeneous supercomputers"""

    homepage = "http://www.bi.cs.titech.ac.jp/megadock/"
    url      = "http://www.bi.cs.titech.ac.jp/megadock/archives/megadock-4.0.3.tgz"

    version('4.0.3', sha256='c1409a411555f4f7b4eeeda81caf622d8a28259a599ea1d2181069c55f257664')

    variant('mpi', description='Enable MPI', default=False)
    variant('cuda', description='Enable CUDA', default=False)

    depends_on('fftw')

    depends_on('mpi', when='+mpi')
    depends_on('cuda', when='+cuda')

    def edit(self, spec, prefix):
        # point cuda samples to cuda prefix
        filter_file('/opt/cuda/6.5/samples', '$(CUDA_INSTALL_PATH)/samples',
                    'Makefile', string=True)

        # sneak link to -lm for sin(), cos()
        filter_file('-o calcrg', '-lm -o calcrg', 'Makefile', string=True)

        # don't force a cuda architecture
        filter_file('-arch=$(SM_VERSIONS) ', '', 'Makefile', string=True)

        # set mpi, cuda installations
        if '+mpi' in spec:
            env['MPICOMPILER'] = self.spec['mpi'].mpicxx

        if '+cuda' in spec:
            env['CUDA_INSTALL_PATH'] = self.spec['cuda'].prefix

        env['FFTW_INSTALL_PATH'] = self.spec['fftw'].prefix
        env['CPPCOMPILER'] = 'c++'

        # use -fopenmp flag if gcc
        if '%gcc' in spec:
            env['OMPFLAG'] = '-fopenmp'

    @property
    def build_targets(self):
        spec = self.spec
        return [
            'USE_GPU=%s' % ('1' if '+cuda' in spec else '0'),
            'USE_MPI=%s' % ('1' if '+mpi' in spec else '0'),
        ]

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        for suffix in ['', '-gpu', '-dp', '-gpu-dp']:
            fn = 'megadock' + suffix
            if os.path.isfile(fn):
                install(fn, prefix.bin)
