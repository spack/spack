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


class PyRadicalUtils(PythonPackage):
    """Shared code and tools for various RADICAL Projects"""

    homepage = "http://radical.rutgers.edu"
    url      = "https://pypi.io/packages/source/r/radical.utils/radical.utils-0.45.tar.gz"

    version('0.45', 'c0bec2a0951b0dc990366d82e78e65fe')
    version('0.41.1', '923446539545dc157768026c957cecb2')

    depends_on('py-setuptools', type='build')
    depends_on('py-colorama',   type=('build', 'run'))
    depends_on('py-netifaces',  type=('build', 'run'))
