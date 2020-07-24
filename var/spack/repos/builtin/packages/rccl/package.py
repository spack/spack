# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rccl(CMakePackage):
    """RCCL (pronounced "Rickle") is a stand-alone library
    of standard collective communication routines for GPUs,
    implementing all-reduce, all-gather, reduce, broadcast,
    and reduce-scatter."""

    homepage = "https://github.com/RadeonOpenCompute/rccl"
    url      = "https://github.com/ROCmSoftwarePlatform/rccl/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='290b57a66758dce47d0bfff3f5f8317df24764e858af67f60ddcdcadb9337253')

    depends_on('cmake@3.5.2', type='build')
    depends_on('rocm-cmake@3.5:', type='build', when='@3.5:')
    depends_on('hip@3.5:', type='build', when='@3.5:')
    depends_on('comgr@3.5:', type='build', when='@3.5:')
    depends_on('rocm-device-libs@3.5:', type='build', when='@3.5:')

    def patch(self):
        filter_file(
            'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/../include"',
            'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"',
            'rccl-targets.cmake', string=True)

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DCMAKE_CXX_COMPILER={}/hipcc'.format(spec['hip'].prefix.bin),
            '-DCMAKE_PREFIX_PATH={}'.format(spec['hip'].prefix)
        ]

        return args
