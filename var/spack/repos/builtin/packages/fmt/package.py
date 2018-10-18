# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fmt(CMakePackage):
    """fmt (formerly cppformat) is an open-source formatting library.
    It can be used as a safe alternative to printf or as a fast alternative
    to C++ IOStreams."""

    homepage = "http://fmtlib.net/latest/index.html"
    url      = "https://github.com/fmtlib/fmt/releases/download/4.0.0/fmt-4.0.0.zip"

    version('4.1.0', 'ded3074a9405a07604d6355fdb592484')
    version('4.0.0', '605b5abee11b83195191234f4f414cf1')
    version('3.0.2', 'b190a7b8f2a5e522ee70cf339a53d3b2')
    version('3.0.1', '14505463b838befe1513b09cae112715')
    version('3.0.0', 'c099561e70fa194bb03b3fd5de2d3fd0')

    depends_on('cmake@2.8.12:', type='build')

    def cmake_args(self):
        return [
            '-DCMAKE_C_FLAGS={0}'.format(self.compiler.pic_flag),
            '-DCMAKE_CXX_FLAGS={0}'.format(self.compiler.pic_flag),
        ]
