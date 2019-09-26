# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCsvkit(PythonPackage):
    """A library of utilities for working with CSV, the king of tabular file
    formats"""

    homepage = 'http://csvkit.rtfd.org/'
    url      = "https://pypi.io/packages/source/c/csvkit/csvkit-0.9.1.tar.gz"

    version('0.9.1', '48d78920019d18846933ee969502fff6')

    depends_on('py-setuptools', type='build')
    depends_on('py-python-dateutil@2.2', type=('build', 'run'), when='@0.9.1')
    depends_on('py-python-dateutil', type=('build', 'run'), when='@0.9.2:')
    depends_on('py-dbf@0.94.003', type=('build', 'run'))
    depends_on('py-xlrd', type=('build', 'run'))
    depends_on('py-sqlalchemy', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-openpyxl@2.2.0-b1', type=('build', 'run'))
