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


class PyCdo(PythonPackage):
    """The cdo package provides an interface to the Climate Data
    Operators from Python."""

    homepage = "https://pypi.python.org/pypi/cdo"
    url      = "https://pypi.python.org/packages/sources/c/cdo/cdo-1.3.2.tar.gz"

    version('1.3.2', '4b3686ec1b9b891f166c1c466c6db745',
            url="https://pypi.python.org/packages/d6/13/908e7c1451e1f5fb68405f341cdcb3196a16952ebfe1f172cb788f864aa9/cdo-1.3.2.tar.gz")

    depends_on('cdo')

    depends_on('py-setuptools', type='build')
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-netcdf', type=('build', 'run'))
