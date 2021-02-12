# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import platform

_versions = {
    'v5.2.1': {
        'Linux-aarch64': ('d2ac1669154ec27b794b64d026ad09caecee6e5e17fd35107595a7517711d2b9', 'https://github.com/kunpengcompute/hyperscan/archive/v5.2.1.aarch64.tar.gz'),
        'Linux-x86_64': ('fd879e4ee5ecdd125e3a79ef040886978ae8f1203832d5a3f050c48f17eec867', 'https://github.com/intel/hyperscan/archive/v5.2.1.tar.gz')
    }
}


class Hyperscan(CMakePackage):
    """High-performance regular expression matching library."""

    homepage = "https://www.hyperscan.io/"
    url      = "https://github.com/intel/hyperscan/archive/v5.2.1.tar.gz"

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version('5.4.0', sha256='e51aba39af47e3901062852e5004d127fa7763b5dbbc16bcca4265243ffa106f')
    version('5.3.0', sha256='9b50e24e6fd1e357165063580c631a828157d361f2f27975c5031fc00594825b')
    version('5.2.1', sha256='fd879e4ee5ecdd125e3a79ef040886978ae8f1203832d5a3f050c48f17eec867')
    version('5.2.0', sha256='bb02118efe7e93df5fc24296406dfd0c1fa597176e0c211667152cd4e89d9d85')
    version('5.1.1', sha256='e3bb509d4002f2d75e1804e754efa6334316d1ee110a3b85c8156c08fe5e2369')
    version('5.1.0', sha256='c751e85a537bc2cebb699f42a66faaf42edf10468f0315cb0719d2051eefa4d8')
    version('5.0.0', sha256='f2bdebff62a2fc0b974b309da7be4959869fb7cababe1169b7693cfd672c2fe0')
    version('4.7.0', sha256='a0c07b48ae80903001ab216b03fdf6359bfd5777b2976de728947725b335e941')
    version('4.6.0', sha256='0dfbfc2e5e82a6a7b2feca3d982d08fb7d4a979a4e75f667a37484cae4fda815')
    version('4.5.2', sha256='1f8fa44e94b642e54edc6a74cb8117d01984c0e661a15cad5a785e3ba28d18f5')
    version(ver, sha256=pkg[0], url=pkg[1])

    depends_on('boost')
    depends_on('pcre')
    depends_on('ragel', type='build')
