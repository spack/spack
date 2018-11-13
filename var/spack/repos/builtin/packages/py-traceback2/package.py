# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTraceback2(PythonPackage):
    """Backports of the traceback module"""

    homepage = "https://github.com/testing-cabal/traceback2"
    url      = "https://pypi.io/packages/source/t/traceback2/traceback2-1.4.0.tar.gz"

    version('1.4.0', '9e9723f4d70bfc6308fa992dd193c400')

    depends_on('py-setuptools', type='build')
    depends_on('py-linecache2', type=('build', 'run'))
    depends_on('py-pbr', type=('build', 'run'))
