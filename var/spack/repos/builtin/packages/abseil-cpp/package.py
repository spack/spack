# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AbseilCpp(CMakePackage):
    """Abseil Common Libraries (C++) """

    homepage = "https://abseil.io/"
    url      = "https://github.com/abseil/abseil-cpp/archive/20180600.tar.gz"

    maintainers = ['jcftang']

    version('20200225.1', sha256='0db0d26f43ba6806a8a3338da3e646bb581f0ca5359b3a201d8fb8e4752fd5f8')
    version('20190808', sha256='8100085dada279bf3ee00cd064d43b5f55e5d913be0dfe2906f06f8f28d5b37e')
    version('20181200', sha256='e2b53bfb685f5d4130b84c4f3050c81bf48c497614dc85d91dbd3ed9129bce6d')
    version('20180600', sha256='794d483dd9a19c43dc1fbbe284ce8956eb7f2600ef350dac4c602f9b4eb26e90')

    variant('shared', default=True,
            description='Build shared instead of static libraries')

    conflicts('+shared', when='@:20190808')

    def cmake_args(self):
        args = ["-DBUILD_TESTING=OFF",  "-DCMAKE_CXX_STANDARD=11"]
        args.append('-DBUILD_SHARED_LIBS:Bool={0}'.format(
            'ON' if '+shared' in self.spec else 'OFF'))
        return args
