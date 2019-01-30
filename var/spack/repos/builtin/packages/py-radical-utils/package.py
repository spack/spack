# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRadicalUtils(PythonPackage):
    """Shared code and tools for various RADICAL Projects"""

    homepage = "http://radical.rutgers.edu"
    url      = "https://pypi.io/packages/source/r/radical.utils/radical.utils-0.45.tar.gz"

    version('0.45', 'c0bec2a0951b0dc990366d82e78e65fe')
    version('0.41.1', '923446539545dc157768026c957cecb2')

    depends_on('py-setuptools', type='build')
    depends_on('py-colorama',   type=('build', 'run'))
    depends_on('py-netifaces',  type=('build', 'run'))
