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
