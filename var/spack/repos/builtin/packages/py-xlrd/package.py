# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXlrd(PythonPackage):
    """Library for developers to extract data from Microsoft Excel (tm)
    spreadsheet files"""

    homepage = 'http://www.python-excel.org/'
    pypi = "xlrd/xlrd-0.9.4.tar.gz"

    version('2.0.1', sha256='f72f148f54442c6b056bf931dbc34f986fd0c3b0b6b5a58d013c9aef274d0c88')
    version('2.0.0', sha256='e1ae0dbdb0a4888e381255f9aefe3efcd7ea64a35666e7a03c3f3c9e4b44641b')
    version('1.2.0', sha256='546eb36cee8db40c3eaa46c351e67ffee6eeb5fa2650b71bc4c758a29a1b29b2')
    version('1.1.0', sha256='8a21885513e6d915fe33a8ee5fdfa675433b61405ba13e2a69e62ee36828d7e2')
    version('1.0.0', sha256='0ff87dd5d50425084f7219cb6f86bb3eb5aa29063f53d50bf270ed007e941069')
    version('0.9.4', sha256='8e8d3359f39541a6ff937f4030db54864836a06e42988c452db5b6b86d29ea72')
