# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rdc(CMakePackage):
    """ROCm Data Center Tool"""

    homepage = "https://github.com/RadeonOpenCompute/rdc"
    url      = "https://github.com/RadeonOpenCompute/rdc/archive/rocm-3.8.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.8.0', sha256='d0d0a0e68a848b7a8fa2d88c1d0352ce68e1e142debf32c31d941904f03c4b2f')

    depends_on('cmake@3.15:', type='build')
    depends_on('grpc@1.28.1+shared', type='build')
    depends_on('protobuf', type=('build', 'link'))
    depends_on('rocm-smi-lib@3.8.0', type=('build', 'link'))
    depends_on('libcap', type=('build', 'link'))

    def patch(self):
        filter_file(
            r'\${ROCM_DIR}/rocm_smi', '${ROCM_SMI_DIR}', 'CMakeLists.txt')
        filter_file(
            r'${GRPC_ROOT}/bin/protoc',
            '{0}/bin/protoc'.format(self.spec['protobuf'].prefix),
            'CMakeLists.txt', string=True)

    def cmake_args(self):
        rpath = self.rpath
        rpath.append(self.prefix.opt.rocm.rdc.lib)
        rpath = ';'.join(rpath)
        args = ['-DCMAKE_INSTALL_RPATH=' + rpath,
                '-DGRPC_ROOT=' + self.spec['grpc'].prefix,
                '-DCMAKE_MODULE_PATH={0}/cmake_modules'.format
                (self.stage.source_path),
                '-DROCM_SMI_DIR=' + self.spec['rocm-smi-lib'].prefix,
                '-DCMAKE_BUILD_WITH_INSTALL_RPATH=1']
        return args
