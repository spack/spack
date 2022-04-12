from spack import *
from spack.pkg.builtin.py_torch import PyTorch as BuiltinPyTorch


class PyTorch(BuiltinPyTorch):
    __doc__ = BuiltinPyTorch.__doc__

    # GCC 11 removed thread_id equality, fix other compilation errors
    patch('gcc_thread_id.patch', when='@1.10.0%gcc@11')
    patch('https://patch-diff.githubusercontent.com/raw/pytorch/pytorch/pull/66089.patch',
          sha256='1965445f124b15fbbfc1b9a8e70a798296123a1db0d5186d09a74bb060aa8794',
          when='@1.10.0%gcc@11')
