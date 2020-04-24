# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sd(CargoPackage):
    """An intuitive find & replace CLI"""

    homepage  = "https://github.com/chmln/sd"
    crates_io = "sd"
    git       = "https://github.com/chmln/sd.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.7.4', sha256='03dcb91467c19f3974995b5fff99aed5e073d35571ef0acabd1ef5bc4e62186b')
    version('0.7.2', sha256='95cfa8ccebd8f5ad53cf4c4ab660f58b33bb164e2502fcc1e2c0b9b6b245cfc1')
    version('0.7.1', sha256='68eabdf638f50cc23b6af62c10c2d9cb6c4eb7e017bb0de3df54afe66892bbd9')
    version('0.7.0', sha256='6b7b4b3de1d7fa432f6204531e9bb2e61e4bab98ff9fcaf355c4b7173f1be0d6')
    version('0.6.5', sha256='cad11ac08ea693cd526608095cff8a1d3cee52627b59c9d6c0bb4546880fdf48')
    version('0.6.4', sha256='8583f636e01a08a348fd42a2c3e4159cf8b0683fa4ef4f7f2361260d5dd5a2d6')
    version('0.6.3', sha256='f7a9199b4da377fcffe6e1a0bec3d29562156eca0a853a148e4324d84d40a043')
    version('0.6.2', sha256='e607b78d2310f0be885a2ee405e9f011555d4676c5f5e3e36858378be8ebc425')
    version('0.6.1', sha256='d76cb9c0072bab2a4717fb0e1ba5324882dada5c6a567ea85a82c582963630de')
    version('0.6.0', sha256='40e68429303ebc705545dd96842dd96bf65079025199604f1133fce914a1b75b')
    version('0.5.0', sha256='30d506059be0f877e75f97bc7395401af6da4751d5505bad06b48d4c972a52c3')
    version('0.4.3', sha256='7527dd73d32cbd325793c20f5c5c9cb0d5004ba293b8452e4039fa7c1e83cd4e')
    version('0.4.2', sha256='ccdaddd1b10f187a17b5080b07a636bdddc7fe80c057d3c87efe2c020cf9c0e1')
    version('0.4.1', sha256='820ecd913d682303cb873347e5ed955e89ceab657f01e60a5388b91efdb3883e')
    version('0.4.0', sha256='b82717f00424c59f6c0a9b2cc8c9e37c876ee714a174e56aabed0013b935718a')
    version('0.3.0', sha256='2b19f997eabd83ce2c0542e2bda434a7b3778b7c6bc885acea47f1976307fbcf')
    version('0.2.0', sha256='4d2a27ca39e38752c0005f6220aecafeeb95a321bdcdf41645e19cff02324d8b')
    version('0.1.1', sha256='b64bcc1a8cefe7bd1f577f709f6df096410f9cc8858c5f5e9775625208198b44')
    version('0.1.0', sha256='d0d1e6da5e134601e3f537f7ec866077cc5f97e368702a039d823d806be17e9e')
