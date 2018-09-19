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


class Nccl(MakefilePackage):
    """Optimized primitives for collective multi-GPU communication."""

    homepage = "https://github.com/NVIDIA/nccl"
    url      = "https://github.com/NVIDIA/nccl/archive/v1.3.4-1.tar.gz"

    version('1.3.4-1', '5b9ce7fbdce0fde68e0f66318e6ff422')
    version('1.3.0-1', 'f6fb1d56913a7d212ca0c300e76f01fb')

    depends_on('cuda')

    @property
    def build_targets(self):
        return ['CUDA_HOME={0}'.format(self.spec['cuda'].prefix)]

    @property
    def install_targets(self):
        return ['PREFIX={0}'.format(self.prefix), 'install']
