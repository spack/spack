# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from glob import glob


class Cuda(Package):
    """CUDA is a parallel computing platform and programming model invented
    by NVIDIA. It enables dramatic increases in computing performance by
    harnessing the power of the graphics processing unit (GPU).

    Note: This package does not currently install the drivers necessary
    to run CUDA. These will need to be installed manually. See:
    https://docs.nvidia.com/cuda/ for details."""

    homepage = "https://developer.nvidia.com/cuda-zone"

    version('10.0.130', sha256='92351f0e4346694d0fcb4ea1539856c9eb82060c25654463bfd8574ec35ee39a', expand=False,
            url="https://developer.nvidia.com/compute/cuda/10.0/Prod/local_installers/cuda_10.0.130_410.48_linux")
    version('9.2.88', 'dd6e33e10d32a29914b7700c7b3d1ca0', expand=False,
            url="https://developer.nvidia.com/compute/cuda/9.2/Prod/local_installers/cuda_9.2.88_396.26_linux")
    version('9.1.85', '67a5c3933109507df6b68f80650b4b4a', expand=False,
            url="https://developer.nvidia.com/compute/cuda/9.1/Prod/local_installers/cuda_9.1.85_387.26_linux")
    version('9.0.176', '7a00187b2ce5c5e350e68882f42dd507', expand=False,
            url="https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda_9.0.176_384.81_linux-run")
    version('8.0.61', '33e1bd980e91af4e55f3ef835c103f9b', expand=False,
            url="https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda_8.0.61_375.26_linux-run")
    version('8.0.44', '6dca912f9b7e2b7569b0074a41713640', expand=False,
            url="https://developer.nvidia.com/compute/cuda/8.0/prod/local_installers/cuda_8.0.44_linux-run")
    version('7.5.18', '4b3bcecf0dfc35928a0898793cf3e4c6', expand=False,
            url="http://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/cuda_7.5.18_linux.run")
    version('6.5.14', '90b1b8f77313600cc294d9271741f4da', expand=False,
            url="http://developer.download.nvidia.com/compute/cuda/6_5/rel/installers/cuda_6.5.14_linux_64.run")

    # CUDA conflicts taken from official NVidia website
    #
    # Note that installation guide for CUDA prior to 8.0 are unavailable,
    # thus no Spack conflict statements have been implemented prior to
    # version 8.0.44. These are conflicts from Linux systems analagous
    # conflicts for Mac can be added later.
    #
    # Not all conflicts are expressed, some conflicts are never encountered
    # in practice. For example, XL compiler on Intel hardware or vice-versa
    cuda_warning = 'CUDA is not supported by this version of the compiler ' \
                   'on your architecture.'

    # CUDA 10.0.130
    # Table 1 from here:
    # https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html
    cuda_version = '@10.0.130'
    conflicts('%gcc@8:', when=cuda_version, msg=cuda_warning)
    conflicts('%llvm@7:', when=cuda_version, msg=cuda_warning)
    conflicts('%pgi@:17', when=cuda_version, msg=cuda_warning)

    cuda_version = '@10.0.130 arch=x86_64'
    conflicts('%intel@:17', when=cuda_version, msg=cuda_warning)
    conflicts('%intel@19:', when=cuda_version, msg=cuda_warning)

    cuda_version = '@10.0.130 arch=ppc64le'
    conflicts('%xl@:12', when=cuda_version, msg=cuda_warning)
    conflicts('%xl@14:15', when=cuda_version, msg=cuda_warning)
    conflicts('%xl@17:', when=cuda_version, msg=cuda_warning)

    # CUDA 9.2.88
    # https://docs.nvidia.com/cuda/archive/9.2/cuda-installation-guide-linux/index.html
    cuda_version = '@9.2.88'
    conflicts('%llvm@6:', when=cuda_version, msg=cuda_warning)

    cuda_version = '@9.2.88 arch=x86_64'
    conflicts('%gcc@8:', when=cuda_version, msg=cuda_warning)
    conflicts('%pgi@:16', when=cuda_version, msg=cuda_warning)
    conflicts('%intel@18:', when=cuda_version, msg=cuda_warning)

    cuda_version = '@9.2.88 arch=ppc64le'
    conflicts('%gcc@6:', when=cuda_version, msg=cuda_warning)
    conflicts('%pgi@:17', when=cuda_version, msg=cuda_warning)
    conflicts('%xl@:12', when=cuda_version, msg=cuda_warning)
    conflicts('%xl@14:15', when=cuda_version, msg=cuda_warning)

    # CUDA 9.1.85
    # https://docs.nvidia.com/cuda/archive/9.1/cuda-installation-guide-linux/index.html
    cuda_version = '@9.1.85'
    conflicts('%pgi@:16', when=cuda_version, msg=cuda_warning)
    conflicts('%llvm@5:', when=cuda_version, msg=cuda_warning)

    cuda_version = '@9.1.85 arch=x86_64'
    conflicts('%gcc@7:', when=cuda_version, msg=cuda_warning)
    conflicts('%intel@:16', when=cuda_version, msg=cuda_warning)
    conflicts('%intel@18:', when=cuda_version, msg=cuda_warning)

    cuda_version = '@9.1.85 arch=ppc64le'
    conflicts('%gcc@6:', when=cuda_version, msg=cuda_warning)
    conflicts('%xl@:12', when=cuda_version, msg=cuda_warning)
    conflicts('%xl@14:', when=cuda_version, msg=cuda_warning)

    # CUDA 9.0.176
    # https://docs.nvidia.com/cuda/archive/9.0/cuda-installation-guide-linux/index.html
    cuda_version = '@9.0.176'
    conflicts('%pgi@:16', when=cuda_version, msg=cuda_warning)
    conflicts('%llvm@4:', when=cuda_version, msg=cuda_warning)

    cuda_version = '@9.0.176 arch=x86_64'
    conflicts('%gcc@7:', when=cuda_version, msg=cuda_warning)
    conflicts('%intel@:16', when=cuda_version, msg=cuda_warning)
    conflicts('%intel@18:', when=cuda_version, msg=cuda_warning)

    cuda_version = '@9.0.176 arch=ppc64le'
    conflicts('%gcc@6:', when=cuda_version, msg=cuda_warning)
    conflicts('%xl@:12', when=cuda_version, msg=cuda_warning)
    conflicts('%xl@14:', when=cuda_version, msg=cuda_warning)

    # CUDA 8.0.x
    # https://docs.nvidia.com/cuda/archive/8.0/cuda-installation-guide-linux/index.html
    cuda_version = '@8 arch=x86_64'
    conflicts('%gcc@7:', when=cuda_version, msg=cuda_warning) 
    conflicts('%intel@:16', when=cuda_version, msg=cuda_warning)
    conflicts('%intel@17:', when=cuda_version, msg=cuda_warning)
    conflicts('%pgi@:16', when=cuda_version, msg=cuda_warning)
    conflicts('%llvm@4:', when=cuda_version, msg=cuda_warning)

    cuda_version = '@8 arch=ppc64le'
    conflicts('%pgi', when=cuda_version, msg=cuda_warning)
    conflicts('%xl@:12', when=cuda_version, msg=cuda_warning)
    conflicts('%xl@14:', when=cuda_version, msg=cuda_warning)
    conflicts('%llvm', when=cuda_version, msg=cuda_warning)

    def setup_environment(self, spack_env, run_env):
        run_env.set('CUDA_HOME', self.prefix)

    def install(self, spec, prefix):
        runfile = glob(join_path(self.stage.path, 'cuda*_linux*'))[0]
        chmod = which('chmod')
        chmod('+x', runfile)
        runfile = which(runfile)

        # Note: NVIDIA does not officially support many newer versions of
        # compilers.  For example, on CentOS 6, you must use GCC 4.4.7 or
        # older. See:
        # http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#system-requirements
        # https://gist.github.com/ax3l/9489132
        # for details.

        runfile(
            '--silent',         # disable interactive prompts
            '--verbose',        # create verbose log file
            '--override',       # override compiler version checks
            '--toolkit',        # install CUDA Toolkit
            '--toolkitpath=%s' % prefix
        )
