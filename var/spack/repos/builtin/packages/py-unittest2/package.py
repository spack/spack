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


class PyUnittest2(PythonPackage):
    """unittest2 is a backport of the new features added to the unittest
    testing framework in Python 2.7 and onwards."""

    homepage = "https://pypi.python.org/pypi/unittest2"
    url      = "https://pypi.python.org/packages/source/u/unittest2/unittest2-1.1.0.tar.gz"

    version('1.1.0', 'f72dae5d44f091df36b6b513305ea000')

    depends_on('py-setuptools', type='build')
    depends_on('py-enum34', when='^python@:3.3', type=('build', 'run'))
