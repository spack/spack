##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class PyPytest(PythonPackage):
    """pytest: simple powerful testing with Python."""

    homepage = "http://pytest.org/"
    url      = "https://pypi.io/packages/source/p/pytest/pytest-3.0.7.tar.gz"

    import_modules = [
        '_pytest', '_pytest.assertion', '_pytest._code',
        '_pytest.vendored_packages', 'pytest'
    ]

    version('3.0.7', '89c60546507dc7eb6e9e40a6e9f720bd')
    version('3.0.2', '61dc36e65a6f6c11c53b1388e043a9f5')

    # Most Python packages only require setuptools as a build dependency.
    # However, pytest requires setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-py@1.4.29:', type=('build', 'run'))
    depends_on('py-hypothesis@3.5.2:', type=('build', 'run'))

    # TODO: Add a 'test' deptype
    # depends_on('py-nose', type='test')
    # depends_on('py-mock', type='test')
    # depends_on('py-requests', type='test')
