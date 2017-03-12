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


class PyJoblib(PythonPackage):
    """Python function as pipeline jobs"""

    homepage = "http://packages.python.org/joblib/"
    url      = "https://pypi.io/packages/source/j/joblib/joblib-0.10.3.tar.gz"

    version('0.10.3', '455401ccfaf399538d8e5333086df2d3')
    version('0.10.2', 'ebb42af4342c2445b175f86bd478d869')
    version('0.10.0', '61e40322c4fed5c22905f67d7d1aa557')

    depends_on('py-setuptools', type='build')
    # for testing
    # depends_on('py-nose', type=('build', 'run'))
