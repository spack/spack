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
# TODO: switch to single-CUDA tarballs
_versions = {
    '22.2': {
        'Linux-aarch64': ('a8241d1139a768d9a0066d1853748160e4098253024e17e997983884d0d33a19', 'https://developer.download.nvidia.com/hpc-sdk/22.2/nvhpc_2022_222_Linux_aarch64_cuda_multi.tar.gz'),
        'Linux-ppc64le': ('f84f72423452968d5bbe02e297f188682c4759864a736a72b32acb3433db3a26', 'https://developer.download.nvidia.com/hpc-sdk/22.2/nvhpc_2022_222_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('8dfb4007d6912b2722946358ac69409592c1f03426d81971ffbcb6fc5fea2cb8', 'https://developer.download.nvidia.com/hpc-sdk/22.2/nvhpc_2022_222_Linux_x86_64_cuda_multi.tar.gz')},
    '22.1': {
        'Linux-aarch64': ('05cfa8c520a34eab01272a261b157d421a9ff7129fca7d859b944ce6a16d2255', 'https://developer.download.nvidia.com/hpc-sdk/22.1/nvhpc_2022_221_Linux_aarch64_cuda_multi.tar.gz'),
        'Linux-ppc64le': ('9fa9b64fba2c9b287b5800693417d8065c695d18cab0526bad41d9aecc8be2b3', 'https://developer.download.nvidia.com/hpc-sdk/22.1/nvhpc_2022_221_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('7e4366509ed9031ff271e73327dd3121909902a81ac436307801a5373efaff5e', 'https://developer.download.nvidia.com/hpc-sdk/22.1/nvhpc_2022_221_Linux_x86_64_cuda_multi.tar.gz')},
    '21.11': {
        'Linux-aarch64': ('3b11bcd9cca862fabfce1e7bcaa2050ea12130c7e897f4e7859ba4c155d20720', 'https://developer.download.nvidia.com/hpc-sdk/21.11/nvhpc_2021_2111_Linux_aarch64_cuda_multi.tar.gz'),
        'Linux-ppc64le': ('ac51ed92de4eb5e1bdb064ada5bbace5b89ac732ad6c6473778edfb8d29a6527', 'https://developer.download.nvidia.com/hpc-sdk/21.11/nvhpc_2021_2111_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('d8d8ccd0e558d22bcddd955f2233219c96f7de56aa8e09e7be833e384d32d6aa', 'https://developer.download.nvidia.com/hpc-sdk/21.11/nvhpc_2021_2111_Linux_x86_64_cuda_multi.tar.gz')},
    '21.9': {
        'Linux-aarch64': ('52c2c66e30043add4afccedf0ba77daa0000bf42e0db844baa630bb635b91a7d', 'https://developer.download.nvidia.com/hpc-sdk/21.9/nvhpc_2021_219_Linux_aarch64_cuda_multi.tar.gz'),
        'Linux-ppc64le': ('cff0b55fb782be1982bfeec1d9763b674ddbf84ff2c16b364495299266320289', 'https://developer.download.nvidia.com/hpc-sdk/21.9/nvhpc_2021_219_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('7de6a6880fd7e59afe0dee51f1fae4d3bff1ca0fb8ee234b24e1f2fdff23ffc9', 'https://developer.download.nvidia.com/hpc-sdk/21.9/nvhpc_2021_219_Linux_x86_64_cuda_multi.tar.gz')},
    '21.7': {
        'Linux-aarch64': ('73eb3513845b59645f118b1e313472f54519dc252d5f5c32a05df2a2a8a19878', 'https://developer.download.nvidia.com/hpc-sdk/21.7/nvhpc_2021_217_Linux_aarch64_cuda_multi.tar.gz'),
        'Linux-ppc64le': ('37ea23b5a9c696fb3fdb82855643afc4e02aea618102ec801206441f10fc9fba', 'https://developer.download.nvidia.com/hpc-sdk/21.7/nvhpc_2021_217_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('49d6e23492d131474698cf12971722d42e13a54a4eddec382e66e1053b4ac902', 'https://developer.download.nvidia.com/hpc-sdk/21.7/nvhpc_2021_217_Linux_x86_64_cuda_multi.tar.gz')},
    '21.5': {
        'Linux-aarch64': ('1a1748cd7cf538199d92ab3b1208935fa4a62708ba21125aeadb328ddc7380d4', 'https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_aarch64_cuda_multi.tar.gz'),
        'Linux-ppc64le': ('4674931a5ce28724308cb9cebd546eefa3f0646d3d08adbea28ba5ad27f0c163', 'https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('21989e52c58a6914743631c8200de1fec7e10b3449c6c1833f3032ee74b85f8e', 'https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_x86_64_cuda_multi.tar.gz')},
    '21.3': {
        'Linux-aarch64': ('88e0dbf8fcdd06a2ba06aacf65ae1625b8683688f6593ed3bf8ce129ce1b17b7', 'https://developer.download.nvidia.com/hpc-sdk/21.3/nvhpc_2021_213_Linux_aarch64_cuda_multi.tar.gz'),
        'Linux-ppc64le': ('08cd0cd6c80d633f107b44f88685ada7f014fbf6eac19ef5ae4a7952cabe4037', 'https://developer.download.nvidia.com/hpc-sdk/21.3/nvhpc_2021_213_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('391d5604a70f61bdd4ca6a3e4692f6f2391948990c8a35c395b6867341890031', 'https://developer.download.nvidia.com/hpc-sdk/21.3/nvhpc_2021_213_Linux_x86_64_cuda_multi.tar.gz')},
    '21.2': {
        'Linux-aarch64': ('fe19c0232f7c9534f8699b7432483c9cc649f1e92e7f0961d1aa7c54d83297ff', 'https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_aarch64_cuda_multi.tar.gz'),
        'Linux-ppc64le': ('6b69b6e4ebec6a91b9f1627384c50adad79ebdd25dfb20a5f64cf01c3a07f11a', 'https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('a3e3393040185ae844002fbc6c8eb4ffdfb97ce8b2ce29d796fe7e9a521fdc59', 'https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_x86_64_cuda_multi.tar.gz')},
    '21.1': {
        'Linux-aarch64': ('b276e7c0ff78cee837a597d9136cd1d8ded27a9d1fdae1e7d674e2a072a9a6aa', 'https://developer.download.nvidia.com/hpc-sdk/21.1/nvhpc_2021_211_Linux_aarch64_cuda_multi.tar.gz'),
        'Linux-ppc64le': ('bc236c212097bac6b7d04d627d9cc6b75bb6cd473a0b6a1bf010559ce328a2b0', 'https://developer.download.nvidia.com/hpc-sdk/21.1/nvhpc_2021_211_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('d529daf46404724ac3f005be4239f2c30e53f5220bb9453f367dccc3a74d6b41', 'https://developer.download.nvidia.com/hpc-sdk/21.1/nvhpc_2021_211_Linux_x86_64_cuda_multi.tar.gz')},
    '20.11': {
        'Linux-aarch64': ('2f26ca45b07b694b8669e4f761760d4f7faa8d032b21e430adee1af0a27032c1', 'https://developer.download.nvidia.com/hpc-sdk/20.11/nvhpc_2020_2011_Linux_aarch64_cuda_multi.tar.gz'),
        'Linux-ppc64le': ('99e5a5437e82f3914e0fe81feb761a5b599a3fe8b31f3c2cac8ae47e8cdc7b0f', 'https://developer.download.nvidia.com/hpc-sdk/20.11/nvhpc_2020_2011_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('c80fc26e5ba586696f7030f03054c1aaca0752a891c7923faf47eb23b66857ec', 'https://developer.download.nvidia.com/hpc-sdk/20.11/nvhpc_2020_2011_Linux_x86_64_cuda_multi.tar.gz')},
    '20.9': {
        'Linux-aarch64': ('3bfb3d17f5ee99998bcc30d738e818d3b94b828e2d8da7db48bf152a01e22023', 'https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_aarch64_cuda_11.0.tar.gz'),
        'Linux-ppc64le': ('b2966d4047e1dfd981ce63b333ab9c0acbdc2a6a505fa217456ac9fa3b8e7474', 'https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('fe665ab611b03846a90bd70ca4e08c1e59ab527364b971ed0304e0ae73c778d8', 'https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_x86_64_cuda_multi.tar.gz')},
    '20.7': {
        'Linux-aarch64': ('5b83ca1919199ac0aa609309b31c345c5a6453dd3131fddeef9e3ee9059a0e9b', 'https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_aarch64_cuda_11.0.tar.gz'),
        'Linux-ppc64le': ('800ead240bdf61611910b2f6df24ee1d7359377ff3767c923738dd81fcea9312', 'https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_ppc64le_cuda_multi.tar.gz'),
        'Linux-x86_64': ('a5c5c8726d2210f2310a852c6d6e03c9ef8c75e3643e9c94e24909f5e9c2ea7a', 'https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_x86_64_cuda_multi.tar.gz')}
}
# Multi-CUDA tarball links
#_versions = {
#    '22.2': {
#        'Linux-aarch64': ('a8241d1139a768d9a0066d1853748160e4098253024e17e997983884d0d33a19', 'https://developer.download.nvidia.com/hpc-sdk/22.2/nvhpc_2022_222_Linux_aarch64_cuda_multi.tar.gz'),
#        'Linux-ppc64le': ('f84f72423452968d5bbe02e297f188682c4759864a736a72b32acb3433db3a26', 'https://developer.download.nvidia.com/hpc-sdk/22.2/nvhpc_2022_222_Linux_ppc64le_cuda_multi.tar.gz'),
#        'Linux-x86_64': ('8dfb4007d6912b2722946358ac69409592c1f03426d81971ffbcb6fc5fea2cb8', 'https://developer.download.nvidia.com/hpc-sdk/22.2/nvhpc_2022_222_Linux_x86_64_cuda_multi.tar.gz')},
#    '22.1': {
#        'Linux-aarch64': ('05cfa8c520a34eab01272a261b157d421a9ff7129fca7d859b944ce6a16d2255', 'https://developer.download.nvidia.com/hpc-sdk/22.1/nvhpc_2022_221_Linux_aarch64_cuda_multi.tar.gz'),
#        'Linux-ppc64le': ('9fa9b64fba2c9b287b5800693417d8065c695d18cab0526bad41d9aecc8be2b3', 'https://developer.download.nvidia.com/hpc-sdk/22.1/nvhpc_2022_221_Linux_ppc64le_cuda_multi.tar.gz'),
#        'Linux-x86_64': ('7e4366509ed9031ff271e73327dd3121909902a81ac436307801a5373efaff5e', 'https://developer.download.nvidia.com/hpc-sdk/22.1/nvhpc_2022_221_Linux_x86_64_cuda_multi.tar.gz')},
#    '21.11': {
#        'Linux-aarch64': ('3b11bcd9cca862fabfce1e7bcaa2050ea12130c7e897f4e7859ba4c155d20720', 'https://developer.download.nvidia.com/hpc-sdk/21.11/nvhpc_2021_2111_Linux_aarch64_cuda_multi.tar.gz'),
#        'Linux-ppc64le': ('ac51ed92de4eb5e1bdb064ada5bbace5b89ac732ad6c6473778edfb8d29a6527', 'https://developer.download.nvidia.com/hpc-sdk/21.11/nvhpc_2021_2111_Linux_ppc64le_cuda_multi.tar.gz'),
#        'Linux-x86_64': ('d8d8ccd0e558d22bcddd955f2233219c96f7de56aa8e09e7be833e384d32d6aa', 'https://developer.download.nvidia.com/hpc-sdk/21.11/nvhpc_2021_2111_Linux_x86_64_cuda_multi.tar.gz')},
#    '21.9': {
#        'Linux-aarch64': ('52c2c66e30043add4afccedf0ba77daa0000bf42e0db844baa630bb635b91a7d', 'https://developer.download.nvidia.com/hpc-sdk/21.9/nvhpc_2021_219_Linux_aarch64_cuda_multi.tar.gz'),
#        'Linux-ppc64le': ('cff0b55fb782be1982bfeec1d9763b674ddbf84ff2c16b364495299266320289', 'https://developer.download.nvidia.com/hpc-sdk/21.9/nvhpc_2021_219_Linux_ppc64le_cuda_multi.tar.gz'),
#        'Linux-x86_64': ('7de6a6880fd7e59afe0dee51f1fae4d3bff1ca0fb8ee234b24e1f2fdff23ffc9', 'https://developer.download.nvidia.com/hpc-sdk/21.9/nvhpc_2021_219_Linux_x86_64_cuda_multi.tar.gz')},
#    '21.7': {
#        'Linux-aarch64': ('73eb3513845b59645f118b1e313472f54519dc252d5f5c32a05df2a2a8a19878', 'https://developer.download.nvidia.com/hpc-sdk/21.7/nvhpc_2021_217_Linux_aarch64_cuda_multi.tar.gz'),
#        'Linux-ppc64le': ('37ea23b5a9c696fb3fdb82855643afc4e02aea618102ec801206441f10fc9fba', 'https://developer.download.nvidia.com/hpc-sdk/21.7/nvhpc_2021_217_Linux_ppc64le_cuda_multi.tar.gz'),
#        'Linux-x86_64': ('49d6e23492d131474698cf12971722d42e13a54a4eddec382e66e1053b4ac902', 'https://developer.download.nvidia.com/hpc-sdk/21.7/nvhpc_2021_217_Linux_x86_64_cuda_multi.tar.gz')},
#    '21.5': {
#        'Linux-aarch64': ('1a1748cd7cf538199d92ab3b1208935fa4a62708ba21125aeadb328ddc7380d4', 'https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_aarch64_cuda_multi.tar.gz'),
#        'Linux-ppc64le': ('4674931a5ce28724308cb9cebd546eefa3f0646d3d08adbea28ba5ad27f0c163', 'https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_ppc64le_cuda_multi.tar.gz'),
#        'Linux-x86_64': ('21989e52c58a6914743631c8200de1fec7e10b3449c6c1833f3032ee74b85f8e', 'https://developer.download.nvidia.com/hpc-sdk/21.5/nvhpc_2021_215_Linux_x86_64_cuda_multi.tar.gz')},
#    '21.3': {
#        'Linux-aarch64': ('88e0dbf8fcdd06a2ba06aacf65ae1625b8683688f6593ed3bf8ce129ce1b17b7', 'https://developer.download.nvidia.com/hpc-sdk/21.3/nvhpc_2021_213_Linux_aarch64_cuda_multi.tar.gz'),
#        'Linux-ppc64le': ('08cd0cd6c80d633f107b44f88685ada7f014fbf6eac19ef5ae4a7952cabe4037', 'https://developer.download.nvidia.com/hpc-sdk/21.3/nvhpc_2021_213_Linux_ppc64le_cuda_multi.tar.gz'),
#        'Linux-x86_64': ('391d5604a70f61bdd4ca6a3e4692f6f2391948990c8a35c395b6867341890031', 'https://developer.download.nvidia.com/hpc-sdk/21.3/nvhpc_2021_213_Linux_x86_64_cuda_multi.tar.gz')},
#    '21.2': {
#        'Linux-aarch64': ('fe19c0232f7c9534f8699b7432483c9cc649f1e92e7f0961d1aa7c54d83297ff', 'https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_aarch64_cuda_multi.tar.gz'),
#        'Linux-ppc64le': ('6b69b6e4ebec6a91b9f1627384c50adad79ebdd25dfb20a5f64cf01c3a07f11a', 'https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_ppc64le_cuda_multi.tar.gz'),
#        'Linux-x86_64': ('a3e3393040185ae844002fbc6c8eb4ffdfb97ce8b2ce29d796fe7e9a521fdc59', 'https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_x86_64_cuda_multi.tar.gz')},
#    '21.1': {
#        'Linux-aarch64': ('b276e7c0ff78cee837a597d9136cd1d8ded27a9d1fdae1e7d674e2a072a9a6aa', 'https://developer.download.nvidia.com/hpc-sdk/21.1/nvhpc_2021_211_Linux_aarch64_cuda_multi.tar.gz'),
#        'Linux-ppc64le': ('bc236c212097bac6b7d04d627d9cc6b75bb6cd473a0b6a1bf010559ce328a2b0', 'https://developer.download.nvidia.com/hpc-sdk/21.1/nvhpc_2021_211_Linux_ppc64le_cuda_multi.tar.gz'),
#        'Linux-x86_64': ('d529daf46404724ac3f005be4239f2c30e53f5220bb9453f367dccc3a74d6b41', 'https://developer.download.nvidia.com/hpc-sdk/21.1/nvhpc_2021_211_Linux_x86_64_cuda_multi.tar.gz')},
#    '20.11': {
#        'Linux-aarch64': ('2f26ca45b07b694b8669e4f761760d4f7faa8d032b21e430adee1af0a27032c1', 'https://developer.download.nvidia.com/hpc-sdk/20.11/nvhpc_2020_2011_Linux_aarch64_cuda_multi.tar.gz'),
#        'Linux-ppc64le': ('99e5a5437e82f3914e0fe81feb761a5b599a3fe8b31f3c2cac8ae47e8cdc7b0f', 'https://developer.download.nvidia.com/hpc-sdk/20.11/nvhpc_2020_2011_Linux_ppc64le_cuda_multi.tar.gz'),
#        'Linux-x86_64': ('c80fc26e5ba586696f7030f03054c1aaca0752a891c7923faf47eb23b66857ec', 'https://developer.download.nvidia.com/hpc-sdk/20.11/nvhpc_2020_2011_Linux_x86_64_cuda_multi.tar.gz')},
#    '20.9': {
#        'Linux-aarch64': ('3bfb3d17f5ee99998bcc30d738e818d3b94b828e2d8da7db48bf152a01e22023', 'https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_aarch64_cuda_11.0.tar.gz'),
#        'Linux-ppc64le': ('b2966d4047e1dfd981ce63b333ab9c0acbdc2a6a505fa217456ac9fa3b8e7474', 'https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_ppc64le_cuda_multi.tar.gz'),
#        'Linux-x86_64': ('fe665ab611b03846a90bd70ca4e08c1e59ab527364b971ed0304e0ae73c778d8', 'https://developer.download.nvidia.com/hpc-sdk/20.9/nvhpc_2020_209_Linux_x86_64_cuda_multi.tar.gz')},
#    '20.7': {
#        'Linux-aarch64': ('5b83ca1919199ac0aa609309b31c345c5a6453dd3131fddeef9e3ee9059a0e9b', 'https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_aarch64_cuda_11.0.tar.gz'),
#        'Linux-ppc64le': ('800ead240bdf61611910b2f6df24ee1d7359377ff3767c923738dd81fcea9312', 'https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_ppc64le_cuda_multi.tar.gz'),
#        'Linux-x86_64': ('a5c5c8726d2210f2310a852c6d6e03c9ef8c75e3643e9c94e24909f5e9c2ea7a', 'https://developer.download.nvidia.com/hpc-sdk/20.7/nvhpc_2020_207_Linux_x86_64_cuda_multi.tar.gz')}
#}


class Nvhpc(Package):
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
    applications."""

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
#    variant('cuda',         default=False,
#            description="Enable CUDA hooks")
#    variant('nccl',         default=False,
#            description="Enable NCCL hooks")

    provides('blas',        when='+blas')
    provides('lapack',      when='+lapack')
    provides('mpi',         when='+mpi')

    # TODO: TEST THIS THOROUGHLY
#    depends_on('cuda',      when='+cuda')
#    depends_on('nccl',      when='+nccl')

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

#        if '+cuda' in self.spec:
#            cuda_prefix = Prefix(join_path(self.prefix,
#                                           'Linux_%s' % self.spec.target.family,
#                                           self.version, 'cuda'))
#            math_prefix = Prefix(join_path(self.prefix,
#                                           'Linux_%s' % self.spec.target.family,
#                                           self.version, 'math_libs'))
#            env.prepend_path('CUDA_HOME', cuda_prefix)
#            env.prepend_path('PATH', cuda_prefix.bin)
#            env.prepend_path('LD_LIBRARY_PATH', cuda_prefix.lib64)
#            env.prepend_path('LD_LIBRARY_PATH', math_prefix.lib64)

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


#        if '+cuda' in self.spec:
#            cuda_prefix = Prefix(join_path(self.prefix,
#                                           'Linux_%s' % self.spec.target.family,
#                                           self.version, 'cuda'))
#            math_prefix = Prefix(join_path(self.prefix,
#                                           'Linux_%s' % self.spec.target.family,
#                                           self.version, 'math_libs'))
#            env.prepend_path('CUDA_HOME', cuda_prefix)
#            env.prepend_path('PATH', cuda_prefix.bin)
#            env.prepend_path('LD_LIBRARY_PATH', cuda_prefix.lib64)
#            env.prepend_path('LD_LIBRARY_PATH', math_prefix.lib64)
#            env.set('CUDAHOSTCXX', dependent_spec.package.compiler.cxx)

    def setup_dependent_package(self, module, dependent_spec):
        if '+mpi' in self.spec or self.provides('mpi'):
            mpi_prefix = Prefix(join_path(self.prefix,
                                          'Linux_%s' % self.spec.target.family,
                                          self.version, 'comm_libs', 'mpi'))

            self.spec.mpicc  = join_path(mpi_prefix.bin, 'mpicc')
            self.spec.mpicxx = join_path(mpi_prefix.bin, 'mpicxx')
            self.spec.mpif77 = join_path(mpi_prefix.bin, 'mpif77')
            self.spec.mpifc  = join_path(mpi_prefix.bin, 'mpif90')

#        if '+cuda' in self.spec or self.provides('cuda'):
#            cuda_prefix = Prefix(join_path(self.prefix,
#                                           'Linux_%s' % self.spec.target.family,
#                                           self.version, 'cuda'))
#            math_prefix = Prefix(join_path(self.prefix,
#                                           'Linux_%s' % self.spec.target.family,
#                                           self.version, 'math_libs'))
#            self.spec.cuda_home = cuda_prefix
#            self.spec.nvcc = join_path(cuda_prefix.bin, 'nvcc')
#            self.spec.math_libs_path = math_prefix
#            self.spec.math_libs = ['cublas', 'cufft', 'curand', 'cusolver',
#                                   'cusparse', 'cutensor', 'metis', 'nvblas']

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

        pfxlibs = find_libraries(libs, root=prefix, recursive=True)
        return pfxlibs

#        # The following block is adapted from 'cuda' spec
#        if '+cuda' in self.spec:
#            cuda_prefix = Prefix(join_path(self.prefix,
#                                           'Linux_%s' % self.spec.target.family,
#                                           self.version, 'cuda'))
#            math_prefix = Prefix(join_path(self.prefix,
#                                           'Linux_%s' % self.spec.target.family,
#                                           self.version, 'math_libs'))
#            cuda_libs = find_libraries('libcudart', root=cuda_prefix,
#                                       shared=True, recursive=True)
#            filtered_libs = []
#            # CUDA 10.0 provides Compatibility libraries for running newer
#            # versions of CUDA with older drivers. These do not work with newer
#            # drivers.
#            for lib in cuda_libs:
#                parts = lib.split(os.sep)
#                if 'compat' not in parts and 'stubs' not in parts:
#                    filtered_libs.append(lib)
#            # Make sure to keep this list consistent with self.math_libs above
#            # (in setup_dependent_package)
#            math_libs_l = ['cublas', 'cufft', 'curand', 'cusolver',
#                           'cusparse', 'cutensor', 'metis', 'nvblas']
#            static_libs_l = ['metis']
#            math_libs = LibraryList('')
#            for lib in math_libs_l:
#                if lib in static_libs_l:
#                    lib = find_libraries(lib, root=math_prefix,
#                                         shared=False, recursive=True)
#                else:
#                    lib = find_libraries(lib, root=math_prefix,
#                                         shared=True, recursive=True)
#                # Compound assignment operation += isn't supported yet
#                math_libs = math_libs + lib
#            return pfxlibs + LibraryList(filtered_libs) + math_libs
#        else:


