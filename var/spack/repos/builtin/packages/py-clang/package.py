# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyClang(PythonPackage):
    """Python bindings for clang from clang release branches"""

    homepage = "https://clang.llvm.org/"
    pypi     = "clang/clang-5.0.tar.gz"

    version('11.0',    sha256='f838e6475b1fe5c91efb97e80ae19420c39483fd5aa7ef10f03ffb51edc6f8c5')
    version('10.0.1',  sha256='c90eca387fede58e2398c4e211e2b38a310f5caa9adb367a8f84aa1ba2fe98b5')
    version('9.0',     sha256='8655709088313381063be5abce590994da9e7620fcab3bc4d5eb62519c89eebf')
    version('8.0.1',   sha256='aed3f52d5d268f9a83e3b99f0fe7b937e6746a65fab540e07481ea3258983ce1')
    version('7.1.0',   sha256='2fbd8a3c1dc1802ffc81766e9c7a85f4b8ebfa2a0b46d1953e8792b93fe07b4b')
    version('6.0.0.2', sha256='fea8d56f3f5f02f61c4c1160dbce0f4ff244b996993d35433124d4b505de8b79')
    version('6.0.0.1', sha256='27632ad73f2178a3d92f43e213919b00a474f766faa4bfe0b51fa4b8f25b4af1')
    version('6.0.0',   sha256='0ca2b8222156bb82b3bba060709f2b0159da99bef2bce346253719c740df20fa')
    version('5.0',     sha256='ceccae97eda0225a5b44d42ffd61102e248325c2865ca53e4407746464a5333a')

    depends_on('python@2.7:2.8,3:', type=('build', 'run'), when='@:7')
    depends_on('python@3:', type=('build', 'run'), when='@8:')
    depends_on('py-setuptools', type='build')

    for ver in ['5', '6', '7', '8', '9', '10', '11']:
        depends_on('llvm@' + ver, when='@' + ver, type='run')

