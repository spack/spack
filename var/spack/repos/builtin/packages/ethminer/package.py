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


class Ethminer(CMakePackage):
    """The ethminer is an Ethereum GPU mining worker."""

    homepage = "https://github.com/ethereum-mining/ethminer"
    url = "https://github.com/ethereum-mining/ethminer/archive/v0.12.0.tar.gz"

    version('0.12.0', '1c7e3df8476a146702a4050ad984ae5a')

    variant('opencl', default=True, description='Enable OpenCL mining.')
    variant('cuda', default=False, description='Enable CUDA mining.')
    variant('stratum', default=True,
            description='Build with Stratum protocol support.')

    depends_on('python')
    depends_on('boost')
    depends_on('json-c')
    depends_on('curl')
    depends_on('zlib')
    depends_on('cuda', when='+cuda')
    depends_on('mesa', when='+opencl')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DETHASHCL=%s' % ('YES' if '+opencl' in spec else 'NO'),
            '-DETHASHCUDA=%s' % ('YES' if '+cuda' in spec else 'NO'),
            '-DETHSTRATUM=%s' % ('YES' if '+stratum' in spec else 'NO')]
