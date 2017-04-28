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


class Bamtools(Package):
    """C++ API & command-line toolkit for working with BAM data."""

    homepage = "https://github.com/pezmaster31/bamtools"
    url      = "https://github.com/pezmaster31/bamtools/archive/v2.4.0.tar.gz"

    version('2.4.1', '41cadf513f2744256851accac2bc7baa')
    version('2.4.0', '6139d00c1b1fe88fe15d094d8a74d8b9')
    version('2.3.0', 'd327df4ba037d6eb8beef65d7da75ebc')
    version('2.2.3', '6eccd3e45e4ba12a68daa3298998e76d')

    depends_on('cmake', type='build')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)

            make()
            make('install')
