# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Libblastrampoline(MakefilePackage):
    """Using PLT trampolines to provide a BLAS and LAPACK demuxing library."""

    homepage = "https://github.com/JuliaLinearAlgebra/libblastrampoline"
    git      = "https://github.com/JuliaLinearAlgebra/libblastrampoline.git"
    url      = "https://github.com/JuliaLinearAlgebra/libblastrampoline/archive/refs/tags/v3.1.0.tar.gz"

    maintainers = ['haampie', 'giordano']

    version('5.0.2', sha256='2e96fa62957719351da3e4dff8cd0949449073708f5564dae0a224a556432356')
    version('5.0.1', sha256='1066b4d157276e41ca66ca94f0f8c2900c221b49da2df3c410e6f8bf1ce9b488')
    # v5.0.0 contains a bug, fixed in v5.0.1, which causes segmentation faults
    version('5.0.0', sha256='20f434add7d9ae4503bb7a61e320ad1aea8e8371f53b1e32dc691e4701080658', deprecated=True)
    version('4.1.0', sha256='8b1a3a55b1e1a849e907288e3afbd10d367b25364a59cb2ccaddc88604b13266')
    version('4.0.0', sha256='8816dfba6f0c547bca5fba9d83e63062387def3089622a9514babf79e1737310')
    version('3.1.0', sha256='f6136cc2b5d090ceca67cffa55b4c8af4bcee874333d49297c867abdb0749b5f')
    version('3.0.4', sha256='3c8a54a3bd8a2737b7f74ebeb56df8e2a48083c9094dbbff80b225c228e31793')
    version('3.0.3', sha256='a9c553ee6f20fa2f92098edcb3fc4a331c653250e559f72b9317b4ee84500cd7')
    version('3.0.2', sha256='caefd708cf0cf53b01cea74a09ab763bf4dfa4aec4468892720f3921521c1f74')
    version('3.0.1', sha256='b5b8ac0d3aba1bcb9dc26d7d6bb36b352d45e7d7e2594c6122e72b9e5d75a772')
    version('3.0.0', sha256='4d0856d30e7ba0cb0de08b08b60fd34879ce98714341124acf87e587d1bbbcde')
    version('2.2.0', sha256='1fb8752891578b45e187019c67fccbaafb108756aadc69bdd876033846ad30d3')

    build_directory = 'src'

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make('prefix={0}'.format(prefix), 'install')
