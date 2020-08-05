# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocprofilerDev(CMakePackage):
    """ROCPROFILER library for AMD HSA runtime API extension support"""

    homepage = "https://github.com/ROCm-Developer-Tools/rocprofiler"
    url      = "https://github.com/ROCm-Developer-Tools/rocprofiler/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='c42548dd467b7138be94ad68c715254eb56a9d3b670ccf993c43cd4d43659937')

    depends_on('cmake@3:', type='build')
    depends_on('hsakmt-roct@3.5.0:', type='build', when='@3.5.0:')
    depends_on('hsa-rocr-dev@3.5.0:', type='link', when='@3.5.0:')
    depends_on('rocminfo@3.5.0:', type='build', when='@3.5.0:')

    resource(name='roctracer-dev',
             url='https://github.com/ROCm-Developer-Tools/roctracer/archive/rocm-3.5.0.tar.gz',
             sha256='7af5326c9ca695642b4265232ec12864a61fd6b6056aa7c4ecd9e19c817f209e',
             expand=True,
             destination='',
             placement='roctracer')

    def patch(self):
        filter_file('${HSA_RUNTIME_LIB_PATH}/../include',
                    '${HSA_RUNTIME_LIB_PATH}/../include ${HSA_KMT_LIB_PATH}/..\
                     /include', 'test/CMakeLists.txt', string=True)

    def cmake_args(self):
        args = ['-DPROF_API_HEADER_PATH={0}/roctracer/inc/ext'.format(
                self.stage.source_path),
                '-DROCM_ROOT_DIR:STRING={0}/include'.format(
                self.spec['hsakmt-roct'].prefix)
                ]
        return args
