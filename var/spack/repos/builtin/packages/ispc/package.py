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


class Ispc(Package):
    """Intel SPMD (Single Program, Multiple Data) Program Compiler.

    A compiler for the C-based SPMD programming language.  It is built on
    top of the llvm stack.

    Note: this library requires a 32-bit version of `glibc` (specifically,
    it needs to #include <gnu/stubs-32.h>).
    """
    homepage = "http://ispc.github.io/"
    url      = "https://github.com/ispc/ispc/"

    # To add new / old releases, since the spack docs discourage using tags:
    # 1. git clone https://github.com/ispc/ispc.git
    # 2. git checkout <tag> (e.g. v1.9.1)
    # 3. git log
    #    Copy the hash from the latest commit (top of git log),
    #    place this after .../tarball/<here>
    # 4. wget https://github.com/ispc/ispc/tarball/<hash from (3)>
    # 5. run `md5sum <hash from (3)>` since wget will save it as the hash
    version('1.9.1', 'e536686a5fc192b74de7ad0fefdfead9',
            url="https://github.com/ispc/ispc/tarball/87d0c9a2ed7c9d0eb40303a040abba709280f1ac")

    variant('nvptx', default=False,
            description='Also compile the NVIDIA NVPTX llvm component.')
    # :TODO:
    # The +arm variant doesn't appear to ever work, whenever you use the
    # executable it will produce:
    #
    # LLVM ERROR: Cannot select: intrinsic %llvm.x86.avx2.gather.d.pd.256
    #
    # If somebody comes through here and actually needs ARM, please fix this.
    # variant('arm', default=False,
    #         description='Also compile the ARM llvm component.')

    # libtinfo and libncurses have diverged, but ncurses is sufficient
    # and often people just symlink the two to fix build issues
    patch('ignore_libtinfo.patch', when='@1.9.1:')
    # LLVM versions changed names / functions, this fixes them.
    patch('update_llvm_functions_for_nvptx.patch', when="+nvptx")

    depends_on('ncurses', type=("build", "link"))
    depends_on('llvm',    type=("build", "link", "run"))# run necessary?
    depends_on('bison',   type="build")
    depends_on('flex',    type="build")

    def install(self, spec, prefix):
        make_flags = []
        if '+nvptx' in spec:
            make_flags.append("NVPTX_ENABLED=1")
        # :TODO: uncomment when the +arm variant is fixed
        # if '+arm' in spec:
        #     make_flags.append("ARM_ENABLED=1")
        make(*make_flags)
        # A single executable `ispc` is generated
        mkdirp(prefix.bin)
        install('ispc', prefix.bin)
