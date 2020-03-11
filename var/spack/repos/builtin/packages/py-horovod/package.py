# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import fnmatch
import os


class PyHorovod(PythonPackage):
    """Horovod is a distributed deep learning training framework for
    TensorFlow, Keras, PyTorch, and Apache MXNet."""

    homepage = "https://github.com/horovod"
    git      = "https://github.com/horovod/horovod.git"
    url      = "https://github.com/horovod/horovod/archive/v0.19.0.tar.gz"

    version('master', branch='master', submodules='True')
    version('0.19.0',       sha256='0e9fec11cd7f5f39a09f0785d1097cb51c44537ae14c9b4b2578b5cdd21efb9b')
    version('0.18.2',       sha256='a073e08cec65474afdb2d011486b4cb6c7ac8fcb1eca3e02b169e1e7b4a66da6')
    version('0.18.1',       sha256='26e236d1f60955e9dd12b9f0a836f0691296a010fcd1ac72295970a780f4e4fb')
    version('0.18.0',       sha256='94f13e7110c5f3fd1aa194b9d886b5bb91c9bc02ade31bcb84fc6e7f9c043455')
    version('0.17.1',       sha256='14eea5744eda9c62988ffa278a9a5472cebbc6a287eca9ed48cacfcd177e8978')
    version('0.17.0.post1', sha256='220b230611e22dc69777f1be4d9788a07e73a0722e511091fa156cdf68ca798b')
    version('0.17.0',       sha256='4bb121dda6cdaa1677535470adc1836493a9c4930ab19f6b491254ea47a12a4f')
    version('0.16.4',       sha256='c0168dfeb31a56ede52eae115f43fa2d06a5db55a37201064ef901c8000d708d')
    version('0.16.3',       sha256='1857cf1b335723366cc71e4bcd0583f2dde0c821212cda0e1b6bddfe4ba1ea0d')
    version('0.16.2',       sha256='baa9754e59ab0ee72d3b5769cf77e06a2c7b0a2d9626e0e14ca2ab131934ce74')

    variant('pytorch', default=True, description='Enables PyTorch')
    variant('mxnet', default=False, description='Enables mxnet')
    variant('mpi', default=True, description='Enables MPI build')
    variant('gloo', default=False, description='Enables features related to distributed support')
    variant('cuda', default=True, description='Enables CUDA build')

    depends_on('python', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cloudpickle', type=('build', 'run'))
    depends_on('py-psutil', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-torch', type=('build', 'run'))
    depends_on('py-pip', type=('build'))

    # Optional dependencies
    depends_on('cuda', when='+cuda')
    depends_on('nccl', when='+nccl')
    depends_on('gloo', when='+gloo')
    depends_on('mpi', when='+mpi')
    depends_on('py-torch', type=('build', 'run'), when='+pytorch')
    depends_on('mxnet', when='+mxnet')

    phases = ['clean', 'sdist', 'install']

    def install(self, spec, prefix):
        pip = which('pip')
        for file in os.listdir(prefix):
            if fnmatch.fnmatch(file, 'horovod-*.tar.gz'):
                pip('install', file, '--prefix={0}'.format(prefix))
