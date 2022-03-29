# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.

import os
import platform

from spack import *
from spack.util.prefix import Prefix

# FIXME Remove hack for polymorphic versions
# This package uses a ugly hack to be able to dispatch, given the same
# version, to different binary packages based on the platform that is
# running spack. See #13827 for context.
# If you need to add a new version, please be aware that:
#  - versions in the following dict are automatically added to the package
#  - version tuple must be in the form (checksum, url)
#  - checksum must be sha256
#  - package key must be in the form '{os}-{arch}' where 'os' is in the
#    format returned by platform.system() and 'arch' by platform.machine()
_versions = {
    '22.3': {
        'Linux-aarch64': ('9e103676f2bcbe07b21271abf896f003655c52dfdf465d02c2a031a8efbd89e0', 'https://developer.download.nvidia.com/hpc-sdk/22.3/nvhpc_2022_223_Linux_aarch64_cuda_11.6.tar.gz'),
        'Linux-ppc64le': ('42795734bb117b2d7ecf41ccd4abe81512fbde4396bc6f3b246e1f55b2b27415', 'https://developer.download.nvidia.com/hpc-sdk/22.3/nvhpc_2022_223_Linux_ppc64le_cuda_11.6.tar.gz'),
        'Linux-x86_64': ('19e9851767a518de696e25d5c5c0f3e7e03a980d172b27794a51878ca435aff5', 'https://developer.download.nvidia.com/hpc-sdk/22.3/nvhpc_2022_223_Linux_x86_64_cuda_11.6.tar.gz')},
    '22.2': {
        'Linux-aarch64': ('642a75041f50fa04042195fd319fc66062450f8990761341b0ed2cfbb0f28b11', 'https://developer.download.nvidia.com/hpc-sdk/22.2/nvhpc_2022_222_Linux_aarch64_cuda_11.6.tar.gz'),
        'Linux-ppc64le': ('2a0af91203f764309f7add3314fc853f1ccaac21cb6451b3b9abe32386e07c49', 'https://developer.download.nvidia.com/hpc-sdk/22.2/nvhpc_2022_222_Linux_ppc64le_cuda_11.6.tar.gz'),
        'Linux-x86_64': ('081a20c894ea0963940e3e1e8c4f2044892dea42ccbe4fbf8fdfde010b6a6bd7', 'https://developer.download.nvidia.com/hpc-sdk/22.2/nvhpc_2022_222_Linux_x86_64_cuda_11.6.tar.gz')},
    '22.1': {
        'Linux-aarch64': ('e2266ffa680bd47d40b3fb9a470c093a7cfc3d0ba5eb4dd7d061823f6bfb0f51', 'https://developer.download.nvidia.com/hpc-sdk/22.1/nvhpc_2022_221_Linux_aarch64_cuda_11.5.tar.gz'),
        'Linux-ppc64le': ('68c9a8568fae6567ab67fdcac8f1c1cf1de31fe12f12c0d118856b841069b82e', 'https://developer.download.nvidia.com/hpc-sdk/22.1/nvhpc_2022_221_Linux_ppc64le_cuda_11.5.tar.gz'),
        'Linux-x86_64': ('9bab2fb272b7f944a73337de2f9575f9a8d7cfc60ffd146a961c162b7b7ce08f', 'https://developer.download.nvidia.com/hpc-sdk/22.1/nvhpc_2022_221_Linux_x86_64_cuda_11.5.tar.gz')},
    '21.11': {
        'Linux-aarch64': ('6da80a49ad3bf56fc4fd35613ea3392a3593b822db716a87dc941098a366a5cb', 'https://developer.download.nvidia.com/hpc-sdk/21.11/nvhpc_2021_2111_Linux_aarch64_cuda_11.5.tar.gz'),
        'Linux-ppc64le': ('05b7bc46d85d75b18af11c38cf5b63f03a31dfe984b21bd2865e9d818bb9d29e', 'https://developer.download.nvidia.com/hpc-sdk/21.11/nvhpc_2021_2111_Linux_ppc64le_cuda_11.5.tar.gz'),
        'Linux-x86_64': ('91773db3a70dfbce70ecb46e00b823db0586ebab28cd5e66c947a1631971610c', 'https://developer.download.nvidia.com/hpc-sdk/21.11/nvhpc_2021_2111_Linux_x86_64_cuda_11.5.tar.gz')},
    '21.9': {
        'Linux-aarch64': ('7995bf20a2f24cad6703b7801e32f0768a59ed6413a5c9c9795ab87e4c1e40fe', 'https://developer.download.nvidia.com/hpc-sdk/21.9/nvhpc_2021_219_Linux_aarch64_cuda_11.4.tar.gz'),
        'Linux-ppc64le': ('72f98a5d4b50e2d94d3a7a90a988d441f768e22845058daf5a8868eed1699441', 'https://developer.download.nvidia.com/hpc-sdk/21.9/nvhpc_2021_219_Linux_ppc64le_cuda_11.4.tar.gz'),
        'Linux-x86_64': ('9203e9620dbd5699d92615d58df9adcffd19c6d25794d8b297b7b3723d16c9c1', 'https://developer.download.nvidia.com/hpc-sdk/21.9/nvhpc_2021_219_Linux_x86_64_cuda_11.4.tar.gz')},
    '21.7': {
        'Linux-aarch64': ('0357311dd1efd584b81ea6aad1cfbd5e813e2863310f15753f0bf14a7fad0f30', 'https://developer.download.nvidia.com/hpc-sdk/21.7/nvhpc_2021_217_Linux_aarch64_cuda_11.4.tar.gz'),
        'Linux-ppc64le': ('9fe221c21de1228eb7c991dcb857a8db5a1798b938c2e766ad306bbe051c3b52', 'https://developer.download.nvidia.com/hpc-sdk/21.7/nvhpc_2021_217_Linux_ppc64le_cuda_11.4.tar.gz'),
        'Linux-x86_64': ('e2062e0b4f56f4b31ed88d08f8cb9f371bf2f2fb0c59a06b2473833c742c8b75', 'https://developer.download.nvidia.com/hpc-sdk/21.7/nvhpc_2021_217_Linux_x86_64_cuda_11.4.tar.gz')},
    '21.5': {
        'Linux-aarch64': ('301e6a2901f031a48e6cd347985202d4312f90100361c52c4682d074e5f49e06', 'https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_aarch64_cuda_11.3.tar.gz'),
        'Linux-ppc64le': ('2273f973471eb0c4f53186e26bdf5aeab592dc6b4272fae42f3afecd33a7bfa5', 'https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_ppc64le_cuda_11.3.tar.gz'),
        'Linux-x86_64': ('c624cdd662099fbde5ca904272ad614ef190577b4bbbf8921e49968f1de6502d', 'https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_x86_64_cuda_11.3.tar.gz')},
    '21.3': {
        'Linux-aarch64': ('cfae502b8623931992ae2feb2329cd9f51c031718a4474cb627103144d72ad77', 'https://developer.download.nvidia.com/hpc-sdk/21.3/nvhpc_2021_213_Linux_aarch64_cuda_11.2.tar.gz'),
        'Linux-ppc64le': ('a9a5e132457e0a35424f28d42425ef310bd20eb3a49dbcbdc000a579ad63e02f', 'https://developer.download.nvidia.com/hpc-sdk/21.3/nvhpc_2021_213_Linux_ppc64le_cuda_11.2.tar.gz'),
        'Linux-x86_64': ('d5e90baf1aaf8d6b41c2901950c2c2d02ac441456276f3f46c9fee962527c042', 'https://developer.download.nvidia.com/hpc-sdk/21.3/nvhpc_2021_213_Linux_x86_64_cuda_11.2.tar.gz')},
    '21.2': {
        'Linux-aarch64': ('049d2ac25d3f36a614b22b078e5cc9dec84ea4957c8108ecccf93492e703763c', 'https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_aarch64_cuda_11.2.tar.gz'),
        'Linux-ppc64le': ('a052a8aee516ef8416bf182b7f49435a5a71af3215dfeffc21f5c8ca9707922d', 'https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_ppc64le_cuda_11.2.tar.gz'),
        'Linux-x86_64': ('aadab6f66c90fff7fb553ce1bbd65923d4723ef124101bce1cb080a7362d6f3b', 'https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_x86_64_cuda_11.2.tar.gz')},
    '21.1': {
        'Linux-aarch64': ('4d6b7915f6abfc2c4031d5dddb72917259c79875ef80f349e1b376a592a2c85b', 'https://developer.download.nvidia.com/hpc-sdk/21.1/nvhpc_2021_211_Linux_aarch64_cuda_11.2.tar.gz'),
        'Linux-ppc64le': ('e0f30a3456e869a6983ec30e30a79647506cec2b998961b5e05e7856b9f01c85', 'https://developer.download.nvidia.com/hpc-sdk/21.1/nvhpc_2021_211_Linux_ppc64le_cuda_11.2.tar.gz'),
        'Linux-x86_64': ('e021bb3d99873613edb9dba93a2e19e9a13de42349ee4b4775cd4d09af89d379', 'https://developer.download.nvidia.com/hpc-sdk/21.1/nvhpc_2021_211_Linux_x86_64_cuda_11.2.tar.gz')},
    '20.11': {
        'Linux-aarch64': ('f55dc668cff037c6fce27c2d7e09c3091fbe975aeaf74c03989a73763b25968f', 'https://developer.download.nvidia.com/hpc-sdk/20.11/nvhpc_2020_2011_Linux_aarch64_cuda_11.1.tar.gz'),
        'Linux-ppc64le': ('4f1272054c8c2008cbe864b5d43e1a050c09fb4d6d651c1c6708c428b70eee3d', 'https://developer.download.nvidia.com/hpc-sdk/20.11/nvhpc_2020_2011_Linux_ppc64le_cuda_11.1.tar.gz'),
        'Linux-x86_64': ('eeba5d8aa6b6b0ffdfa9cc7b96d5df53581c5c7061c5d71e049ba7c2a9d3585a', 'https://developer.download.nvidia.com/hpc-sdk/20.11/nvhpc_2020_2011_Linux_x86_64_cuda_11.1.tar.gz')},
    '20.9': {
        'Linux-aarch64': ('3bfb3d17f5ee99998bcc30d738e818d3b94b828e2d8da7db48bf152a01e22023', 'https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_aarch64_cuda_11.0.tar.gz'),
        'Linux-ppc64le': ('7e34a3d136644dbb4c5a911352a74945aceeb0aa4f91634ae755d53223e46172', 'https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_ppc64le_cuda_11.0.tar.gz'),
        'Linux-x86_64': ('8fa07d762e1b48155f3d531a16b8fffeb6f28b9d8a0033a1f2ba47fdb16ffd58', 'https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_x86_64_cuda_11.0.tar.gz')},
    '20.7': {
        'Linux-aarch64': ('5b83ca1919199ac0aa609309b31c345c5a6453dd3131fddeef9e3ee9059a0e9b', 'https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_aarch64_cuda_11.0.tar.gz'),
        # ppc64le 20.7 download is unavailable.
        'Linux-x86_64': ('ec5a385650194b4213bce53f3766089656916e28e38df3aa3882ff35667b0be2', 'https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_x86_64_cuda_11.0.tar.gz')}
}


