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


class MsgpackC(CMakePackage):
    """A small, fast binary interchange format convertible to/from JSON"""
    homepage = "http://www.msgpack.org"
    url      = "https://github.com/msgpack/msgpack-c/archive/cpp-3.0.1.tar.gz"

    version('3.0.1', 'a79f05f0dc5637c161805d6c0e9bfbe7')
    version('1.4.1', 'e2fd3a7419b9bc49e5017fdbefab87e0')

    depends_on('cmake@2.8.12:', type='build')

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_FLAGS=-Wno-implicit-fallthrough",
            "-DCMAKE_C_FLAGS=-Wno-implicit-fallthrough"
        ]
        return args
