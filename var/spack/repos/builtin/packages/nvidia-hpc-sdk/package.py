# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.util.prefix import Prefix
import platform
import os


class NvidiaHpcSdk(Package, CudaPackage):
    """The NVIDIA HPC Software Development Kit (SDK) includes the proven compilers,
       libraries and software tools essential to maximizing developer productivity
       and the performance and portability of HPC applications."""

    homepage = "https://developer.nvidia.com/hpc-sdk"

    maintainers = ['ajkotobi']

    version('2020_207', sha256='a5c5c8726d2210f2310a852c6d6e03c9ef8c75e3643e9c94e24909f5e9c2ea7a')

    variant('network', default='network', description='Network installation',
      values=('network', 'single'), multi=False)

    depends_on('cuda@10:')
    conflicts('^cuda@:10', when='platform=aarch64')

    def url_for_version(self, version):
        if platform.machine() == "aarch64":
           url = "https://developer.download.nvidia.com/hpc-sdk/nvhpc_{0}_Linux_{1}_cuda_11.0.tar.gz"
        else:
           url = "https://developer.download.nvidia.com/hpc-sdk/nvhpc_{0}_Linux_{1}_cuda_multi.tar.gz"
        return url.format(version, platform.machine())

    def install(self, spec, prefix):

        os.environ['NVHPC_SILENT'] = "true"
        os.environ['NVHPC_INSTALL_DIR'] = self.prefix
        os.environ['NVHPC_DEFAULT_CUDA'] = str(self.spec['cuda'].version.up_to(2))
        os.environ['NVHPC_INSTALL_TYPE'] = self.spec.variants['network'].value
        os.environ['NVHPC_INSTALL_LOCAL_DIR'] = self.prefix

        os.system("./install")

    def setup_run_environment(self, env):
        # TO-DO: Cleaner way to handle path building
        ver_build = self.version.split("_", 1)[1]
        target_version = ver_build[:2]+'.'+ver_build[:-1]
        prefix_new = Prefix(join_path(self.prefix,
          platform.system()+'_'+platform.machine(), target_version))

        env.set('target', platform.system()+'_'+platform.machine())
        env.set('version', target_version)
        env.set('NVHPC', prefix_new)

        env.set('PATH', prefix_new.compilers.bin)
        env.set('LD_LIBRARY_PATH', prefix_new.compilers.lib)
        env.set('MANPATH', prefix_new.compilers.man)

        env.set('F77', join_path(prefix_new.compilers.bin, 'nvfortran'))
        env.set('F90', join_path(prefix_new.compilers.bin, 'nvfortran'))
        env.set('FC',  join_path(prefix_new.compilers.bin, 'nvfortran'))
        env.set('CC',  join_path(prefix_new.compilers.bin, 'nvc'))
        env.set('CXX', join_path(prefix_new.compilers.bin, 'nvc++'))
        env.set('CPP',  'cpp')

        env.prepend_path('CPATH', prefix_new.math_libs.include)
        env.prepend_path('CPATH', prefix_new.compilers.include)
        env.prepend_path('CPATH', prefix_new.cuda.include)

        env.prepend_path('LD_LIBRARY_PATH', prefix_new.cuda.lib64)
        env.prepend_path('LD_LIBRARY_PATH', prefix_new.math_libs.lib64)
