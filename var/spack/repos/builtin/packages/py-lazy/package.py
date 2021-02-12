# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLazy(PythonPackage):
    """Lazy attributes for Python objects"""

    pypi = "lazy/lazy-1.2.zip"

    version('1.4', sha256='2c6d27a5ab130fb85435320651a47403adcb37ecbcc501b0c6606391f65f5b43')
    version('1.3', sha256='c80a77bf7106ba7b27378759900cfefef38271088dc63b014bcfe610c8e68e3d')
    version('1.2', sha256='127ea610418057b953f0d102bed83f2c367be13b59f8d0ddf3b8a86c7d31b970')

    depends_on('py-setuptools', type='build')
