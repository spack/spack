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


class PyStatsmodels(PythonPackage):
    """Statistical computations and models for use with SciPy"""

    homepage = "http://www.statsmodels.org"
    url      = "https://pypi.io/packages/source/s/statsmodels/statsmodels-0.8.0.tar.gz"

    version('0.8.0', 'b3e5911cc9b00b71228d5d39a880bba0')

    variant('tests',    default=False, description='With nose tests')
    variant('plotting', default=False, description='With matplotlib')

    # according to http://www.statsmodels.org/dev/install.html earlier versions
    # might work.
    depends_on('py-setuptools@0.6c5:', type='build')
    depends_on('py-numpy@1.7.0:',      type=('build', 'run'))
    depends_on('py-scipy@0.11:',       type=('build', 'run'))
    depends_on('py-pandas@0.12:',      type=('build', 'run'))
    depends_on('py-patsy@0.2.1:',      type=('build', 'run'))
    depends_on('py-cython@0.24:',      type=('build', 'run'))
    depends_on('py-nose',              type='run', when='+tests')
    depends_on('py-matplotlib@1.3:',   type='run', when='+plotting')
