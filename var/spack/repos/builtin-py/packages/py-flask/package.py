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


class PyFlask(PythonPackage):
    """A microframework based on Werkzeug, Jinja2 and good intentions"""

    homepage = "http://github.com/pallets/flask"
    url      = "https://pypi.io/packages/source/F/Flask/Flask-0.11.1.tar.gz"

    version('0.12.2', '97278dfdafda98ba7902e890b0289177')
    version('0.12.1', '76e9fee5c3afcf4634b9baf96c578207')
    version('0.11.1', 'd2af95d8fe79cf7da099f062dd122a08')

    depends_on('py-setuptools',         type='build')
    depends_on('py-werkzeug@0.7:',      type=('build', 'run'))
    depends_on('py-jinja2@2.4:',        type=('build', 'run'))
    depends_on('py-itsdangerous@0.21:', type=('build', 'run'))
    depends_on('py-click@2.0:',         type=('build', 'run'))
