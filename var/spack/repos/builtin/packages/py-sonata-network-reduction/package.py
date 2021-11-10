# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySonataNetworkReduction(PythonPackage):
    """Pythonic Sonata circuit reduction API"""

    homepage = "https://bbpgitlab.epfl.ch/nse/sonata-network-reduction/"
    git      = "git@bbpgitlab.epfl.ch:nse/sonata-network-reduction.git"

    version('develop', branch='master')
    version('0.1.8', tag='sonata-network-reduction-v0.1.8')
    version('0.1.7', tag='sonata-network-reduction-v0.1.7')
    version('0.1.0', tag='sonata-network-reduction-v0.1.0')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-numpy@1.14:1.99', type='run')
    depends_on('py-h5py@3.0.0:4.99', type='run', when='@0.1.3:')
    depends_on('py-h5py@2.3:2.99', type='run', when='@:0.1.2')
    depends_on('py-pandas@0.25:1.99', type='run')
    depends_on('py-tqdm@4.34:4.99', type='run')
    depends_on('py-lxml@4.3.4:4.99', type='run', when='@:0.1.2')
    depends_on('py-dask', type='run', when='@0.1.2:')
    depends_on('py-dask-mpi', type='run', when='@0.1.2:')
    depends_on('py-distributed@2.0:2.21', type='run', when='@0.1.2:')
    depends_on('py-bluepyopt@1.8.68:1.999', type='run')
    depends_on('py-joblib@0.14:0.99', type='run', when='@:0.1.1')
    depends_on('py-bglibpy@4.3:4.999', type='run')
    depends_on('py-bluepysnap@0.5.2:0.99', type='run')
    depends_on('neuron+python', type='run')
    depends_on('py-neuron-reduce@0.0.8:0.99', type='run')
    depends_on('py-morphio@3.0.0:3.999', type='run', when='@0.1.2:')
    depends_on('py-morphio@2.3.9:2.999', type='run', when='@:0.1.0')
    depends_on('py-neurom@1.4.18:1.5.99', type='run', when='@:0.1.2')
    depends_on('py-morph-tool@0.2.7:2.99', type='run')
    depends_on('py-click@6.7:7.99', type='run')
    depends_on('py-aibs-circuit-converter@0.0.3:0.99', type='run')
    depends_on('py-pyyaml@5.3:5.99', type='run')

    def setup_run_environment(self, env):
        env.set('NEURON_INIT_MPI', "0")
        env.unset('PMI_RANK')
