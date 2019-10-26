# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPerf(PythonPackage):
    """The Python perf module is a toolkit to write, run and
    analyze benchmarks.
    """

    homepage = "https://pypi.python.org/pypi/pyperf"
    url = "https://github.com/vstinner/pyperf/archive/1.5.1.tar.gz"

    version('1.5.1', sha256='9c271862bc2911be8eb01031a4a86cbc3f5bb615971514383802d3dcf46f18ed')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
