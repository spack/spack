# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTorch(PythonPackage):
    """Tensors and Dynamic neural networks in Python
    with strong GPU acceleration."""

    homepage = "http://pytorch.org/"
    git      = "https://github.com/pytorch/pytorch.git"

    maintainers = ['adamjstewart']
    import_modules = [
        'tools', 'caffe2', 'torch', 'tools.cwrap', 'tools.autograd',
        'tools.setup_helpers', 'tools.shared', 'tools.jit', 'tools.pyi',
        'tools.nnwrap', 'tools.cwrap.plugins', 'caffe2.core', 'caffe2.proto',
        'caffe2.python', 'caffe2.distributed', 'caffe2.perfkernels',
        'caffe2.experiments', 'caffe2.contrib', 'caffe2.quantization',
        'caffe2.core.nomnigraph', 'caffe2.python.ideep', 'caffe2.python.mint',
        'caffe2.python.layers', 'caffe2.python.onnx', 'caffe2.python.trt',
        'caffe2.python.models', 'caffe2.python.docs', 'caffe2.python.modeling',
        'caffe2.python.mkl', 'caffe2.python.examples',
        'caffe2.python.predictor', 'caffe2.python.helpers',
        'caffe2.python.rnn', 'caffe2.python.onnx.bin',
        'caffe2.python.models.seq2seq', 'caffe2.experiments.python',
        'caffe2.contrib.nnpack', 'caffe2.contrib.warpctc',
        'caffe2.contrib.nccl', 'caffe2.contrib.playground',
        'caffe2.contrib.gloo', 'caffe2.contrib.script', 'caffe2.contrib.prof',
        'caffe2.contrib.tensorboard', 'caffe2.contrib.aten',
        'caffe2.contrib.playground.resnetdemo',
        'caffe2.contrib.script.examples', 'caffe2.contrib.aten.docs',
        'caffe2.quantization.server', 'torch.nn', 'torch.onnx',
        'torch.distributed', 'torch.autograd', 'torch.multiprocessing',
        'torch.cuda', 'torch.backends', 'torch.optim', 'torch.utils',
        'torch.contrib', 'torch.jit', 'torch.sparse',
        'torch.for_onnx', 'torch._thnn', 'torch.distributions',
        'torch.nn.parallel', 'torch.nn._functions', 'torch.nn.backends',
        'torch.nn.utils', 'torch.nn.modules', 'torch.nn.parallel.deprecated',
        'torch.nn._functions.thnn', 'torch.distributed.deprecated',
        'torch.autograd._functions', 'torch.backends.cuda',
        'torch.backends.mkl', 'torch.backends.mkldnn', 'torch.backends.openmp',
        'torch.backends.cudnn', 'torch.utils.backcompat',
        'torch.utils.bottleneck', 'torch.utils.ffi', 'torch.utils.tensorboard',
        'torch.utils.data', 'torch.utils.data._utils'
    ]

    version('1.1.0', tag='v1.1.0', submodules=True)
    version('1.0.1', tag='v1.0.1', submodules=True)
    version('1.0.0', tag='v1.0.0', submodules=True)
    version('0.4.1', tag='v0.4.1', submodules=True)
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
    depends_on('py-typing', when='@0.3.2: ^python@:3.4', type=('run', 'build'))
    depends_on('intel-mkl', when='+mkl')
    depends_on('cuda@7.5:', when='+cuda', type=('build', 'link', 'run'))
    depends_on('cuda@9:', when='@1.1:+cuda', type=('build', 'link', 'run'))
    depends_on('cudnn@6:', when='+cuda+cudnn')
    depends_on('cudnn@7:', when='@1.1:+cuda+cudnn')
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
