# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyHorovod(PythonPackage):
    """Horovod is a distributed deep learning training framework for
    TensorFlow, Keras, PyTorch, and Apache MXNet."""

    homepage = "https://github.com/horovod"
    git      = "https://github.com/horovod/horovod.git"

    maintainers = ['adamjstewart']

    version('master', branch='master', submodules=True)
    version('0.19.3', tag='v0.19.3', submodules=True)
    version('0.19.2', tag='v0.19.2', submodules=True)
    version('0.19.1', tag='v0.19.1', submodules=True)
    version('0.19.0', tag='v0.19.0', submodules=True)
    version('0.18.2', tag='v0.18.2', submodules=True)
    version('0.18.1', tag='v0.18.1', submodules=True)
    version('0.18.0', tag='v0.18.0', submodules=True)
    version('0.17.1', tag='v0.17.1', submodules=True)
    version('0.17.0', tag='v0.17.0', submodules=True)
    version('0.16.4', tag='v0.16.4', submodules=True)
    version('0.16.3', tag='v0.16.3', submodules=True)
    version('0.16.2', tag='v0.16.2', submodules=True)

    # https://github.com/horovod/horovod/blob/master/docs/install.rst
    variant('frameworks', default='pytorch',
            description='Deep learning frameworks to build support for',
            values=('tensorflow', 'pytorch', 'mxnet', 'keras', 'spark'),
            multi=True)
    variant('controllers', default='mpi',
            description='Controllers to coordinate work between processes',
            values=('mpi', 'gloo'), multi=True)
    variant('tensor_ops', default='nccl',
            description='Framework to use for GPU/CPU operations',
            values=('nccl', 'mpi', 'gloo', 'ccl'), multi=False)

    # Required dependencies
    depends_on('py-setuptools',  type='build')
    depends_on('py-cloudpickle', type=('build', 'run'))
    depends_on('py-psutil',      type=('build', 'run'))
    depends_on('py-pyyaml',      type=('build', 'run'))
    depends_on('py-six',         type=('build', 'run'))

    # Framework dependencies
    depends_on('py-tensorflow@1.1.0:',  type=('build', 'link', 'run'), when='frameworks=tensorflow')
    depends_on('py-torch@0.4.0:',       type=('build', 'link', 'run'), when='frameworks=pytorch')
    depends_on('py-torchvision',        type=('build', 'run'),         when='frameworks=pytorch @:0.19.1')
    depends_on('py-cffi@1.4.0:',        type=('build', 'run'),         when='frameworks=pytorch')
    depends_on('mxnet@1.4.1:+python',   type=('build', 'link', 'run'), when='frameworks=mxnet')
    depends_on('py-keras@2.0.8,2.1.2:', type=('build', 'run'),         when='frameworks=keras')
    depends_on('py-h5py@2.9:',          type=('build', 'run'),         when='frameworks=spark')
    depends_on('py-numpy',              type=('build', 'run'),         when='frameworks=spark')
    depends_on('py-petastorm@0.8.2',    type=('build', 'run'),         when='frameworks=spark @:0.19.1')
    depends_on('py-petastorm@0.9.0:',   type=('build', 'run'),         when='frameworks=spark @0.19.2:')
    depends_on('py-pyarrow@0.15.0:',    type=('build', 'run'),         when='frameworks=spark')
    depends_on('py-pyspark@2.3.2:',     type=('build', 'run'),         when='frameworks=spark')

    # Controller dependencies
    depends_on('mpi', when='controllers=mpi')
    # There does not appear to be a way to use an external Gloo installation
    depends_on('cmake', type='build', when='controllers=gloo')

    # Tensor Operations dependencies
    depends_on('nccl@2:', when='tensor_ops=nccl')
    depends_on('mpi', when='tensor_ops=mpi')
    # There does not appear to be a way to use an external Gloo installation
    depends_on('cmake', type='build', when='tensor_ops=gloo')

    # Test dependencies
    depends_on('py-mock', type='test')
    depends_on('py-pytest', type='test')
    depends_on('py-pytest-forked', type='test')

    conflicts('controllers=gloo', when='platform=darwin', msg='Gloo cannot be compiled on MacOS')

    # https://github.com/horovod/horovod/pull/1835
    patch('fma.patch', when='@0.19.0:0.19.1')

    def setup_build_environment(self, env):
        # Frameworks
        if 'frameworks=tensorflow' in self.spec:
            env.set('HOROVOD_WITH_TENSORFLOW', 1)
        else:
            env.set('HOROVOD_WITHOUT_TENSORFLOW', 1)
        if 'frameworks=pytorch' in self.spec:
            env.set('HOROVOD_WITH_PYTORCH', 1)
        else:
            env.set('HOROVOD_WITHOUT_PYTORCH', 1)
        if 'frameworks=mxnet' in self.spec:
            env.set('HOROVOD_WITH_MXNET', 1)
        else:
            env.set('HOROVOD_WITHOUT_MXNET', 1)

        # Controllers
        if 'controllers=mpi' in self.spec:
            env.set('HOROVOD_WITH_MPI', 1)
        else:
            env.set('HOROVOD_WITHOUT_MPI', 1)
        if 'controllers=gloo' in self.spec:
            env.set('HOROVOD_WITH_GLOO', 1)
        else:
            env.set('HOROVOD_WITHOUT_GLOO', 1)

        # Tensor Operations
        if 'tensor_ops=nccl' in self.spec:
            env.set('HOROVOD_GPU', 'CUDA')

            env.set('HOROVOD_CUDA_HOME', self.spec['cuda'].prefix)
            env.set('HOROVOD_CUDA_INCLUDE',
                    self.spec['cuda'].headers.directories[0])
            env.set('HOROVOD_CUDA_LIB', self.spec['cuda'].libs.directories[0])

            env.set('HOROVOD_NCCL_HOME', self.spec['nccl'].prefix)
            env.set('HOROVOD_NCCL_INCLUDE',
                    self.spec['nccl'].headers.directories[0])
            env.set('HOROVOD_NCCL_LIB', self.spec['nccl'].libs.directories[0])

            env.set('HOROVOD_GPU_ALLREDUCE', 'NCCL')
            env.set('HOROVOD_GPU_BROADCAST', 'NCCL')
        else:
            env.set('HOROVOD_CPU_OPERATIONS',
                    self.spec.variants['tensor_ops'].value.upper())

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        horovodrun = Executable(self.prefix.bin.horovodrun)
        horovodrun('--check-build')
