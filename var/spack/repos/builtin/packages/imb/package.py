##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
from shutil import copyfile
from shutil import copymode
import sys
import os


class Imb(MakefilePackage):
    """Intel MPI Benchmark"""

    homepage = "https://github.com/intel/mpi-benchmarks.git"
    url      = "https://github.com/intel/mpi-benchmarks.git"

    version('master',  git=url)

    depends_on('mpi')

    def edit(self, spec, prefix):
        os.chdir("src")
        makefile = FileFilter('make_ict')
        makefile.filter('CC          = .*', 'CC = %s' %
                            self.spec['mpi'].mpicc)

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        imb = join_path(prefix.bin, "IMB-MPI1")
        copyfile("IMB-MPI1", imb)
        chmod = which('chmod')
        chmod('+x', imb)
