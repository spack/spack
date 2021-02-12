# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFsspec(PythonPackage):
    """A specification for pythonic filesystems."""

    homepage = "https://github.com/intake/filesystem_spec"
    pypi = "fsspec/fsspec-0.4.4.tar.gz"

    version('0.8.5', sha256='890c6ce9325030f03bd2eae81389ddcbcee53bdd475334ca064595e1e45f92a6')
    version('0.8.4', sha256='e1e494d4814f6804769f3c7bfd7a722a15113cc0339d14755297f09306b8f21f')
    version('0.8.3', sha256='aad96c98b7f73bc437bb024e7cb3b0943c61049f95d6c5edec5b8b8850fd0875')
    version('0.8.2', sha256='c08fbbb517d1c550be38ae0eba26b0b39b2b656617396ecce8c9ccd1a107c0ee')
    version('0.8.1', sha256='2e1104cc95126020cb2cf5bdd8d64f78c8a8f84783652e26a1e0661f31fe2564')
    version('0.8.0', sha256='176f3fc405471af0f1f1e14cffa3d53ab8906577973d068b976114433c010d9d')
    version('0.7.4', sha256='7075fde6d617cd3a97eac633d230d868121a188a46d16a0dcb484eea0cf2b955')
    version('0.7.3', sha256='1b540552c93b47e83c568e87507d6e02993e6d1b30bc7285f2336c81c5014103')
    version('0.4.4', sha256='97697a46e8bf8be34461c2520d6fc4bfca0ed749b22bb2b7c21939fd450a7d63')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'), when='@0.6.3:')
    depends_on('py-setuptools', type='build')
