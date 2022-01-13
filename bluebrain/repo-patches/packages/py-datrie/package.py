# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDatrie(PythonPackage):
    """Super-fast, efficiently stored Trie for Python (2.x and 3.x).
    """

    homepage = "https://github.com/kmike/datrie"
    url      = "https://pypi.io/packages/source/d/datrie/datrie-3.11.2.tar.gz"

    version('0.8.2', '525b08f638d5cf6115df6ccd818e5a01298cd230b2dac91c8ff2e6499d18765d')
    version('0.8', 'bdd5da6ba6a97e7cd96eef2e7441c8d2ef890d04ba42694a41c7dffa3aca680c')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cython', type=('build'), when='@0.8.2:')
    depends_on('py-pytest-runner', type=('build'))
