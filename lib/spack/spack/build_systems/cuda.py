# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PackageBase
from spack.directives import depends_on, variant, conflicts
import platform


class CudaPackage(PackageBase):
    """Auxiliary class which contains CUDA variant, dependencies and conflicts
    and is meant to unify and facilitate its usage.
    """

    # FIXME: keep cuda and cuda_arch separate to make usage easier untill
    # Spack has depends_on(cuda, when='cuda_arch!=None') or alike
    variant('cuda', default=False,
            description='Build with CUDA')
    # see http://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#gpu-feature-list
    # https://developer.nvidia.com/cuda-gpus
    variant('cuda_arch', default=None,
            description='CUDA architecture',
            values=('20', '30', '32', '35', '50', '52', '53', '60', '61',
                    '62', '70'),
            multi=True)

    # see http://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#nvcc-examples
    # and http://llvm.org/docs/CompileCudaWithLLVM.html#compiling-cuda-code
    @staticmethod
    def cuda_flags(arch_list):
        return [('--generate-code arch=compute_{0},code=sm_{0} '
                 '--generate-code arch=compute_{0},code=compute_{0}').format(s)
                for s in arch_list]

    depends_on("cuda@7:", when='+cuda')

    # CUDA version vs Architecture
    depends_on("cuda@8:", when='cuda_arch=60')
    depends_on("cuda@8:", when='cuda_arch=61')
    depends_on("cuda@8:", when='cuda_arch=62')
    depends_on("cuda@9:", when='cuda_arch=70')

    depends_on('cuda@:8', when='cuda_arch=20')

    # Compiler conflicts:
    # https://gist.github.com/ax3l/9489132
    conflicts('%gcc@5:', when='+cuda ^cuda@:7.5')
    conflicts('%gcc@6:', when='+cuda ^cuda@:8')
    conflicts('%gcc@7:', when='+cuda ^cuda@:9.1')
    conflicts('%gcc@8:', when='+cuda ^cuda@:9.99')
    if (platform.system() != "Darwin"):
        conflicts('%clang@:3.4,3.7:', when='+cuda ^cuda@7.5')
        conflicts('%clang@:3.7,4:', when='+cuda ^cuda@8:9.0')
        conflicts('%clang@:3.7,5:', when='+cuda ^cuda@9.1')
        conflicts('%clang@:3.7,6:', when='+cuda ^cuda@9.2')
    conflicts('%intel@:14,16:', when='+cuda ^cuda@7.5')
    conflicts('%intel@:14,17:', when='+cuda ^cuda@8.0.44')
    conflicts('%intel@:14,18:', when='+cuda ^cuda@8.0.61:9')

    # Make sure cuda_arch can not be used without +cuda
    conflicts('~cuda', when='cuda_arch=20')
    conflicts('~cuda', when='cuda_arch=30')
    conflicts('~cuda', when='cuda_arch=32')
    conflicts('~cuda', when='cuda_arch=35')
    conflicts('~cuda', when='cuda_arch=50')
    conflicts('~cuda', when='cuda_arch=52')
    conflicts('~cuda', when='cuda_arch=53')
    conflicts('~cuda', when='cuda_arch=60')
    conflicts('~cuda', when='cuda_arch=61')
    conflicts('~cuda', when='cuda_arch=62')
    conflicts('~cuda', when='cuda_arch=70')
