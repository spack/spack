##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class PyNatsort(PythonPackage):
    """Simple yet flexible natural sorting in Python."""

    homepage = "https://pypi.org/project/natsort/"
    url = "https://github.com/SethMMorton/natsort/archive/5.2.0.zip"

    version('5.2.0', '2ed2826550eef1f9ea3dd04f08b5da8b')
    version('5.1.1', '0525d4897fc98f40df5cc5a4a05f3c82')
    version('5.1.0', '518688548936d548775fb00afba999fb')
    version('5.0.3', '11147d75693995a946656927df7617d0')
    version('5.0.2', '1eb11a69086a5fb21d03f8189f1afed3')
    version('5.0.1', 'ca21c728bb3dd5dcfb010fa50b9c5e3c')
    version('5.0.0', 'fc7800fea50dcccbf8b116e1dff2ebf8')
    version('4.0.4', '7478ba31ec7fe554fcbfda41bb01f5ef')
    version('4.0.3', '2dc4fb1eb6ebfe4c9d95a12c2406df33')
    version('4.0.1', '659cf6ce95951003de0c85fc80b9f135')

    depends_on('py-setuptools', type=('build'))
