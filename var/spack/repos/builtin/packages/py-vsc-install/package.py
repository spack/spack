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


class PyVscInstall(PythonPackage):
    """Shared setuptools functions and classes
    for Python libraries developed by HPC-UGent.
    """

    homepage = 'https://github.com/hpcugent/vsc-install/'
    url      = 'https://pypi.io/packages/source/v/vsc-install/vsc-install-0.10.25.tar.gz'

    version('0.10.25', 'd1b9453a75cb56dba0deb7a878047b51')

    depends_on('py-setuptools', type=('build', 'run'))
