# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyRadicalGtod(PythonPackage):
    """RADICAL-GTOD provides a single method, gtod, which returns the current
    time in seconds since epoch (01.01.1970) with sub-second resolution and a
    binary tool, radical-gtod, which is a compiled binary and does not require
    the invocation of the Python interpreter."""

    homepage = 'https://radical-cybertools.github.io'
    git      = 'https://github.com/radical-cybertools/radical.gtod.git'
    pypi     = 'radical.gtod/radical.gtod-1.6.7.tar.gz'

    maintainers = ['andre-merzky']

    version('develop', branch='devel')
    version('1.6.7',   sha256='8d7d32e3d0bcf6d7cf176454a9892a46919b03e1ed96bee389380e6d75d6eff8')

    depends_on('python@3.6:',   type=('build', 'run'))
    depends_on('py-setuptools', type='build')
