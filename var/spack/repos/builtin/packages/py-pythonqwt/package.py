# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonqwt(PythonPackage):
    """Qt plotting widgets for Python"""

    homepage = "https://github.com/PierreRaybaut/PythonQwt"
    url      = "https://pypi.io/packages/source/P/PythonQwt/PythonQwt-0.5.5.zip"

    version('0.5.5', 'a60c7da9fbca667337d14aca094b6fda')

    variant('doc', default=False, description="Build documentation.")

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.3:',   type=('build', 'run'))
    depends_on('py-sip',          type=('build', 'run'))
    depends_on('py-pyqt4',      type=('build', 'run'))
    depends_on('py-sphinx@1.1:',  type=('build', 'run'), when='+docs')
