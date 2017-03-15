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

class Rtags(Package):
    """client/server c/c++/objc[++] indexer based on clang"""
    homepage = "http://www.rtags.net/"
    url      = "https://github.com/Andersbakken/rtags/archive/v2.3.tar.gz"

    version('dev', git='https://github.com/Andersbakken/rtags.git')
    version('2.3', '33ac107d3767ac2dd5c1bd2143a0d0da')
    version('2.2', '34ec2aaeecd5910ce630fd3bbb0d5a29')
    version('2.1', 'a59ef304802f1a4406f4c84cf3823f98')

    depends_on("llvm +clang")
    depends_on("cmake")
    depends_on("zlib")

    def install(self, spec, prefix):
        git = which('git', required=True)
        git('submodule', 'update', '--init', '--recursive')
        cmake('.', '-DRTAGS_NO_ELISP_FILES=1', '-DRTAGS_NO_LUA_FILES=1', *std_cmake_args)

        make()
        make("install")
