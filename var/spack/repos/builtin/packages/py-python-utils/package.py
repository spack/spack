# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonUtils(PythonPackage):
    """A module with some convenient utilities not included with the standard Python install"""

    homepage = "https://github.com/WoLpH/python-utils"
    url = "https://pypi.io/packages/source/p/python-utils/python-utils-2.3.0.tar.gz"

    version('2.3.0', sha256='34aaf26b39b0b86628008f2ae0ac001b30e7986a8d303b61e1357dfcdad4f6d3', preferred=True)

    depends_on('py-setuptools', type='build')

    depends_on('py-six', type='run')
