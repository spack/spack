# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFenicsFfcx(PythonPackage):
    """Next generation FEniCS Form Compiler"""

    homepage = "https://github.com/FEniCS/ffcx"
    url = "https://github.com/FEniCS/ffcx/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/ffcx.git"
    maintainers = ["js947", "chrisrichardson", "garth-wells"]

    version('main', branch='main')
    version('0.1.0', sha256='98a47906146ac892fb4a358e04cbfd04066f12d0a4cdb505a6b08ff0b1a17e89')
    version('0.2.0', sha256='0457168cdba0e86ffbfc5b1d44f7b1e1b91fd8a73f54f1eff5998d4b61e6bd10')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cffi', type='run')

    depends_on('py-fenics-ufl@main', type='run', when='@main')
    depends_on('py-fenics-ufl@2021.1.0', type='run', when='@0.1:')

    depends_on('py-fenics-basix@main', type='run', when='@main')
    depends_on('py-fenics-basix@0.1.0', type='run', when='@0.1.0')
    depends_on('py-fenics-basix@0.2.0', type='run', when='@0.2.0')

    depends_on('py-numpy', type='run')
