##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

    homepage = "http://doc.pytest.org/en/latest/"
    url      = "https://pypi.python.org/packages/source/p/pytest/pytest-3.0.2.tar.gz"

    version('3.0.2', '61dc36e65a6f6c11c53b1388e043a9f5',
            url="https://pypi.python.org/packages/2b/05/e20806c99afaff43331f5fd8770bb346145303882f98ef3275fa1dd66f6d/pytest-3.0.2.tar.gz")

    depends_on('py-setuptools', type='build')
    depends_on('py-py@1.4.29:', type=('build', 'run'))
