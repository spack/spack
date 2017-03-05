##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Serban Maerean, serban@us.ibm.com, All rights reserved.
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


class Magma(CMakePackage):
    """The MAGMA project aims to develop a dense linear algebra library
    similar to LAPACK but for heterogeneous/hybrid architectures,
    starting with current "Multicore+GPU" systems.
    """

    homepage = "http://icl.cs.utk.edu/magma/"
    url = "http://icl.cs.utk.edu/projectsfiles/magma/downloads/magma-2.2.0.tar.gz"

    version('2.2.0', '6c1ebf4cdf63eb302ff6258ff8c49217')

    variant('fortran', default=True,
            description='Enable Fortran bindings support')

    depends_on('lapack')

    patch('ibm-xl.patch', when='@2.2:%xl')
    patch('ibm-xl.patch', when='@2.2:%xl_r')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([
            '-DCMAKE_INSTALL_PREFIX=%s' % prefix,
            '-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix,
            '-DLAPACK_LIBRARIES=%s;%s' % (spec['blas'].libs,
                                          spec['lapack'].libs)
        ])

        if '+fortran' in spec:
            options.extend([
                '-DUSE_FORTRAN=yes'
            ])
            if spec.satisfies('%xl') or spec.satisfies('%xl_r'):
                options.extend([
                    '-DCMAKE_Fortran_COMPILER=%s' % self.compiler.f77
                ])

        return options
