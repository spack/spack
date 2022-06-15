# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFsspec(PythonPackage):
    """A specification for pythonic filesystems."""

    homepage = "https://github.com/intake/filesystem_spec"
    pypi = "fsspec/fsspec-0.4.4.tar.gz"

    version('2021.7.0', sha256='792ebd3b54de0b30f1ce73f0ba0a8bcc864724f2d9f248cb8d0ece47db0cbde8')
    version('2021.4.0', sha256='8b1a69884855d1a8c038574292e8b861894c3373282d9a469697a2b41d5289a6')
    version('0.9.0', sha256='3f7a62547e425b0b336a6ac2c2e6c6ac824648725bc8391af84bb510a63d1a56')
    version('0.8.0', sha256='176f3fc405471af0f1f1e14cffa3d53ab8906577973d068b976114433c010d9d')
    version('0.7.3', sha256='1b540552c93b47e83c568e87507d6e02993e6d1b30bc7285f2336c81c5014103')
    version('0.4.4', sha256='97697a46e8bf8be34461c2520d6fc4bfca0ed749b22bb2b7c21939fd450a7d63')

    variant('http', default=False, description='HTTPFileSystem support (Requires version 0.8.1+)')

    conflicts('+http', when='@:0.8.0', msg='Only available in 0.8.1+')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'), when='@0.6.3:')
    depends_on('py-setuptools', type='build')
    depends_on('py-requests', type=('build', 'run'), when='+http')
    depends_on('py-aiohttp',  type=('build', 'run'), when='+http')
