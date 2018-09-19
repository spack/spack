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


class Stream(MakefilePackage):
    """The STREAM benchmark is a simple synthetic benchmark program that
    measures sustainable memory bandwidth (in MB/s) and the corresponding
    computation rate for simple vector kernels."""

    homepage = "https://www.cs.virginia.edu/stream/ref.html"
    git      = "https://github.com/jeffhammond/STREAM.git"

    version('5.10')

    variant('openmp', default=False, description='Build with OpenMP support')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')

        # Use the Spack compiler wrappers
        makefile.filter('CC = .*', 'CC = cc')
        makefile.filter('FC = .*', 'FC = f77')

        cflags = '-O2'
        fflags = '-O2'
        if '+openmp' in self.spec:
            cflags += ' ' + self.compiler.openmp_flag
            fflags += ' ' + self.compiler.openmp_flag

        # Set the appropriate flags for this compiler
        makefile.filter('CFLAGS = .*', 'CFLAGS = {0}'.format(cflags))
        makefile.filter('FFLAGS = .*', 'FFLAGS = {0}'.format(fflags))

    def install(self, spec, prefix):
        # Manual installation
        mkdir(prefix.bin)
        install('stream_c.exe', prefix.bin)
        install('stream_f.exe', prefix.bin)
