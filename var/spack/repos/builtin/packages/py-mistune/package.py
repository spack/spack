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


class PyMistune(PythonPackage):
    """
    Python markdown parser
    """
    homepage = "http://mistune.readthedocs.org/en/latest/"
    url      = "https://github.com/lepture/mistune/archive/v0.7.1.tar.gz"

    version('0.7.1', '0d9c29700c670790c5b2471070d32ec2')
    version('0.7', '77750ae8b8d0d584894224a7e0c0523a')
    version('0.6', 'd4f3d4f28a69e715f82b591d5dacf9a6')
    version('0.5.1', '1c6cfce28a4aa90cf125217cd6c6fe6c')
    version('0.5', '997736554f1f95eea78c66ae339b5722')

    depends_on('py-setuptools', type='build')
