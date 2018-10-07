# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCurrent(PythonPackage):
    """Current module relative paths and imports"""

    homepage = "http://github.com/xflr6/current"
    url      = "https://pypi.io/packages/source/c/current/current-0.3.1.zip"

    version('0.3.1', '6378769c64d76831e72a6930b47ced27')

    depends_on('py-setuptools', type='build')
