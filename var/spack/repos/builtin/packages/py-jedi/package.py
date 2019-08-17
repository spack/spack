# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJedi(PythonPackage):
    """An autocompletion tool for Python that can be used for text editors."""

    homepage = "https://github.com/davidhalter/jedi"
    url      = "https://pypi.io/packages/source/j/jedi/jedi-0.9.0.tar.gz"

    # unfortunately pypi.io only offers a .whl
    version('0.10.0', '89ed853d4a283bfa0fdbcf688b4d35fe',
                url='https://github.com/davidhalter/jedi/archive/v0.10.0.tar.gz')
    version('0.9.0', '2fee93d273622527ef8c97ac736e92bd')

    depends_on('py-setuptools', type='build')
