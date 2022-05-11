# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmDbgapi(CMakePackage):
    """The AMD Debugger API is a library that provides all the support
       necessary for a debugger and other tools to perform low level
       control of the execution and inspection of execution state of
       AMD's commercially available GPU architectures."""

    homepage = "https://github.com/ROCm-Developer-Tools/ROCdbgapi"
    git      = "https://github.com/ROCm-Developer-Tools/ROCdbgapi.git"
    url      = "https://github.com/ROCm-Developer-Tools/ROCdbgapi/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('master', branch='amd-master')
    version('5.1.0', sha256='406db4b20bda12f6f32cbef88b03110aa001bf7bef6676f36e909b53c8354e43')
    version('5.0.2', sha256='b7554dfe96bda6c2ee762ad6e3e5f91f0f52b5a525e3fb29d5e1fe6f003652b5')
    version('5.0.0', sha256='cff72d7fe43ff791c4117fe87d57314cbebdbcb70002a0411b8a44761012a495')
    version('4.5.2', sha256='9fa574e8389ef69d116caf714af2f938777e0aeeaadd7fad451cf5d2e6699c6e')
    version('4.5.0', sha256='583bbf18df593f376c4cc70f25b68c191bd38fde20a336c0f5c8e5d85fda2fcf')
    version('4.3.1', sha256='dddf2549ad6bb806f7e5d5a5336f5a00fe87a124f2a778be18ec4dc41f891912')
    version('4.3.0', sha256='4255d83d218bb0db8be9fef18e03a955ea1c6de1c635c31685ee5fc1540ddde6')
    version('4.2.0', sha256='fcdee5aaf5ed40c0377ce007a2947da9e718eeee86ca3e13192ff9e96a1b7373')
    version('4.1.0', sha256='d04fd9b2005691313547c4134b027b56b0ec6089f67d3bccbdb8fb1c92cde9bd', deprecated=True)
    version('4.0.0', sha256='e87f31b3a22861397eb62d8363dd1e153596097ccfe68c6eefc1a83a2432ae18', deprecated=True)
    version('3.10.0', sha256='89a8d352d59e4c0dc13160b1bf1f4bc3bfec5af544050030aa619b1ff88f1850', deprecated=True)
    version('3.9.0', sha256='d1553f89d2b0419304ea82ed2b97abdc323c2fed183f0e119da1a72416a48136', deprecated=True)
    version('3.8.0', sha256='760ff77c6578f3548f367a8bd3dda8680b7519f6b20216755105b87785d1e3f8', deprecated=True)
    version('3.7.0', sha256='bdeaf81ea8a0ac861a697e435c72cbe767c291638be43f0d09116ad605dfee4f', deprecated=True)
    version('3.5.0', sha256='eeba0592bc79b90e5b874bba18fd003eab347e8a3cc80343708f8d19e047e87b', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0',
                '5.0.2', '5.1.0', 'master']:
        depends_on('hsa-rocr-dev@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type=('build', 'link'), when='@' + ver)

    def patch(self):
        filter_file(r'(<INSTALL_INTERFACE:include>)',  r'\1 {0}/include'.
                    format(self.spec['hsa-rocr-dev'].prefix), 'CMakeLists.txt')
