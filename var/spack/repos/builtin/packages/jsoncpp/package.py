# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
