# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jali(CMakePackage):
    """Jali is a parallel, unstructured mesh infrastructure library designed
    for use by multi-physics simulations.
    """

    homepage = "https://github.com/lanl/jali"
    git      = "https://github.com/lanl/jali"
    url      = "https://github.com/lanl/jali/archive/1.1.1.tar.gz"

    maintainers = ['raovgarimella']

    version('master', branch='master')
    version('1.1.1', sha256='c96c000b3893ea7f15bbc886524476dd466ae145e77deedc27e412fcc3541207')
    version('1.1.0', sha256='783dfcd6a9284af83bb380ed257fa8b0757dc2f7f9196d935eb974fb6523c644')
    version('1.0.5', sha256='979170615d33a7bf20c96bd4d0285e05a2bbd901164e377a8bccbd9af9463801')

    variant('mstk', default=True, description='Enable MSTK')

    # dependencies
    depends_on('cmake@3.13:', type='build')

    depends_on('mpi')

    depends_on('boost')

    depends_on('mstk@3.3.0: +exodusii+parallel~use_markers partitioner=all', when='+mstk')

    depends_on('zoltan -fortran')
    depends_on('metis')
    depends_on('exodusii')

    # Unit testing variant
    depends_on('unittest-cpp', type='test')

    def cmake_args(self):
        options = []
        if '+with_mstk' in self.spec:
            options.append('-DENABLE_MSTK_Mesh=ON')
        else:
            options.append('-DENABLE_MSTK_Mesh=OFF')

        # Unit test variant
        if self.run_tests:
            options.append('-DENABLE_Tests=ON')
        else:
            options.append('-DENABLE_Tests=OFF')

        return options
