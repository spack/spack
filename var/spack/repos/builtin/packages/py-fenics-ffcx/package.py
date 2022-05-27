# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFenicsFfcx(PythonPackage):
    """Next generation FEniCS Form Compiler"""

    homepage = "https://github.com/FEniCS/ffcx"
    url = "https://github.com/FEniCS/ffcx/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/ffcx.git"
    maintainers = ["chrisrichardson", "garth-wells"]

    version('main', branch='main')
    version('0.4.2', sha256='3be6eef064d6ef907245db5b6cc15d4e603762e68b76e53e099935ca91ef1ee4')
    version('0.3.0', sha256='33fa1a0cc5762f360033c25a99ec9462be933f8ba413279e35cd2c3b5c3e6096')
    version('0.2.0', sha256='562a704163a6427e0341d267e69b8bf55d8f53d673829170b443191577e8d9b6')
    version('0.1.0', sha256='98a47906146ac892fb4a358e04cbfd04066f12d0a4cdb505a6b08ff0b1a17e89')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools@58:', type='build', when="@0.4:")
    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build', when="@0.4:")

    depends_on('py-cffi', type='run')

    depends_on('py-fenics-ufl@main', type='run', when='@main')
    depends_on('py-fenics-ufl@2022.1.0', type='run', when='@0.4.2')
    depends_on('py-fenics-ufl@2021.1.0', type='run', when='@0.1.0:0.3')

    depends_on('py-fenics-basix@main', type='run', when='@main')
    depends_on('py-fenics-basix@0.4.2', type='run', when='@0.4.2')
    depends_on('py-fenics-basix@0.3.0', type='run', when='@0.3.0')
    depends_on('py-fenics-basix@0.2.0', type='run', when='@0.2.0')
    depends_on('py-fenics-basix@0.1.0', type='run', when='@0.1.0')

    depends_on('py-numpy', type='run')
