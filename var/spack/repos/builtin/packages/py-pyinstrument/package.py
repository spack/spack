# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyPyinstrument(PythonPackage):
    """Call stack profiler for Python. Shows you why your code is slow!"""

    homepage = "https://github.com/joerick/pyinstrument"
    pypi = "pyinstrument/pyinstrument-4.0.3.tar.gz"

    version('4.0.3', sha256='08caf41d21ae8f24afe79c664a34af1ed1e17aa5d4441cd9b1dc15f87bbbac95')
    version('3.1.3', sha256='353c7000a6563b16c0be0c6a04104d42b3154c5cd7c1979ab66efa5fdc5f5571')
    version('3.1.0', sha256='10c1fed4996a72c3e1e2bac1940334756894dbd116df3cc3b2d9743f2ae43016')

    depends_on('python@3.7:', when='@4:', type=('build', 'run'))
    depends_on('python@3.6:', when='@3.3:3.4', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-pytest-runner', when='@:3.1.3', type='build')
    depends_on('npm', when='@:3', type='build')
    depends_on('py-pyinstrument-cext@0.2.2:', when='@:3', type=('build', 'run'))
