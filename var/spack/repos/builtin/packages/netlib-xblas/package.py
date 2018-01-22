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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install netlib-xblas
#
# You can edit this file again by typing:
#
#     spack edit netlib-xblas
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class NetlibXblas(AutotoolsPackage):
    """XBLAS is a reference implementation for the dense and banded BLAS
       routines, along with extended and mixed precision version. Extended
       precision is only used internally; input and output arguments remain
       the same as in the existing BLAS. Extra precisions is implemented as
       double-double (i.e., 128-bit total, 106-bit significand). Mixed
       precision permits some input/output arguments of different types
       (mixing real and complex) or precisions (mixing single and
       double). This implementation is proof of concept, and no attempt was
       made to optimize performance; performance should be as good as
       straightforward but careful code written by hand."""

    homepage = "http://www.netlib.org/xblas"
    url      = "http://www.netlib.org/xblas/xblas.tar.gz"

    version('1.0.248', '990c680fb5e446bb86c10936e4cd7f88')

    provides('blas')

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        install('libxblas.a', prefix.lib)
        # XBLAS should be a drop-in BLAS replacement
        install('libxblas.a', join_path(prefix.lib, 'libblas.a'))

        headers = ['f2c-bridge.h',
                   'blas_dense_proto.h',
                   'blas_enum.h',
                   'blas_extended.h',
                   'blas_extended_private.h',
                   'blas_extended_proto.h',
                   'blas_fpu.h',
                   'blas_malloc.h']
        mkdirp(prefix.include)
        for h in headers:
            install(join_path('src', h), prefix.include)

        return
