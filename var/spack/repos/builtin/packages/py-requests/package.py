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
    url = "https://github.com/kennethreitz/requests/archive/v2.13.0.tar.gz"


    version('2.13.0', '94ad79c2e57917aca999308b1fb4cbb4')
    version('2.11.1', 'ad5f9c47b5c5dfdb28363ad7546b0763')

    depends_on('py-setuptools',              type='build')
    depends_on('py-alabaster@0.7.7:',        type=('build', 'run'))
    depends_on('py-babel@2.2.0:',            type=('build', 'run'))
    depends_on('py-coverage@4.0.3:',         type=('build', 'run'))
    depends_on('py-decorator@4.0.9:',        type=('build', 'run'))
    depends_on('py-docutils@0.12:',          type=('build', 'run'))
    depends_on('py-flask@0.10.1:',           type=('build', 'run'))
    depends_on('py-httpbin@0.4.1:',          type=('build', 'run'))
    depends_on('py-itsdangerous@0.24:',      type=('build', 'run'))
    depends_on('py-jinja2@2.8:',             type=('build', 'run'))
    depends_on('py-markupsafe@0.23:',        type=('build', 'run'))
    depends_on('py-py@1.4.31:',              type=('build', 'run'))
    depends_on('py-pygments@2.1.1:',         type=('build', 'run'))
    depends_on('py-pysocks@1.5.6:',          type=('build', 'run'))
    depends_on('py-pytest@2.8.7:',           type=('build', 'run'))
    depends_on('py-pytest-cov@2.2.1:',       type=('build', 'run'))
    depends_on('py-pytest-httpbin@0.2.0:',   type=('build', 'run'))
    depends_on('py-pytest-mock@0.11.0:',     type=('build', 'run'))
    depends_on('py-pytz@2015.7:',            type=('build', 'run'))
    depends_on('py-six@1.10.0:',             type=('build', 'run'))
    depends_on('py-snowballstemmer@1.2.1:',  type=('build', 'run'))
    depends_on('py-sphinx@1.3.5:',           type=('build', 'run'))
    depends_on('py-sphinx-rtd-theme@0.1.9:', type=('build', 'run'))
    depends_on('py-werkzeug@0.11.4:',        type=('build', 'run'))
    depends_on('py-wheel@0.29.0:',           type=('build', 'run'))
