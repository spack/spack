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


class Raja(CMakePackage):
    """RAJA Parallel Framework."""
    homepage = "http://software.llnl.gov/RAJA/"

    version('master', git='https://github.com/LLNL/RAJA.git', branch='master', submodules='True')
    version('develop', git='https://github.com/LLNL/RAJA.git', branch='develop', submodules='True')
    version('0.5.3', git='https://github.com/LLNL/RAJA.git', tag='v0.5.3', submodules="True")
    version('0.5.2', git='https://github.com/LLNL/RAJA.git', tag='v0.5.2', submodules="True")
    version('0.5.1', git='https://github.com/LLNL/RAJA.git', tag='v0.5.1', submodules="True")
    version('0.5.0', git='https://github.com/LLNL/RAJA.git', tag='v0.5.0', submodules="True")
    version('0.4.1', git='https://github.com/LLNL/RAJA.git', tag='v0.4.1', submodules="True")
    version('0.4.0', git='https://github.com/LLNL/RAJA.git', tag='v0.4.0', submodules="True")

    variant('cuda', default=False, description='Build with CUDA backend')
    variant('openmp', default=True, description='Build OpenMP backend')

    depends_on('cuda', when='+cuda')

    depends_on('cmake@3.3:', type='build')

    def cmake_args(self):
        spec = self.spec

        options = []

        if '+openmp' in spec:
            options.extend([
                '-DENABLE_OPENMP=On'])

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=On',
                '-DCUDA_TOOLKIT_ROOT_DIR=%s' % (spec['cuda'].prefix)])

        return options
