# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPy2bit(PythonPackage):
    """A package for accessing 2bit files using lib2bit."""

    homepage = "https://pypi.python.org/pypi/py2bit"
    url      = "https://pypi.io/packages/source/p/py2bit/py2bit-0.2.1.tar.gz"

    version('0.2.1', 'eaf5b1c80a0bbf0b35af1f002f83a556')

    depends_on('py-setuptools', type='build')
