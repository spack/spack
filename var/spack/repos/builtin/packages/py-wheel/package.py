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


class PyWheel(PythonPackage):
    """A built-package format for Python."""

    homepage = "https://pypi.python.org/pypi/wheel"

    version('0.30.0', 'aa1145d48e4da2f9415eac2d51468a83',
        url='https://pypi.python.org/packages/a7/37/947b4329c4a3c72093b6c8e9b4be8c7f10c32dbb78848d3a234ce01c059d/wheel-0.30.0a0.tar.gz')
    version('0.26.0', '4cfc6e7e3dc7377d0164914623922a10',
        url='https://pypi.python.org/packages/source/w/wheel/wheel-0.26.0.tar.gz')

    depends_on('py-setuptools', type='build')
