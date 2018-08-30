##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


class Branson(CMakePackage):
    """Branson's purpose is to study different algorithms for parallel Monte
    Carlo transport. Currently it contains particle passing and mesh passing
    methods for domain decomposition."""

    homepage = "https://github.com/lanl/branson"
    url      = "https://github.com/lanl/branson/archive/1.01.zip"
    git      = "https://github.com/lanl/branson.git"

    tags = ['proxy-app']

    version('develop', branch='develop')
    version('1.01', 'cf7095a887a8dd7d417267615bd0452a')

    depends_on('mpi@2:')
    depends_on('boost')
    depends_on('metis')
    depends_on('parmetis')

    root_cmakelists_dir = 'src'

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append('-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc)
        args.append('-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx)
        args.append('-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc)
        return args

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.doc)
        install('spack-build/BRANSON', prefix.bin)
        install('LICENSE.txt', prefix.doc)
        install('README.md', prefix.doc)
