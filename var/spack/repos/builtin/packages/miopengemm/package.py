# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Miopengemm(CMakePackage):
    """An OpenCL general matrix multiplication (GEMM) API
    and kernel generator"""

    homepage = "https://github.com/ROCmSoftwarePlatform/MIOpenGEMM"
    git      = "https://github.com/ROCmSoftwarePlatform/MIOpenGEMM.git"
    url      = "https://github.com/ROCmSoftwarePlatform/MIOpenGEMM/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    def url_for_version(self, version):
        if version == Version('1.1.6'):
            return "https://github.com/ROCmSoftwarePlatform/MIOpenGEMM/archive/1.1.6.tar.gz"
        url = "https://github.com/ROCmSoftwarePlatform/MIOpenGEMM/archive/rocm-{0}.tar.gz"
        return url.format(version)

    version('5.1.0', sha256='e2b20cdc20a745bcb7a554852e6b4bd39274c7dcc13fc19a81a282fb4dfa475f')
    version('5.0.2', sha256='64a6bf7c902af63d85563e29361763e9daa1fd3699490a91c222b057673612cc')
    version('5.0.0', sha256='122cfb4e79476092e84f73f48540701c90fb87e0dc20cdf39f202d92e9ff5544')
    version('4.5.2', sha256='e778e0ccb123cd637ac459b2aecdf0fdead158580479bc0adfc9a28879e1d1c9')
    version('4.5.0', sha256='54ec908109a91f9022b61e63e3a1b9706cdcf133ba6fb3b39a65ca0e79be7747')
    version('4.3.1', sha256='0aee2281d9b8c625e9bda8efff3067237d6155a53f6c720dcb4e3b3ec8bf8d14', deprecated=True)
    version('4.3.0', sha256='d32b3b98e695b7db2fd2faa6587a57728d1252d6d649dcb2db3102f98cd5930e', deprecated=True)
    version('4.2.0', sha256='a11fa063248ed339fe897ab4c5d338b7279035fa37fcbe0909e2c4c352aaefb1', deprecated=True)
    version('4.1.0', sha256='389328eb4a16565853691bd5b01a0eab978d99e3217329236ddc63a38b8dd4eb', deprecated=True)
    version('4.0.0', sha256='366d03facb1ec5f6f4894aa88859df1d7fea00fee0cbac5173d7577e9a8ba799', deprecated=True)
    version('3.10.0', sha256='66d844a17729ab25c1c2a243667d9714eb89fd51e42bfc014e2faf54a8642064', deprecated=True)
    version('3.9.0', sha256='8e1273c35d50e9fd92e303d9bcbdd42ddbfda20844b3248428e16b54928f6dc2', deprecated=True)
    version('3.8.0', sha256='d76f5b4b3b9d1e3589a92f667f39eab5b5ab54ec3c4e04d412035be3ec623547', deprecated=True)
    version('3.7.0', sha256='392b280ca564b120f6b24ec1fe8782cba08a8a5fb52938e8bc3dc887d3fd08fa', deprecated=True)
    version('1.1.6', sha256='9ab04903794c6a59432928eaec92c687d51e2b4fd29630cf227cbc49d56dc69b', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('rocm-cmake@3.5.0', type='build', when='@1.1.6')
    depends_on('rocm-opencl@3.5.0',              when='@1.1.6')

    for ver in ['3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0',
                '5.0.2', '5.1.0']:
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('rocm-opencl@' + ver,              when='@' + ver)
