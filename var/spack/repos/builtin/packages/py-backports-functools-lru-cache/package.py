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


class PyBackportsFunctoolsLruCache(PythonPackage):
    """Backport of functools.lru_cache from Python 3.3"""

    homepage = "https://github.com/jaraco/backports.functools_lru_cache"
    url = "https://pypi.io/packages/source/b/backports.functools_lru_cache/backports.functools_lru_cache-1.4.tar.gz"

    version('1.5', '20f53f54cd3f04b3346ce75a54959754')
    version('1.4', 'b954e7d5e2ca0f0f66ad2ed12ba800e5')
    version('1.0.1', 'c789ef439d189330b99872746a6d9e85',
            url="https://pypi.io/packages/source/b/backports.functools_lru_cache/backports.functools_lru_cache-1.0.1.zip")

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@1.15.0:', type='build')
    depends_on('python@2.6.0:3.3.99',        type=('build', 'run'))
