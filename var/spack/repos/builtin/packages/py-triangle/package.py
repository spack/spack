# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTriangle(PythonPackage):
    """Python bindings to the triangle library"""

    homepage = 'https://github.com/drufat/triangle'
    url      = 'https://github.com/drufat/triangle/archive/refs/tags/v20200424.tar.gz'

    version('20200424', sha256='fe3e889aa27c0d9fb859881e70a1a1171b1a22e506b71899218052055416f616')

    depends_on('triangle',  type=('build', 'run'))
    depends_on('py-numpy',  type=('build', 'run'))
    depends_on('py-cython', type=('build'))
