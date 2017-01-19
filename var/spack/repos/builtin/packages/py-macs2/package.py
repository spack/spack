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


class PyMacs2(PythonPackage):
    """MACS2 Model-based Analysis of ChIP-Seq"""

    homepage = "https://github.com/taoliu/MACS"
    url      = "https://pypi.python.org/packages/9f/99/a8ac96b357f6b0a6f559fe0f5a81bcae12b98579551620ce07c5183aee2c/MACS2-2.1.1.20160309.tar.gz"

    version('2.1.1.20160309', '2008ba838f83f34f8e0fddefe2a3a0159f4a740707c68058f815b31ddad53d26')

    depends_on('python@2.7:2.8')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-macs2 requires py-setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy@1.6:', type=('build', 'run'))
