# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyHorovod(PythonPackage):
    """Horovod is a distributed deep learning training framework for
    TensorFlow, Keras, PyTorch, and Apache MXNet."""

    homepage = "https://github.com/horovod"
    git      = "https://github.com/horovod/horovod.git"
    url      = "https://github.com/horovod/horovod/archive/v0.19.0.tar.gz"

    maintainers = ['adamjstewart']

    version('master', branch='master', submodules='True')
    version('0.19.0', sha256='0e9fec11cd7f5f39a09f0785d1097cb51c44537ae14c9b4b2578b5cdd21efb9b')
    version('0.18.2', sha256='a073e08cec65474afdb2d011486b4cb6c7ac8fcb1eca3e02b169e1e7b4a66da6')
    version('0.18.1', sha256='26e236d1f60955e9dd12b9f0a836f0691296a010fcd1ac72295970a780f4e4fb')
    version('0.18.0', sha256='94f13e7110c5f3fd1aa194b9d886b5bb91c9bc02ade31bcb84fc6e7f9c043455')
    version('0.17.1', sha256='14eea5744eda9c62988ffa278a9a5472cebbc6a287eca9ed48cacfcd177e8978')
    version('0.17.0', sha256='4bb121dda6cdaa1677535470adc1836493a9c4930ab19f6b491254ea47a12a4f')
    version('0.16.4', sha256='c0168dfeb31a56ede52eae115f43fa2d06a5db55a37201064ef901c8000d708d')
    version('0.16.3', sha256='1857cf1b335723366cc71e4bcd0583f2dde0c821212cda0e1b6bddfe4ba1ea0d')
    version('0.16.2', sha256='baa9754e59ab0ee72d3b5769cf77e06a2c7b0a2d9626e0e14ca2ab131934ce74')

    # Deep learning frameworks
    variant('pytorch',    default=True,  description='Enables PyTorch')
    variant('tensorflow', default=False, description='Enables TensorFlow')
    variant('mxnet',      default=False, description='Enables Apache MXNet')

    # Distributed support
    variant('gloo', default=False, description='Enables features related to distributed support')
    variant('mpi',  default=True,  description='Enables MPI build')

    # GPU support
    variant('cuda', default=True, description='Enables CUDA build')
    variant('gpu_allreduce', default='nccl',
            description='Backend to use for GPU_ALLREDUCE',
            values=('mpi', 'nccl'), multi=False)  # DDL support is deprecated
    variant('gpu_allgather', default='mpi',
            description='Backend to use for GPU_ALLGATHER',
            values=('mpi',), multi=False)
    variant('gpu_broadcast', default='nccl',
            description='Backend to use for GPU_BROADCAST',
            values=('mpi', 'nccl'), multi=False)

    # Required dependencies
    depends_on('py-setuptools', type='build')
    depends_on('py-cloudpickle', type=('build', 'run'))
    depends_on('py-psutil', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))

    # Deep learning frameworks
    depends_on('py-torch@0.4.0:', type=('build', 'run'), when='+pytorch')
    depends_on('py-torch+cuda', type=('build', 'run'), when='+pytorch+cuda')
    depends_on('py-cffi@1.4.0:', type=('build', 'run'), when='+pytorch')
    depends_on('py-tensorflow@1.1.0:', type=('build', 'link', 'run'), when='+tensorflow')
    depends_on('mxnet@1.4.0:+python', type=('build', 'link', 'run'), when='+mxnet')
    depends_on('mxnet+cuda', type=('build', 'link', 'run'), when='+mxnet+cuda')

    # Distributed support
    # There does not appear to be a way to use an external Gloo installation
    depends_on('cmake', type='build', when='+gloo')
    depends_on('mpi', when='+mpi')
    depends_on('mpi', when='gpu_allreduce=mpi')
    depends_on('mpi', when='gpu_allgather=mpi')
    depends_on('mpi', when='gpu_broadcast=mpi')

    # GPU support
    depends_on('cuda', when='+cuda')
    depends_on('nccl@2.0:', when='gpu_allreduce=nccl')
    depends_on('nccl@2.0:', when='gpu_broadcast=nccl')

    # Test dependencies
    depends_on('py-mock', type='test')
    depends_on('py-pytest', type='test')
    depends_on('py-pytest-forked', type='test')

    conflicts('+gloo', when='platform=darwin', msg='Gloo cannot be compiled on MacOS')
    conflicts('~gloo~mpi', msg='One of Gloo or MPI are required for Horovod to run')
    conflicts('~pytorch~tensorflow~mxnet', msg='At least one deep learning backend is required')

    def setup_build_environment(self, env):
        # Deep learning frameworks
        if '~pytorch' in self.spec:
            env.set('HOROVOD_WITHOUT_PYTORCH', 1)
        if '~tensorflow' in self.spec:
            env.set('HOROVOD_WITHOUT_TENSORFLOW', 1)
        if '~mxnet' in self.spec:
            env.set('HOROVOD_WITHOUT_MXNET', 1)

        # Distributed support
        if '~gloo' in self.spec:
            env.set('HOROVOD_WITHOUT_GLOO', 1)
        if '+mpi' in self.spec:
            env.set('HOROVOD_WITH_MPI', 1)
        else:
            env.set('HOROVOD_WITHOUT_MPI', 1)

        # GPU support
        if '+cuda' in self.spec:
            env.set('HOROVOD_CUDA_HOME', self.spec['cuda'].prefix)
            env.set('HOROVOD_CUDA_INCLUDE',
                    self.spec['cuda'].headers.directories[0])
            env.set('HOROVOD_CUDA_LIB', self.spec['cuda'].libs.directories[0])
        if '^nccl' in self.spec:
            env.set('HOROVOD_NCCL_HOME', self.spec['nccl'].prefix)
            env.set('HOROVOD_NCCL_INCLUDE',
                    self.spec['nccl'].headers.directories[0])
            env.set('HOROVOD_NCCL_LIB', self.spec['nccl'].libs.directories[0])
        env.set('HOROVOD_GPU_ALLREDUCE',
                self.spec.variants['gpu_allreduce'].value.upper())
        env.set('HOROVOD_GPU_ALLGATHER',
                self.spec.variants['gpu_allgather'].value.upper())
        env.set('HOROVOD_GPU_BROADCAST',
                self.spec.variants['gpu_broadcast'].value.upper())
