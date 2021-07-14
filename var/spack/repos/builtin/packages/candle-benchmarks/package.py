# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CandleBenchmarks(Package):
    """ECP-CANDLE Benchmarks"""

    homepage = "https://github.com/ECP-CANDLE/Benchmarks"
    url      = "https://github.com/ECP-CANDLE/Benchmarks/archive/v0.1.tar.gz"

    tags = ['proxy-app', 'ecp-proxy-app']
    git = "https://github.com/ECP-CANDLE/Benchmarks.git"
    version('master', branch='master')
    version('0.1', tag='v0.1')
    version('0.2', tag='v0.2')
    version('0.3', tag='v0.3')

    # version('0.1', sha256='767f74f43ee3a5d4e0f26750f2a96b8433e25a9cd4f2d29938ac8acf263ab58d')
    # version('0.2', sha256='0e5e4ca2648f5318180276a13a9712d182d074d011e7f0ee7171bf7668bc21a1')
    # version('0.3', sha256='6309173e56ae4d2dfba8ff879fd19fba70bbba77be2291892f8191a94f4e4470')

    variant('mpi', default=True, description='Build with MPI support')

    extends('python')
    depends_on('python@2.7:')
    depends_on('opencv@3.2.0: +core +imgproc +jpeg +png +tiff -dnn ~eigen ~gtk')

    depends_on('py-astropy', type=('build', 'run'))
    depends_on('py-h5py~mpi', when='~mpi', type=('build', 'run'))
    depends_on('py-h5py+mpi', when='+mpi', type=('build', 'run'))
    depends_on('py-keras', type=('build', 'run'))
    depends_on('py-mdanalysis', type=('build', 'run'))
    depends_on('py-mpi4py', when='+mpi', type=('build', 'run'))
    depends_on('py-matplotlib +image@:2.2.3', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-numba', type=('build', 'run'))
    depends_on('py-patsy', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))
    depends_on('py-statsmodels', type=('build', 'run'))
    depends_on('py-theano +cuda', type=('build', 'run'))
    depends_on('py-tqdm', type=('build', 'run'))
    depends_on('py-torch', type=('build', 'run'))
    depends_on('py-tensorflow+cuda', type=('build', 'run'))






    # see #3244, but use external for now
    # depends_on('tensorflow')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix.bin)
