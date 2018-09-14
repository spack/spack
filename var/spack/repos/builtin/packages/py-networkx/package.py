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


class PyNetworkx(PythonPackage):
    """NetworkX is a Python package for the creation, manipulation, and study
    of the structure, dynamics, and functions of complex networks."""
    homepage = "http://networkx.github.io/"
    url      = "https://pypi.io/packages/source/n/networkx/networkx-1.11.tar.gz"

    version('2.1', sha256='64272ca418972b70a196cb15d9c85a5a6041f09a2f32e0d30c0255f25d458bb1',
            url='https://pypi.io/packages/source/n/networkx/networkx-2.1.zip')
    version('1.11', md5='6ef584a879e9163013e9a762e1cf7cd1')
    version('1.10', md5='eb7a065e37250a4cc009919dacfe7a9d')

    depends_on('py-decorator', type=('build', 'run'))
    depends_on('py-decorator@4.1.0:', type=('build', 'run'), when='@2.1:')
    depends_on('py-setuptools', type='build')
