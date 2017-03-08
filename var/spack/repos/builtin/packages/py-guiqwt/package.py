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


class PyGuiqwt(PythonPackage):
    """guiqwt is a set of tools for curve and image plotting
    (extension to PythonQwt)"""

    homepage = "https://github.com/PierreRaybaut/guiqwt"
    url      = "https://pypi.io/packages/source/g/guiqwt/guiqwt-3.0.2.zip"

    version('3.0.2', 'b49cd9706f56eb5d519390ba709d8c8c')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.3:',       type=('build', 'run'))
    depends_on('py-scipy@0.7:',       type=('build', 'run'))
    depends_on('py-guidata@1.7.0:',   type=('build', 'run'))
    depends_on('py-pythonqwt@0.5.0:', type=('build', 'run'))
    depends_on('py-pillow',           type=('build', 'run'))
