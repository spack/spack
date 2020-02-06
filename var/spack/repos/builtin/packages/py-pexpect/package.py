# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPexpect(PythonPackage):
    """Pexpect allows easy control of interactive console applications."""
    homepage = "https://pypi.python.org/pypi/pexpect"
    url      = "https://pypi.io/packages/source/p/pexpect/pexpect-4.2.1.tar.gz"

    version('4.6.0', sha256='2a8e88259839571d1251d278476f3eec5db26deb73a70be5ed5dc5435e418aba')
    version('4.2.1', sha256='3d132465a75b57aa818341c6521392a06cc660feb3988d7f1074f39bd23c9a92')
    version('3.3', sha256='dfea618d43e83cfff21504f18f98019ba520f330e4142e5185ef7c73527de5ba')

    depends_on('py-ptyprocess', type=('build', 'run'))
