# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyinstrument(PythonPackage):
    """Call stack profiler for Python. Shows you why your code is slow!"""

    homepage = "https://github.com/joerick/pyinstrument"
    url      = "https://github.com/joerick/pyinstrument/archive/v3.1.0.tar.gz"

    version('3.1.0', sha256='02319607daf65110e246085f5e2ee111f565f213eed1991229f2d58e9a7657a5')

    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
    depends_on('npm', type='build')
    depends_on('py-pyinstrument-cext@0.2.2:', type=('build', 'run'))
    depends_on('py-pytest', type='test')
