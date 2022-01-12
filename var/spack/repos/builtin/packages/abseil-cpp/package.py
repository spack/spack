# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AbseilCpp(CMakePackage):
    """Abseil Common Libraries (C++) """

    homepage = "https://abseil.io/"
    url      = "https://github.com/abseil/abseil-cpp/archive/20210324.2.tar.gz"

    maintainers = ['jcftang']

    version('20210324.2', sha256='59b862f50e710277f8ede96f083a5bb8d7c9595376146838b9580be90374ee1f')
    version('20210324.1', sha256='441db7c09a0565376ecacf0085b2d4c2bbedde6115d7773551bc116212c2a8d6')
    version('20210324.0', sha256='dd7db6815204c2a62a2160e32c55e97113b0a0178b2f090d6bab5ce36111db4b')
    version('20200923.3', sha256='ebe2ad1480d27383e4bf4211e2ca2ef312d5e6a09eba869fd2e8a5c5d553ded2')
    version('20200923.2', sha256='bf3f13b13a0095d926b25640e060f7e13881bd8a792705dd9e161f3c2b9aa976')
    version('20200923.1', sha256='808350c4d7238315717749bab0067a1acd208023d41eaf0c7360f29cc8bc8f21')
    version('20200225.2', sha256='f41868f7a938605c92936230081175d1eae87f6ea2c248f41077c8f88316f111')
    version('20200225.1', sha256='0db0d26f43ba6806a8a3338da3e646bb581f0ca5359b3a201d8fb8e4752fd5f8')
    version('20190808', sha256='8100085dada279bf3ee00cd064d43b5f55e5d913be0dfe2906f06f8f28d5b37e')
    version('20181200', sha256='e2b53bfb685f5d4130b84c4f3050c81bf48c497614dc85d91dbd3ed9129bce6d')
    version('20180600', sha256='794d483dd9a19c43dc1fbbe284ce8956eb7f2600ef350dac4c602f9b4eb26e90')

    variant('shared', default=True,
            description='Build shared instead of static libraries')

    conflicts('+shared', when='@:20190808')

    variant('cxxstd', values=('11', '14', '17', '20'), default='11',
            description="C++ standard used during compilation")

    def cmake_args(self):
        shared = 'ON' if '+shared' in self.spec else 'OFF'
        cxxstd = self.spec.variants['cxxstd'].value
        return [
            self.define('BUILD_TESTING', 'OFF'),
            self.define('BUILD_SHARED_LIBS:Bool', shared),
            self.define('CMAKE_CXX_STANDARD', cxxstd)
        ]
