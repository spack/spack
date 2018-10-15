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


class NlohmannJson(CMakePackage):
    """JSON for Modern C++"""

    homepage = "https://nlohmann.github.io/json/"
    url      = "https://github.com/nlohmann/json/archive/v3.1.2.tar.gz"
    maintainers = ['ax3l']

    version('3.3.0', sha256='2fd1d207b4669a7843296c41d3b6ac5b23d00dec48dba507ba051d14564aa801')
    version('3.1.2', '557651b017c36ad596ba3b577ba1b539')

    variant('single_header', default=True,
        description='Use amalgamated single-header')
    variant('test', default=True,
        description='Build the tests')

    depends_on('cmake@3.8:', type='build')

    # requires mature C++11 implementations
    conflicts('%gcc@:4.7')
    # v3.3.0 adds support for gcc 4.8
    # https://github.com/nlohmann/json/releases/tag/v3.3.0
    conflicts('%gcc@:4.8', when='@:3.2.9')
    conflicts('%intel@:16')
    conflicts('%pgi@:14')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DJSON_MultipleHeaders:BOOL={0}'.format(
                'ON' if '~single_header' in spec else 'OFF'),
            '-DBUILD_TESTING:BOOL={0}'.format(
                'ON' if '+test' in spec else 'OFF')
        ]

        return args
