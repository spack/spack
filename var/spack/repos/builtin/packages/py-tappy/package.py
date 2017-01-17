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


class PyTappy(PythonPackage):
    """Python TAP interface module for unit tests"""
    homepage = "https://github.com/mblayman/tappy"
    # base https://pypi.python.org/pypi/cffi
    url      = "https://pypi.python.org/packages/source/t/tap.py/tap.py-1.6.tar.gz"

    version('1.6', 'c8bdb93ad66e05f939905172a301bedf')

    extends('python', ignore='bin/nosetests|bin/pygmentize')

    depends_on('python@2.6:2.7,3.2:3.4')
    depends_on('py-nose', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
