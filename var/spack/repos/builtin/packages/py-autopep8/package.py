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


class PyAutopep8(PythonPackage):
    """autopep8 automatically formats Python code to conform to the
    PEP 8 style guide."""

    homepage = "https://github.com/hhatto/autopep8"
    url      = "https://pypi.io/packages/source/a/autopep8/autopep8-1.2.4.tar.gz"

    version('1.3.3', '8951f43748406015b663a54ab05d891a')
    version('1.2.4', 'fcea19c0c5e505b425e2a78afb771f5c')
    version('1.2.2', '3d97f9c89d14a0975bffd32a2c61c36c')

    extends('python', ignore='bin/pep8')
    depends_on('python@2.6:2.8,3.2:')

    depends_on('py-pycodestyle@1.5.7:1.7.0', type=('build', 'run'), when='@:1.2.4')
    depends_on('py-pycodestyle@2.3.0:', type=('build', 'run'), when='@1.3:')

    depends_on('py-setuptools', type='build')
