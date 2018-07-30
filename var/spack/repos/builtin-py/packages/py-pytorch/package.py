##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
