# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOpenpyxl(PythonPackage):
    """A Python library to read/write Excel 2010 xlsx/xlsm files"""

    homepage = "http://openpyxl.readthedocs.org/"
    url      = "https://pypi.io/packages/source/o/openpyxl/openpyxl-2.4.5.tar.gz"

    version('2.4.5', '3de13dc9b731e1a9dd61b873d9b35a8a')
    version('2.2.0-b1', 'eeefabe384f6e53166c8c2e6abe5d11b')

    depends_on('python@2.6:2.8,3.0:3.1,3.3:')

    depends_on('py-setuptools', type='build')

    depends_on('py-jdcal',      type=('build', 'run'))
    depends_on('py-et-xmlfile', type=('build', 'run'))
