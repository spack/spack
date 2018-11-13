# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytorch(PythonPackage):
    """Tensors and Dynamic neural networks in Python
    with strong GPU acceleration."""

    homepage = "http://pytorch.org/"
    git      = "https://github.com/pytorch/pytorch.git"

    version('0.4.0', tag='v0.4.0', submodules=True)
    version('0.3.1', tag='v0.3.1', submodules=True)

    variant('cuda', default='False', description='Add GPU support')
    variant('cudnn', default='False', description='Add cuDNN support')
    variant('nccl', default='False', description='Add NCCL support')
    variant('mkldnn', default='False', description='Add Intel MKL DNN support')
    variant('magma', default='False', description='Add MAGMA support')

    conflicts('+cudnn', when='~cuda')
    conflicts('+nccl', when='~cuda')
    conflicts('+magma', when='~cuda')
    conflicts('+mkldnn', when='@:0.3.2')

    depends_on('py-setuptools', type='build')
    depends_on('py-cffi', type='build')
    depends_on('py-numpy', type=('run', 'build'))
    depends_on('blas')
    depends_on('lapack')
    depends_on('py-pyyaml', type=('run', 'build'))
    depends_on('py-typing', when='@0.3.2:', type=('run', 'build'))
    depends_on('intel-mkl', when='+mkl')
    depends_on('cuda', when='+cuda', type=('build', 'link', 'run'))
    depends_on('cudnn', when='+cuda+cudnn')
    depends_on('nccl', when='+cuda+nccl')
    depends_on('magma+shared', when='+cuda+magma')

    def setup_environment(self, build_env, run_env):
        build_env.set('MAX_JOBS', make_jobs)

        if '+cuda' in self.spec:
            build_env.set('CUDA_HOME', self.spec['cuda'].prefix)
        else:
            build_env.set('NO_CUDA', 'TRUE')

        if '+cudnn' in self.spec:
            build_env.set('CUDNN_LIB_DIR',
                          self.spec['cudnn'].prefix.lib)
            build_env.set('CUDNN_INCLUDE_DIR',
                          self.spec['cudnn'].prefix.include)
        else:
            build_env.set('NO_CUDNN', 'TRUE')

        if '+nccl' in self.spec:
            build_env.set('NCCL_ROOT_DIR', self.spec['nccl'].prefix)
        else:
            build_env.set('NO_SYSTEM_NCCL', 'TRUE')

        if '+mkldnn' in self.spec:
            build_env.set('MKLDNN_HOME', self.spec['intel-mkl'].prefix)
        else:
            build_env.set('NO_MKLDNN', 'TRUE')

        build_env.set('NO_NNPACK', 'TRUE')

        build_env.set('PYTORCH_BUILD_VERSION', str(self.version))
        build_env.set('PYTORCH_BUILD_NUMBER', 0)
