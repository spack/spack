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


class Jsoncpp(CMakePackage):
    """JsonCpp is a C++ library that allows manipulating JSON values,
    including serialization and deserialization to and from strings.
    It can also preserve existing comment in unserialization/serialization
    steps, making it a convenient format to store user input files."""

    homepage = "https://github.com/open-source-parsers/jsoncpp"
    url      = "https://github.com/open-source-parsers/jsoncpp/archive/1.7.3.tar.gz"

    version('1.7.3', 'aff6bfb5b81d9a28785429faa45839c5')

    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'MinSizeRel', 'Coverage'))

    depends_on('cmake@3.1:', type='build')
    depends_on('python', type='test')

    def cmake_args(self):
        return ['-DBUILD_SHARED_LIBS=ON']
