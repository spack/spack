# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmCmake(CMakePackage):
    """rocm-cmake provides CMake modules for common build tasks
       in the ROCm software stack"""

    homepage = "https://github.com/RadeonOpenCompute/rocm-cmake"
    git      = "https://github.com/RadeonOpenCompute/rocm-cmake.git"
    url      = "https://github.com/RadeonOpenCompute/rocm-cmake/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('master', branch='master')

    version('5.0.2', sha256='86a4ae0f84dcf5be95a252295eb732d6a7a271297eed37800a9d492c16474d0c')
    version('5.0.0', sha256='45eb958fac33aafea86fb498127ebf8f567646ce9d7288d46afbd087500553a1')
    version('4.5.2', sha256='85f2ef51327e4b09d81a221b4ad31c97923dabc1bc8ff127dd6c570742185751')
    version('4.5.0', sha256='c77b71454010adbeea5357773aa98dd0725f655f51a411815807cabf29258395')
    version('4.3.1', sha256='acf2a58e2cd486f473194bf01247c52dbf20bd5f6465810fb221470298f2557f')
    version('4.3.0', sha256='bb752d8d2727b7ef2754838e389075dd4212cf5439d099392141f93d05391415')
    version('4.2.0', sha256='299e190ec3d38c2279d9aec762469628f0b2b1867adc082edc5708d1ac785c3b')
    version('4.1.0', sha256='a4521d119fa07954e529d5e717ad1b338992c0694690dbce00fee26c01129c8c', deprecated=True)
    version('4.0.0', sha256='4577487acaa6e041a1316145867584f31caaf0d4aa2dd8fd7f82f81c269cada6', deprecated=True)
    version('3.10.0', sha256='751be4484efdcf0d5fa675480db6e2cddab897de4708c7c7b9fa7adb430b52d7', deprecated=True)
    version('3.9.0', sha256='e0a8db85bb55acb549f360eb9b04f55104aa93e4c3db33f9ba11d9adae2a07eb', deprecated=True)
    version('3.8.0', sha256='9e4be93c76631224eb49b2fa30b0d14c1b3311a6519c8b393da96ac0649d9f30', deprecated=True)
    version('3.7.0', sha256='51abfb06124c2e0677c4d6f7fe83c22fe855cb21386f0053ace09f8ab297058b', deprecated=True)
    version('3.5.0', sha256='5fc09e168879823160f5fdf4fd1ace2702d36545bf733e8005ed4ca18c3e910f', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('cmake@3.6:', type='build', when='@4.1.0:')
