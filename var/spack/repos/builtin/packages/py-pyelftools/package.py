# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyelftools(PythonPackage):
    """Library for analyzing ELF files and DWARF debugging information"""

    homepage = "https://github.com/eliben/pyelftools"
    pypi = "pyelftools/pyelftools-0.27.tar.gz"

    version('0.27', sha256='cde854e662774c5457d688ca41615f6594187ba7067af101232df889a6b7a66b')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
