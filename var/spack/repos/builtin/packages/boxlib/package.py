# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Boxlib(CMakePackage):
    """BoxLib, a software framework for massively parallel
       block-structured adaptive mesh refinement (AMR) codes."""

    homepage = "https://ccse.lbl.gov/BoxLib/"
    url = "https://github.com/BoxLib-Codes/BoxLib/archive/16.12.2.tar.gz"

    version('16.12.2', 'a28d92a5ff3fbbdbbd0a776a59f18526')

    depends_on('mpi')

    variant('dims', default='3', values=('1', '2', '3'), multi=False,
            description='Number of spatial dimensions')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend([
            '-DBL_SPACEDIM=%d' % int(spec.variants['dims'].value),
            '-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON',
            '-DENABLE_FBASELIB=ON',
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc
        ])

        return options
