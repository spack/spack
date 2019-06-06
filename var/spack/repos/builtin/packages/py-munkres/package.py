# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMunkres(PythonPackage):
    """Python library for Munkres algorithm"""

    homepage = "https://github.com/bmc/munkres"
    url = "https://pypi.io/packages/source/m/munkres/munkres-1.1.2.tar.gz"

    version('1.1.2', sha256='81e9ced40c3d0ffc48be4b6da5cfdfaa49041faaaba8075b159974ec47926aea', preferred=True)

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
