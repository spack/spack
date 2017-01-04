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


class PyPytz(PythonPackage):
    """World timezone definitions, modern and historical."""

    homepage = "https://pypi.python.org/pypi/pytz"
    url      = "https://pypi.python.org/packages/source/p/pytz/pytz-2014.10.tar.gz"

    version('2016.6.1', 'b6c28a3b968bc1d8badfb61b93874e03',
            url="https://pypi.python.org/packages/5d/8e/6635d8f3f9f48c03bb925fab543383089858271f9cfd1216b83247e8df94/pytz-2016.6.1.tar.gz")
    version('2014.10', 'eb1cb941a20c5b751352c52486aa1dd7')
    version('2015.4', '417a47b1c432d90333e42084a605d3d8')
    version('2016.3', 'abae92c3301b27bd8a9f56b14f52cb29')

    depends_on('py-setuptools', type='build')
