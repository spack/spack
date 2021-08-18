# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install flexflow
#
# You can edit this file again by typing:
#
#     spack edit flexflow
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os

from spack import *


class Flexflow(CMakePackage):
  """FlexFlow is a deep learning framework that accelerates 
     distributed DNN training by automatically searching for 
     efficient parallelization strategies. FlexFlow provides 
     a drop-in replacement for TensorFlow Keras and PyTorch. """

  homepage = "http://flexflow.ai"
  git = "https://github.com/flexflow/FlexFlow.git"
  
  maintainers = ['jiazhihao', 'eddy16112']
  version('master', branch='master', submodules=True)
  
  depends_on("cmake@3.16:", type='build')
  depends_on('cuda@10.0:11.9')
  depends_on('cudnn')
 
  depends_on('nccl', when='+nccl')
  depends_on('python@3.6:3.9', when='+python')
  depends_on('mpi', when='network=gasnet')
  depends_on('ucx', when='conduit=ucx')
  depends_on('mpi', when='conduit=mpi')
  
  cuda_arch_list = ('0', '60', '70', '75', '80')
  max_dims_list = ('4', '5')
  gasnet_conduit_list = ('aries', 'ibv', 'udp', 'mpi', 'ucx', 'none')
  for nvarch in cuda_arch_list:
    for maxdims in max_dims_list:
      for gasnet_conduit in gasnet_conduit_list:
        depends_on('legion@flexflow +cuda cuda_arch={0} +cuda_hijack -gpu_reduction +python max_dims={1} conduit={2}'.format(nvarch, maxdims, gasnet_conduit),
                   when='cuda_arch={0} max_dims={1} conduit={2}'.format(nvarch, maxdims, gasnet_conduit))
  
  variant('max_dims', default='4',
          values=max_dims_list,
          description="Set max number of dimensions for logical regions.",
          multi=False)
  
  variant('zlib', default=True, description="Enable zlib support.")
  
  variant('nccl', default=False, description="Enable zlib support.")
  
  variant('python', default=True, description="Enable Python support.")
  
  variant('examples', default=False, description="Build all examples.")
 
  variant('avx2', default=False, description="Enable AVX2 support.")  

  variant('gasnet', default=False, description="Enable GASNet support.")
 
  variant('conduit', default='none',
          values=gasnet_conduit_list,
          description="The gasnet conduit(s) to enable.",
          multi=False)
  conflicts('conduit=none', when='gasnet=True',
            msg="a conduit must be selected when enable GASNet")
  
  # cuda_arch=0 means FlexFlow will automatically detect the cuda arch of the current platform
  variant('cuda_arch', default='0',
          values=cuda_arch_list,
          description="GPU/CUDA architecture to build for.",
          multi=False)

  def cmake_args(self):
    spec = self.spec
    cmake_cxx_flags = []
    options = ['-DCUDA_USE_STATIC_CUDA_RUNTIME=OFF']
    
    if '+python' in spec:
      options.append('-DFF_USE_PYTHON=ON')
    else:
      options.append('-DFF_USE_PYTHON=OFF')
      
    if '+nccl' in spec:
      options.append('-DFF_USE_NCCL=ON')
    else:
      options.append('-DFF_USE_NCCL=OFF')
      
    if '+examples' in spec:
      options.append('-DFF_BUILD_ALL_EXAMPLES=ON')
    else:
      options.append('-DFF_BUILD_ALL_EXAMPLES=OFF')
      
    if '+avx2' in spec:
      options.append('-DFF_USE_AVX2=ON')
    else:
      options.append('-DFF_USE_AVX2=OFF')

    if '+gasnet' in spec:
      options.append('-DFF_USE_GASNET=ON')
      gasnet_conduit = spec.variants['conduit'].value
      options.append('-DFF_GASNET_CONDUIT=%s' % gasnet_conduit)
    else:
      options.append('-DFF_USE_GASNET=OFF')

    maxdims = spec.variants['max_dims'].value
    options.append('-DFF_MAX_DIM=%s' % maxdims)
  
    cuda_arch = spec.variants['cuda_arch'].value
    if cuda_arch != '0': 
      options.append('-DFF_CUDA_ARCH=%s' % cuda_arch)
  
    legion_root = '/vast/home/wwu/spack/opt/spack/linux-centos7-broadwell/gcc-8.1.0/legion-flexflow-ewcwauwrlac6z3lofy7mh24xg4oa22vt'
    options.append('-DLEGION_ROOT=%s' %legion_root)  
    return options
