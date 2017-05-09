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


class PyFlask(PythonPackage):
    """A microframework based on Werkzeug, Jinja2 and good intentions"""

    homepage = "http://github.com/pallets/flask"
    url      = "https://github.com/pallets/flask/archive/0.12.1.tar.gz"

    version('0.12.1', '96b4e75958d5903a288cde5cd817c952')
    version('0.12',   '05955d5210e075d6f80bc176ddaa07fe')
    version('0.11.1', '91d9ae06a86eecea15ae851796d52d08')
    version('0.11',   '887f24aefd3ee678d82f5b875b76180a')
    version('0.10.1', '5c32eee153a2dcd30405225a5af1fea4')
    version('0.10',   '4c01039cf3b47efb223d63cdbac96c3a')
    version('0.9',    '6faa8c222a4e1293fa0628c39bdf80a9')
    version('0.8.1',  'f4bc18732060d2648fe79e0e9d9bbff8')
    version('0.8',    'c250ff97104283fee2da07166bc37364')
    version('0.7.2',  '12371cb27546e0d25332cea109ccf237')

    depends_on('py-setuptools',         type='build')
    depends_on('py-werkzeug@0.7:',      type=('build', 'run'))
    depends_on('py-jinja2@2.4:',        type=('build', 'run'))
    depends_on('py-itsdangerous@0.21:', type=('build', 'run'))
    depends_on('py-click@2.0:',         type=('build', 'run'))
