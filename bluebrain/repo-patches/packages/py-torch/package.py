from spack import *
from spack.pkg.builtin.py_torch import PyTorch as BuiltinPyTorch


class PyTorch(BuiltinPyTorch):
    __doc__ = BuiltinPyTorch.__doc__

    # GCC 11 removed thread_id equality, fix other compilation errors
    patch('gcc_thread_id.patch', when='@1.10.0%gcc@11')
    patch('https://patch-diff.githubusercontent.com/raw/pytorch/pytorch/pull/66089.patch',
          sha256='a03a7a55c61e965a75a979328592fb62819cf08bb5f33ff235a4035494dcb620',
          when='@1.10.0%gcc@11')
