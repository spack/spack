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


class Functionalizer(CMakePackage):
    """Apply several steps of filtering on touches
    """
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/building/Functionalizer"
    git      = "ssh://bbpcode.epfl.ch/building/Functionalizer"

    version('develop', submodules=True)
    version('3.12.2', tag='v3.12.2', submodules=True)
    version('3.12.1', tag='v3.12.1', submodules=True)
    version('3.12.0', tag='v3.12.0', submodules=True)
    version('3.11.0',
            commit='50c83265c100cec66a27eea9311b58a9b652cb5f',
            submodules=True)
    version('gap-junctions',
            commit='6095a851119d8125a81f2858c7a0de2ff6f012d6',
            submodules=True)

    depends_on('boost@1.50:')
    depends_on('cmake', type='build')
    depends_on('cmake@:3.0.0', type='build', when='@gap-junctions')
    depends_on('hpctools~openmp')
    depends_on('hpctools~openmp@:3.1', when='@gap-junctions')
    depends_on('hdf5@1.8:')
    depends_on('libxml2')
    depends_on('pkg-config', type='build')
    depends_on('mpi')
    depends_on('zlib')

    def patch(self):
        """Prevent `-isystem /usr/include` from appearing, since this confuses gcc.
        """
        if self.spec.satisfies('@gap-junctions'):
            return
        filter_file(r'(include_directories\()SYSTEM ',
                    r'\1',
                    'functionalizer/CMakeLists.txt')

    def cmake_args(self):
        args = [
            '-DCMAKE_C_COMPILER={}'.format(self.spec['mpi'].mpicc),
            '-DCMAKE_CXX_COMPILER={}'.format(self.spec['mpi'].mpicxx)
        ]
        return args
