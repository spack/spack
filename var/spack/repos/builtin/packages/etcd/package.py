# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import platform


class Etcd(Package):
    """etcd is a distributed reliable key-value store for the most
    critical data of a distributed system"""

    homepage = "https://etcd.io/"
    url      = "https://github.com/etcd-io/etcd/archive/v3.4.7.tar.gz"

    version('3.4.14', sha256='dec1f1adb2e35eebad28f09845b087d3fc1206881e7e645d6991ab28e97adea8')
    version('3.4.13', sha256='fc77c3949b5178373734c3b276eb2281c954c3cd2225ccb05cdbdf721e1f775a')
    version('3.4.12', sha256='7ae7152d35a606cc46a227836303246b53aa4d62a320972de4f71635b934a358')
    version('3.4.11', sha256='caf6e537211ff9459156bedfe5491b42d08633bc72dbd7521e4fb9971cd08f0f')
    version('3.4.10', sha256='ab105ada8a6f579c395b265a183bc7525644fe0c2c4c213dac94739991b1a573')
    version('3.4.9',  sha256='bfdcea0fc83c6d6edb70667a2272f8fc597c61976ecc6f8ecbfeb380ff02618b')
    version('3.4.7', sha256='858f5ad8c830a66f6bd0cd19386deea64d374185b32f40650ba979e0a70b8b97')
    version('3.4.6',  sha256='e9ebd003f5545a05017a8dbdde236d6c9d25f98ee35f8ba237e57b75330664f9')
    version('3.4.5',  sha256='2888f73dc52ba89da470d9bd40b1348ffe8b3da51cd8fe8bff5a1a8db2e50d46')
    version('3.4.4',  sha256='46bcd0d034fe9cc6ae86a9f2a72bdc78761ca99bfd5ae4b96b24e4ad93fc627e')
    version('3.3.20', sha256='a9fcd2a3343f7f5b99acae956dd7c4fe12f16772b660f16fa9c24368df002477')

    depends_on('go@:1.13.9')

    def setup_run_environment(self, env):
        if platform.machine() == 'aarch64':
            env.set('ETCD_UNSUPPORTED_ARCH', 'arm64')

    def setup_build_environment(self, env):
        if platform.machine() == 'aarch64':
            env.set('ETCD_UNSUPPORTED_ARCH', 'arm64')

    def install(self, spec, prefix):
        make()
        install_tree('bin', prefix.bin)
