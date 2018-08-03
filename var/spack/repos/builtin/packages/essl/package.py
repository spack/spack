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


class Essl(Package):
    """IBM's Engineering and Scientific Subroutine Library (ESSL)."""

    homepage = "https://www.ibm.com/systems/power/software/essl/"

    variant('ilp64', default=False, description='64 bit integers')
    variant(
        'threads', default='openmp',
        description='Multithreading support',
        values=('openmp', 'none'),
        multi=False
    )
    variant('cuda', default=False, description='CUDA acceleration')

    provides('blas')

    conflicts('+cuda', when='+ilp64',
              msg='ESSL+cuda+ilp64 cannot combine CUDA acceleration'
              ' 64 bit integers')

    conflicts('+cuda', when='threads=none',
              msg='ESSL+cuda threads=none cannot combine CUDA acceleration'
              ' without multithreading support')

    @property
    def blas_libs(self):
        spec = self.spec
        prefix = self.prefix

        if '+ilp64' in spec:
            essl_lib = ['libessl6464']
        else:
            essl_lib = ['libessl']

        if spec.satisfies('threads=openmp'):
            # ESSL SMP support requires XL or Clang OpenMP library
            if '%xl' in spec or '%xl_r' in spec or '%clang' in spec:
                if '+ilp64' in spec:
                    essl_lib = ['libesslsmp6464']
                else:
                    if '+cuda' in spec:
                        essl_lib = ['libesslsmpcuda']
                    else:
                        essl_lib = ['libesslsmp']

        essl_root = prefix.lib64
        essl_libs = find_libraries(
            essl_lib,
            root=essl_root,
            shared=True
        )

        return essl_libs

    def install(self, spec, prefix):
        raise InstallError('IBM ESSL is not installable;'
                           ' it is vendor supplied')
