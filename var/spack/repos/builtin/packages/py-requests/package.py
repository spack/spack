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


class PyRequests(PythonPackage):
    """Python HTTP for Humans."""

    homepage = "http://python-requests.org"
    url = "https://pypi.io/packages/source/r/requests/requests-2.13.0.tar.gz"

    version('2.13.0', '921ec6b48f2ddafc8bb6160957baf444')
    version('2.11.1', 'ad5f9c47b5c5dfdb28363ad7546b0763')

    depends_on('py-setuptools',              type='build')
    # from setup.py:
    # test_requirements = ['pytest>=2.8.0', 'pytest-httpbin'==0.0.7,
    #                      'pytest-cov', 'pytest-mock']
    # needs #1279 and #2869
    # depends_on('py-pytest@2.8.7:',           type=('build', 'run'))
    # depends_on('py-pytest-cov@2.2.1:',       type=('build', 'run'))
    # depends_on('py-pytest-httpbin@0.2.0:',   type=('build', 'run'))
    # depends_on('py-pytest-mock@0.11.0:',     type=('build', 'run'))
