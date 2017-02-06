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


class Archer(Package):
    """ARCHER, a data race detection tool for large OpenMP applications."""

    homepage = "https://github.com/PRUNERS/ARCHER"

    version('1.0.0b', git='https://github.com/PRUNERS/ARCHER.git',
            commit='2cf7ead36358842871d5bd9c33d499f62bf8dd38')

    depends_on('cmake', type='build')
    depends_on('llvm+clang~gold')
    depends_on('ninja', type='build')
    depends_on('llvm-openmp-ompt')

    def install(self, spec, prefix):

        with working_dir('spack-build', create=True):
            cmake_args = std_cmake_args[:]
            cmake_args.extend([
                '-G', 'Ninja',
                '-DCMAKE_C_COMPILER=clang',
                '-DCMAKE_CXX_COMPILER=clang++',
                '-DOMP_PREFIX:PATH=%s' % spec['llvm-openmp-ompt'].prefix,
            ])

            cmake('..', *cmake_args)
            ninja = Executable('ninja')
            ninja()
            ninja('install')