class NvhpcSlim(Package):
    """The NVIDIA HPC SDK is a comprehensive suite of compilers, libraries
    and tools essential to maximizing developer productivity and the
    performance and portability of HPC applications. The NVIDIA HPC
    SDK C, C++, and Fortran compilers support GPU acceleration of HPC
    modeling and simulation applications with standard C++ and
    Fortran, OpenACC directives, and CUDA. GPU-accelerated math
    libraries maximize performance on common HPC algorithms, and
    optimized communications libraries enable standards-based
    multi-GPU and scalable systems programming. Performance profiling
    and debugging tools simplify porting and optimization of HPC
    applications. This package provides a single CUDA version."""

    homepage = "https://developer.nvidia.com/hpc-sdk"

    maintainers = ['samcmill']
    tags = ['e4s']

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])

    variant('blas',         default=True,
            description="Enable BLAS")
    variant('install_type', default='single',
            values=('single', 'network'), multi=False,
            description='Network installs are for installations shared '
                        'by different operating systems')
    variant('lapack',       default=True,
            description="Enable LAPACK")
    variant('mpi',          default=False,
            description="Enable MPI")

    provides('blas',        when='+blas')
    provides('lapack',      when='+lapack')
    provides('mpi',         when='+mpi')

    def install(self, spec, prefix):
        # Enable the silent installation feature
        os.environ['NVHPC_SILENT'] = "true"
        os.environ['NVHPC_ACCEPT_EULA'] = "accept"
        os.environ['NVHPC_INSTALL_DIR'] = prefix

        if spec.variants['install_type'].value == 'network':
            os.environ['NVHPC_INSTALL_TYPE'] = "network"
            os.environ['NVHPC_INSTALL_LOCAL_DIR'] = \
                "%s/%s/%s/share_objects" % \
                (prefix, 'Linux_%s' % spec.target.family, self.version)
        else:
            os.environ['NVHPC_INSTALL_TYPE'] = "single"

        # Run install script
        os.system("./install")

    def setup_run_environment(self, env):
        prefix = Prefix(join_path(self.prefix,
                                  'Linux_%s' % self.spec.target.family,
                                  self.version, 'compilers'))

        env.set('CC',  join_path(prefix.bin, 'nvc'))
        env.set('CXX', join_path(prefix.bin, 'nvc++'))
        env.set('F77', join_path(prefix.bin, 'nvfortran'))
        env.set('FC',  join_path(prefix.bin, 'nvfortran'))

        env.prepend_path('PATH',            prefix.bin)
        env.prepend_path('LIBRARY_PATH',    prefix.lib)
        env.prepend_path('LD_LIBRARY_PATH', prefix.lib)
        env.prepend_path('MANPATH',         prefix.man)

        if '+mpi' in self.spec:
            mpi_prefix = Prefix(join_path(self.prefix,
                                          'Linux_%s' % self.spec.target.family,
                                          self.version, 'comm_libs', 'mpi'))
            env.prepend_path('PATH', mpi_prefix.bin)
            env.prepend_path('LD_LIBRARY_PATH', mpi_prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = Prefix(join_path(self.prefix,
                                  'Linux_%s' % self.spec.target.family,
                                  self.version, 'compilers'))

        env.prepend_path('LIBRARY_PATH',    prefix.lib)
        env.prepend_path('LD_LIBRARY_PATH', prefix.lib)

        if '+mpi' in self.spec:
            mpi_prefix = Prefix(join_path(self.prefix,
                                          'Linux_%s' % self.spec.target.family,
                                          self.version, 'comm_libs', 'mpi'))

            env.prepend_path('LD_LIBRARY_PATH', mpi_prefix.lib)

    def setup_dependent_package(self, module, dependent_spec):
        if '+mpi' in self.spec or self.provides('mpi'):
            mpi_prefix = Prefix(join_path(self.prefix,
                                          'Linux_%s' % self.spec.target.family,
                                          self.version, 'comm_libs', 'mpi'))

            self.spec.mpicc  = join_path(mpi_prefix.bin, 'mpicc')
            self.spec.mpicxx = join_path(mpi_prefix.bin, 'mpicxx')
            self.spec.mpif77 = join_path(mpi_prefix.bin, 'mpif77')
            self.spec.mpifc  = join_path(mpi_prefix.bin, 'mpif90')

    @property
    def libs(self):
        prefix = Prefix(join_path(self.prefix,
                                  'Linux_%s' % self.spec.target.family,
                                  self.version, 'compilers'))
        libs = []

        if '+blas' in self.spec:
            libs.append('libblas')

        if '+lapack' in self.spec:
            libs.append('liblapack')
            libs.append('libnvf')

        return find_libraries(libs, root=prefix, recursive=True)
