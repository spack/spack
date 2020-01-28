# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOpenpyxl(PythonPackage):
    """A Python library to read/write Excel 2010 xlsx/xlsm files"""

    homepage = "http://openpyxl.readthedocs.org/"
    url      = "https://pypi.io/packages/source/o/openpyxl/openpyxl-2.4.5.tar.gz"

    version('2.4.5', sha256='78c331e819fb0a63a1339d452ba0b575d1a31f09fdcce793a31bec7e9ef4ef21')

    depends_on('python@2.6:2.8,3.0:3.1,3.3:')

    depends_on('py-setuptools', type='build')

    depends_on('py-jdcal',      type=('build', 'run'))
    depends_on('py-et-xmlfile', type=('build', 'run'))
