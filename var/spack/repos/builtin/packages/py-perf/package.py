# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPerf(PythonPackage):
    """The Python perf module is a toolkit to write, run and
    analyze benchmarks.
    """

    homepage = "https://pypi.python.org/pypi/perf"
    url = "https://github.com/vstinner/perf/archive/1.5.1.tar.gz"

    version('1.5.1', 'e3dc532fdbaf44f2d921556164bd74e5')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
