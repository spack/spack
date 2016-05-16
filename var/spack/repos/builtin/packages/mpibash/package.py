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
import os
from spack import *

class Mpibash(Package):
    """Parallel scripting right from the Bourne-Again Shell (Bash)"""
    homepage = "http://www.ccs3.lanl.gov/~pakin/software/mpibash-4.3.html"

    version('4.3', '81348932d5da294953e15d4814c74dd1',
            url="http://ftp.gnu.org/gnu/bash/bash-4.3.tar.gz")

    # patch -p1 < ../mpibash-4.3.patch
    patch('mpibash-4.3.patch', level=1, when='@4.3')

    # above patch modifies configure.ac
    depends_on('autoconf')

    # uses MPI_Exscan which is in MPI-1.2 and later
    depends_on('mpi@1.2:')

    depends_on('libcircle')

    def install(self, spec, prefix):
        # run autoconf to rebuild configure
        autoconf = which('autoconf')
        autoconf()

        configure("--prefix=" + prefix,
                  "CC=mpicc")

        make(parallel=False)

        make("install")
