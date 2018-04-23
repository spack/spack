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


class Rtags(CMakePackage):
    """RTags is a client/server application that indexes C/C++ code"""

    homepage = "https://github.com/Andersbakken/rtags/"
    url      = "https://andersbakken.github.io/rtags-releases/rtags-2.17.tar.gz"

    version('2.17', '95b24d7729678645a027d83be114d624')
    # version('2.12', '84988aaff27915a79d4b4b57299f9a51')  # no available

    depends_on("llvm@3.3: +clang")
    depends_on("zlib")
    depends_on("openssl")
    depends_on("lua@5.3:")
    depends_on("bash-completion")
    depends_on("pkgconfig", type='build')

    patch("add_string_iterator_erase_compile_check.patch", when='@2.12')

    def cmake_args(self):
        args = ['-DCMAKE_EXPORT_COMPILE_COMMANDS=1',
                '-DRTAGS_NO_ELISP_FILES=1',
                ]
        return args
