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


class Nnvm(CMakePackage):
    """nnvm is a modular, decentralized and lightweight
    part to help build deep learning libraries."""

    homepage = "https://github.com/dmlc/nnvm"
    git      = "https://github.com/dmlc/nnvm.git"

    version('master', branch='master')
    version('20170418', commit='b279286304ac954098d94a2695bca599e832effb')

    variant('shared', default=True, description='Build a shared NNVM lib.')

    depends_on('dmlc-core')

    patch('cmake.patch')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DUSE_SHARED_NNVM=%s' % ('ON' if '+shared' in spec else 'OFF'),
            '-DUSE_STATIC_NNVM=%s' % ('ON' if '~shared' in spec else 'OFF'),
        ]
