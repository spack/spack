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


class PyPy4j(PythonPackage):
    """Enables Python programs to dynamically access arbitrary Java
    objects."""

    homepage = "https://www.py4j.org/"
    url = "https://pypi.io/packages/source/p/py4j/py4j-0.10.4.zip"

    version('0.10.6', sha256='d3e7ac7c2171c290eba87e70aa5095b7eb6d6ad34789c007c88d550d9f575083')
    version('0.10.4', sha256='406fbfdbcbbb398739f61fafd25724670a405a668eb08c1721d832eadce06aae')
    version('0.10.3', sha256='f4570108ad014dd52a65c2288418e31cb8227b5ecc39ad7fc7fe98314f7a26f2')

    depends_on('py-setuptools', type='build')
