# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
    git      = "https://github.com/RadeonOpenCompute/atmi.git"
    url      = "https://github.com/RadeonOpenCompute/atmi/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('5.0.2', sha256='3aea040f5a246539ab118f2183cf3e802a21e0e6215a53025eda77f382341747')
    version('5.0.0', sha256='208c1773170722b60b74357e264e698df5871e9d9d490d64011e6ea76750d9cf')
    version('4.5.2', sha256='c235cfb8bdd89deafecf9123264217b8cc5577a5469e3e1f24587fa820d0792e')
    version('4.5.0', sha256='64eeb0244cedae99db7dfdb365e0ad624106cc1090a531f94885ae81e254aabf')
    version('4.3.1', sha256='4497fa6d33547b946e2a51619f2777ec36e9cff1b07fd534eb8a5ef0d8e30650')
    version('4.3.0', sha256='1cbe0e9258ce7cce7b7ccc288335dffbac821ceb745c4f3fd48e2a258abada89')
    version('4.2.0', sha256='c1c89c00d2dc3e764c63b2e51ff7fd5c06d5881ed56aed0adf639582d3389585')
    version('4.1.0', sha256='b31849f86c79f90466a9d67f0a28a93c1675181e38e2a5f571ffc963e4b06f5f', deprecated=True)
    version('4.0.0', sha256='8a2e5789ee7165aff0f0669eecd23ac0a5c8a5bfbc1acd9380fe9a8ed5bffe3a', deprecated=True)
    version('3.10.0', sha256='387e87c622ec334d3ba7a2f4f015ea9a219712722f4c56c1ef572203d0d072ea', deprecated=True)
    version('3.9.0', sha256='0a305e85bab210dd9a0410aa01d46227e00b59141e4675c50d731ad1232ab828', deprecated=True)
    version('3.8.0', sha256='039f0c2b369d0dbc01000754893d9210828f4cb9b36c3e70da8c3819b131c933', deprecated=True)
    version('3.7.0', sha256='8df08489a10ee04cea911811393e0e7d91bd437fc1fd81a23a4e7ab924a974f3', deprecated=True)
    version('3.5.0', sha256='3fb57d2e583fab82bd0582d0c2bccff059ca91122c18ac49a7770a8bb041a37b', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('rsync')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2']:
        depends_on('comgr@' + ver, type='link', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='link', when='@' + ver)
        depends_on('elf', type='link', when='@' + ver)

    root_cmakelists_dir = 'src'

    patch('0001-Remove-relative-link-paths-to-external-libraries.patch', when='@3.5.0')
    patch('0002-Remove-usr-bin-rsync-reference.patch', when='@4.0.0:')

    def cmake_args(self):
        return [
            '-DROCM_VERSION={0}'.format(self.spec.version)
        ]

    @run_after('install')
    def install_stub(self):
        install('include/atmi_interop_hsa.h', self.prefix.include)
