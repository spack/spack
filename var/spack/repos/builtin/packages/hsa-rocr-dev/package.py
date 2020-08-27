# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class HsaRocrDev(CMakePackage):
    """This repository includes the user mode API nterfaces and libraries
       necessary for host applications to launch computer kernels to available
       HSA ROCm kernel agents.AMD Heterogeneous System Architecture HSA -
       Linux HSA Runtime for Boltzmann (ROCm) platforms."""

    homepage = "https://github.com/RadeonOpenCompute/ROCR-Runtime"
    url      = "https://github.com/RadeonOpenCompute/ROCR-Runtime/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='52c12eec3e3404c0749c70f156229786ee0c3e6d3c979aed9bbaea500fa1f3b8')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    for ver in ['3.5.0']:
        depends_on('hsakmt-roct@' + ver, type=('link', 'run'), when='@' + ver)
        depends_on('libelf@0.8:', type='link', when="@" + ver)

    depends_on('cmake@3:', type="build")

    patch('0001-Do-not-set-an-explicit-rpath-by-default-since-packag.patch', when='@3.5.0')

    root_cmakelists_dir = 'src'

    def cmake_args(self):
        libelf_include = self.spec['libelf'].prefix.include.libelf
        args = ['-DLIBELF_INCLUDE_DIRS=%s' % libelf_include]
        return args
