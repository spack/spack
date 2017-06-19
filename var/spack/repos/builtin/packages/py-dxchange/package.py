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


class PyDxchange(PythonPackage):
    """DXchange provides an interface with tomoPy and raw tomographic data
       collected at different synchrotron facilities."""

    homepage = "https://github.com/data-exchange/dxchange"
    url      = "https://github.com/data-exchange/dxchange/archive/v0.1.2.tar.gz"

    version('0.1.2', '36633bb67a1e7d1fb60c2300adbcbab3')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type='run')
    depends_on('py-scipy', type='run')
    depends_on('py-h5py', type='run')
    depends_on('py-six', type='run')
    depends_on('py-netcdf4', type='run')
    depends_on('py-spefile', type='run')
    depends_on('py-edffile', type='run')
    depends_on('py-tifffile', type='run')
    depends_on('py-dxfile', type='run')
