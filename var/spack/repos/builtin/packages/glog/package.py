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


class Glog(Package):
    """C++ implementation of the Google logging module."""

    homepage = "https://github.com/google/glog"
    url      = "https://github.com/google/glog/archive/v0.3.5.tar.gz"

    version('0.3.5', '5df6d78b81e51b90ac0ecd7ed932b0d4')
    version('0.3.4', 'df92e05c9d02504fb96674bc776a41cb')
    version('0.3.3', 'c1f86af27bd9c73186730aa957607ed0')

    depends_on('gflags')
    depends_on('cmake', when="@0.3.5:")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make('install')

    @when('@0.3.5:')
    def install(self, spec, prefix):
        cmake_args = ['-DBUILD_SHARED_LIBS=TRUE']
        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make('install')
