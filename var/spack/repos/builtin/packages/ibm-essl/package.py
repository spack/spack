##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class IbmEssl(Package):
    """Engineering and Scientific Subroutine Library (ESSL)."""

    homepage = "https://www.ibm.com/systems/power/software/essl/"
    url      = "ibm-essl"

    variant('ilp64', default=False, description='64 bit integers')
    variant(
        'threads', default='openmp',
        description='Multithreading support',
        values=('openmp', 'none'),
        multi=False
    )
    variant('cuda', default=False, description='CUDA acceleration')

    provides('blas')
    provides('essl')

    @property
    def blas_libs(self):
        spec = self.spec
        prefix = self.prefix

        if spec.satisfies('threads=openmp'):
            # ESSL SMP support requires XL OpenMP library
            if '%xl' in spec or '%clang' in spec:
                if '+ilp64' in spec:
                    if '+cuda' in spec:
                        raise InstallError(
                            "IBM's ESSL does not support 64bit Integers with "
                            "CUDA acceleration")
                    else:
                        essl_lib = ['libesslsmp6464']
                else:
                    essl_lib = ['libesslsmp']
            else:
                if '+ilp64' in spec:
                    if '+cuda' in spec:
                        raise InstallError(
                            "IBM's ESSL does not support 64bit Integers with "
                            "CUDA acceleration")
                    else:
                        essl_lib = ['libessl6464']
                else:
                    essl_lib = ['libessl']
        else:
            if '+ilp64' in spec:
                if '+cuda' in spec:
                    raise InstallError(
                        "IBM's ESSL does not support 64bit Integers with "
                        "CUDA acceleration")
                else:
                    essl_lib = ['libessl6464']
            else:
                essl_lib = ['libessl']

        essl_root = prefix.lib64

        essl_libs = find_libraries(
            essl_lib,
            root=essl_root,
            shared=True
        )

        return essl_libs
