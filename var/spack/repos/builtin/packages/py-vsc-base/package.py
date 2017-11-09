##############################################################################
# Copyright (c) 2017, Kenneth Hoste
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


class PyVscBase(PythonPackage):
    """Common Python libraries tools created by HPC-UGent"""

    homepage = 'https://github.com/hpcugent/vsc-base/'
    url      = 'https://pypi.io/packages/source/v/vsc-base/vsc-base-2.5.8.tar.gz'

    version('2.5.8', '57f3f49eab7aa15a96be76e6c89a72d8')

    depends_on('py-setuptools', type=('build', 'run'))
