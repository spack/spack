##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PyPy(PythonPackage):
    """Library with cross-python path, ini-parsing, io, code, log facilities"""

    homepage = "http://pylib.readthedocs.io/en/latest/"
    url      = "https://pypi.io/packages/source/p/py/py-1.5.4.tar.gz"

    import_modules = [
        'py', 'py._process', 'py._vendored_packages', 'py._path',
        'py._log', 'py._code', 'py._io'
    ]

    version('1.5.4',  '7502d66fa68ea4ae5b61c511cd177d6a')
    version('1.5.3',  '667d37a148ad9fb81266492903f2d880')
    version('1.4.33', '15d7107cbb8b86593bf9afa16e56da65')
    version('1.4.31', '5d2c63c56dc3f2115ec35c066ecd582b')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    def test(self):
        # Tests require pytest, creating a circular dependency
        pass
