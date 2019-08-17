# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXlrd(PythonPackage):
    """Library for developers to extract data from Microsoft Excel (tm)
    spreadsheet files"""

    homepage = 'http://www.python-excel.org/'
    url      = "https://pypi.io/packages/source/x/xlrd/xlrd-0.9.4.tar.gz"

    version('0.9.4', '911839f534d29fe04525ef8cd88fe865')
