##############################################################################
# Copyright (c) 2017, Kenneth Hoste
#
# This file is part of Spack.
# Created by Kenneth Hoste, kenneth.hoste@gmail.com
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


class PyEasybuildEasyblocks(PythonPackage):
    """Collection of easyblocks for EasyBuild, a software build and
    installation framework for (scientific) software on HPC systems.
    """

    homepage = 'http://hpcugent.github.io/easybuild/'
    url      = 'https://pypi.io/packages/source/e/easybuild-easyblocks/easybuild-easyblocks-3.1.2.tar.gz'

    version('3.1.2', 'be08da30c07e67ed3e136e8d38905fbc')

    depends_on('py-easybuild-framework@3.1:', when='@3.1:', type='run')
