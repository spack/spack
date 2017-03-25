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


class PyCython(PythonPackage):
    """The Cython compiler for writing C extensions for the Python language."""
    homepage = "https://pypi.python.org/pypi/cython"
    url      = "https://pypi.io/packages/source/c/cython/Cython-0.25.2.tar.gz"

    version('0.25.2', '642c81285e1bb833b14ab3f439964086')

    version('0.23.5', '66b62989a67c55af016c916da36e7514')
    version('0.23.4', '157df1f69bcec6b56fd97e0f2e057f6e')

    # These versions contain illegal Python3 code...
    version('0.22', '1ae25add4ef7b63ee9b4af697300d6b6')
    version('0.21.2', 'd21adb870c75680dc857cd05d41046a4')
