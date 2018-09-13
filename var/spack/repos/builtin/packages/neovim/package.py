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


class Neovim(CMakePackage):
    """NeoVim: the future of vim"""

    homepage = "http://neovim.io"
    url      = "https://github.com/neovim/neovim/archive/v0.2.0.tar.gz"

    version('0.3.1', '5405bced1c929ebc245c75409cd6c7ef')
    version('0.3.0', 'e5fdb2025757c337c17449c296eddf5b')
    version('0.2.2', '44b69f8ace88b646ec890670f1e462c4')
    version('0.2.1', 'f4271f22d2a46fa18dace42849c56a98')
    version('0.2.0', '9af7f61f9f0b1a2891147a479d185aa2')

    depends_on('lua@5.1:5.2')
    depends_on('lua-lpeg')
    depends_on('lua-mpack')
    depends_on('lua-bitlib')
    depends_on('libuv')
    depends_on('jemalloc')
    depends_on('libtermkey')
    depends_on('libvterm')
    depends_on('unibilium')
    depends_on('msgpack-c')
    depends_on('gperf')

    def cmake_args(self):
        args = []
        if self.version >= Version('0.2.1'):
            args = ['-DPREFER_LUA=ON']

        return args
