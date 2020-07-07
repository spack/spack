# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Atmi(CMakePackage):
    """Asynchronous Task and Memory Interface, or ATMI, is a runtime framework and programming model for heterogeneous CPU-GPU systems. It provides a consistent, declarative API to create task graphs on CPUs and GPUs (integrated and discrete)."""
       
    homepage = "https://github.com/RadeonOpenCompute/atmi"
    url      = "https://github.com/RadeonOpenCompute/atmi/archive/rocm-3.5.0.tar.gz"
    
    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='3fb57d2e583fab82bd0582d0c2bccff059ca91122c18ac49a7770a8bb041a37b')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')
    depends_on('cmake@3.5.2', type='build')
    depends_on('comgr@3.5:', type='build', when='@3.5:')
    depends_on('hsa-rocr-dev@3.5:', type='build',when='@3.5:')
    depends_on('libelf@0.8:', type='build',when='@3.5:')
    root_cmakelists_dir = 'src'

    def cmake_args(self):
        # workaround as it was checking for /opt/rocm/.info/version in the make file
        spec=self.spec
        args = [
                '-DROCM_VERSION=3.5.0-2588',
                '-DCMAKE_VERBOSE_MAKEFILE=1',
                '-DCMAKE_PREFIX_PATH={}/include/hsa;{}/hsa/lib;{}/include;{}/lib;{}/include;{}/lib'.format(spec['hsa-rocr-dev'].prefix, spec['hsa-rocr-dev'].prefix, spec['hsakmt-roct'].prefix, spec['hsakmt-roct'].prefix, spec['libelf'].prefix, spec['libelf'].prefix)
               ]
        return args

    @run_after('install')
    def install_stub(self):
        install('include/atmi_interop_hsa.h', self.prefix.include)

