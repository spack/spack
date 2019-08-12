# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWcwidth(PythonPackage):
    """Measures number of Terminal column cells of wide-character codes"""

    homepage = "https://pypi.python.org/pypi/wcwidth"
    url      = "https://pypi.io/packages/source/w/wcwidth/wcwidth-0.1.7.tar.gz"

    version('0.1.7', 'b3b6a0a08f0c8a34d1de8cf44150a4ad')

    depends_on('py-setuptools', type='build')
