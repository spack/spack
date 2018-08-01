##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class DmlcCore(CMakePackage):
    """DMLC-Core is the backbone library to support all DMLC projects,
    offers the bricks to build efficient and scalable
    distributed machine learning libraries."""

    homepage = "https://github.com/dmlc/dmlc-core"
    git      = "https://github.com/dmlc/dmlc-core.git"

    version('master')
    version('20170508', commit='a6c5701219e635fea808d264aefc5b03c3aec314')

    variant('openmp', default=False, description='Enable OpenMP support')

    patch('cmake.patch')

    def patch(self):
        filter_file('export CC = gcc', '', 'make/config.mk', string=True)
        filter_file('export CXX = g++', '', 'make/config.mk', string=True)
        filter_file('export MPICXX = mpicxx', '',
                    'make/config.mk', string=True)
        filter_file(r'^USE_OPENMP\s*=.*',
                    'USE_OPENMP=%s' % ('1' if '+openmp' in self.spec else '0'),
                    'make/config.mk')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DUSE_OPENMP=%s' % ('ON' if '+openmp' in spec else 'OFF'),
        ]
