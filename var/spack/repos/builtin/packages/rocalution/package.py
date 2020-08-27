# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rocalution(CMakePackage):
    """rocALUTION is a sparse linear algebra library with focus on
       exploring fine-grained parallelism on top of AMD's Radeon Open
       eCosystem Platform ROCm runtime and toolchains, targeting modern
       CPU and GPU platforms. Based on C++ and HIP, it provides a portable,
        generic and flexible design that allows seamless integration with
       other scientific software packages."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocALUTION"
    url      = "https://github.com/ROCmSoftwarePlatform/rocALUTION/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='be2f78c10c100d7fd9df5dd2403a44700219c2cbabaacf2ea50a6e2241df7bfe')

    depends_on('cmake@3.5.2', type='build')
    for ver in ['3.5.0']:
        depends_on('hip@' + ver,  when='@' + ver)
        depends_on('rocblas@' + ver, type='build', when='@' + ver)
        depends_on('rocsparse@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('rocprim@' + ver, type='build', when='@' + ver)

    patch('0001-fix-hip-build-error.patch')

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        args = [
            '-DSUPPORT_OMP=ON',
            '-DSUPPORT_HIP=ON',
            '-DSUPPORT_MPI=OFF',
            '-DBUILD_CLIENTS_SAMPLES=OFF'
        ]
        return args
