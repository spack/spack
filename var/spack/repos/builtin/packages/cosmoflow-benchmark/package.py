# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CosmoflowBenchmark(Package):
    """This is a an implementation of the CosmoFlow 3D convolutional neural
    network for benchmarking. It is written in TensorFlow with the Keras API
    and uses Horovod for distributed training."""

    homepage = "https://github.com/sparticlesteve/cosmoflow-benchmark"
    url      = "hhttps://github.com/sparticlesteve/cosmoflow-benchmark/archive/master.zip"
    git      = "https://github.com/sparticlesteve/cosmoflow-benchmark.git"

    tags = ['proxy-app']

    version('master', branch='master')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-tensorflow')
    depends_on('py-h5py')
    depends_on('py-numpy')
    depends_on('py-pandas')
    depends_on('py-pyyaml')
    depends_on('py-horovod')
    depends_on('py-mpi4py')

    def install(self, spec, prefix):
        # Mostly  about providing an environment so just copy everything
        install_tree('.', prefix)
