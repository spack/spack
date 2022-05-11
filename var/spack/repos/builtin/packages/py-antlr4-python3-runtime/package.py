# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAntlr4Python3Runtime(PythonPackage):
    """This package provides runtime libraries required to use
    parsers generated for the Python3 language by version 4 of
    ANTLR (ANother Tool for Language Recognition).
    """

    homepage = "https://www.antlr.org"
    pypi = "antlr4-python3-runtime/antlr4-python3-runtime-4.7.2.tar.gz"

    version('4.8', sha256='15793f5d0512a372b4e7d2284058ad32ce7dd27126b105fb0b2245130445db33')
    version('4.7.2', sha256='168cdcec8fb9152e84a87ca6fd261b3d54c8f6358f42ab3b813b14a7193bb50b')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-typing', when='^python@:3.4', type=('build', 'run'))
