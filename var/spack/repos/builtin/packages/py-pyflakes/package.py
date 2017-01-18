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


class PyPyflakes(PythonPackage):
    """A simple program which checks Python source files for errors."""

    homepage = "https://github.com/PyCQA/pyflakes"
    url      = "https://github.com/PyCQA/pyflakes/archive/1.3.0.tar.gz"

    version('1.3.0', 'a76173deb7a84fe860c0b60e2fbcdfe2')
    version('1.2.3', '2ac2e148a5c46b6bb06c4785be76f7cc')
    version('1.2.2', 'fe759b9381a6500e67a2ddbbeb5161a4')
    version('1.2.1', '444a06b256e0a70e41c11698b7190e84')
    version('1.2.0', '5d1c87bf09696c4c35dc3103f2a1185c')
    version('1.1.0', '4e18bf78c0455ebcd41e5d6104392c88')
    version('1.0.0', 'e2ea22a825c5100f12e54b71771cde71')
    version('0.9.2', 'd02d5f68e944085fd6ec163a34737a96')
    version('0.9.1', '8108d2248e93ca6a315fa2dd31ee9bb1')
    version('0.9.0', '43c2bcee88606bde55dbf25a253ef886')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-pyflakes requires py-setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
