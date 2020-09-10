# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Atmi(CMakePackage):
    """Asynchronous Task and Memory Interface, or ATMI, is a runtime framework
       and programming model for heterogeneous CPU-GPU systems. It provides a
       consistent, declarative API to create task graphs on CPUs and GPUs
       (integrated and discrete)."""

    homepage = "https://github.com/RadeonOpenCompute/atmi"
    url      = "https://github.com/RadeonOpenCompute/atmi/archive/rocm-3.7.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.7.0', sha256='8df08489a10ee04cea911811393e0e7d91bd437fc1fd81a23a4e7ab924a974f3')
    version('3.5.0', sha256='3fb57d2e583fab82bd0582d0c2bccff059ca91122c18ac49a7770a8bb041a37b')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')
    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0']:
        depends_on('comgr@' + ver, type='link', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='link', when='@' + ver)
        depends_on('libelf@0.8:', type='link', when='@' + ver)

    root_cmakelists_dir = 'src'

    patch('0001-Remove-relative-link-paths-to-external-libraries.patch', when='@3.5.0')

    def cmake_args(self):
        return [
            '-DROCM_VERSION={0}'.format(self.spec.version)
        ]

    @run_after('install')
    def install_stub(self):
        install('include/atmi_interop_hsa.h', self.prefix.include)
