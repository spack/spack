# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXlrd(PythonPackage):
    """Library for developers to extract data from Microsoft Excel (tm)
    spreadsheet files"""

    homepage = 'http://www.python-excel.org/'
    url      = "https://pypi.io/packages/source/x/xlrd/xlrd-0.9.4.tar.gz"

    version('1.0.0', sha256='0ff87dd5d50425084f7219cb6f86bb3eb5aa29063f53d50bf270ed007e941069')
    version('0.9.4', sha256='8e8d3359f39541a6ff937f4030db54864836a06e42988c452db5b6b86d29ea72')

    depends_on('py-setuptools', when='@1.0.0:', type=('build', 'run'))
