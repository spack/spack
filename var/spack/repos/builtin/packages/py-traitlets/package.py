# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTraitlets(PythonPackage):
    """Traitlets Python config system"""

    homepage = "https://pypi.python.org/pypi/traitlets"
    url      = "https://github.com/ipython/traitlets/archive/4.3.1.tar.gz"

    version('4.3.3', sha256='b686c1aadf6ee5a9ee4c22df23bc5cd5bb7b5cfa18afe092e0a139cc2f05fe2e')
    version('4.3.2', sha256='370f938ad730d52272ef74f96f831cb21138f6168e46fe582fe256c35cc656ce')
    version('4.3.1', sha256='3d50b2968f2e1477bd0de4b9656df40fd5624fc85cd1fc15f6c885cd68a4f6a1')
    version('4.3.0', sha256='2f6cbc367fb56cbde91b2585202ef0a5bd41ae205a70aeecca1aeb4cb5b64e66')
    version('4.2.2', sha256='bc749e08dd89c6007eb70e98c958f16d41e9a1fa42fdc9e9ba24e67469efa0ef')
    version('4.2.1', sha256='a9ea45313f7130c555d8c1832529bf3f522ffc584093436783bc4b9611e8c4a9')
    version('4.2.0', sha256='923cbe84bef30c27d2083f014f23a5da0ebe7da2e67a683d97acb07002e2ce0d')
    version('4.1.0', sha256='93ead8dbf7e9617c88b79620072bfc499e7f25613f3df2234e5fdf08348c0a83')
    version('4.0.0', sha256='03f380cb2e47689ae55dbe9a5dccbdde5cad8c4637312d720f4c3a991fb15cd2')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-decorator', type=('build', 'run'))
    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-enum34', when='^python@:3.3', type=('build', 'run'))
