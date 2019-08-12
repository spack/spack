# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLinecache2(PythonPackage):
    """Backports of the linecache module"""

    homepage = "https://github.com/testing-cabal/linecache2"
    url      = "https://pypi.io/packages/source/l/linecache2/linecache2-1.0.0.tar.gz"

    version('1.0.0', '7b25d0289ec36bff1f9e63c4329ce65c')

    depends_on('py-setuptools', type='build')
    depends_on('py-pbr', type=('build', 'run'))
