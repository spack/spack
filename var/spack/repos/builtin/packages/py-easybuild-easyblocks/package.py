##############################################################################
# Copyright (c) 2017, Kenneth Hoste
#
# This file is part of Spack.
# Created by Kenneth Hoste, kenneth.hoste@gmail.com
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


class PyEasybuildEasyblocks(PythonPackage):
    """
    Collection of easyblocks for EasyBuild, a software build and
    installation framework for (scientific) software on HPC systems.
    """

    homepage = 'http://hpcugent.github.io/easybuild/'
    url      = 'https://pypi.python.org/packages/d6/55/9b6634b01fbc26edb9f5af39b06acbe7ec843da438ba5ac3063937934b3e/easybuild-easyblocks-3.1.2.tar.gz'

    version('3.1.2', 'be08da30c07e67ed3e136e8d38905fbc')

    depends_on('py-easybuild-framework', type='run')
