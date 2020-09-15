# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocmDbgapi(CMakePackage):
    """The AMD Debugger API is a library that provides all the support
       necessary for a debugger and other tools to perform low level
       control of the execution and inspection of execution state of
       AMD's commercially available GPU architectures."""

    homepage = "https://github.com/ROCm-Developer-Tools/ROCdbgapi"
    url      = "https://github.com/ROCm-Developer-Tools/ROCdbgapi/archive/rocm-3.7.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.7.0', sha256='bdeaf81ea8a0ac861a697e435c72cbe767c291638be43f0d09116ad605dfee4f')
    version('3.5.0', sha256='eeba0592bc79b90e5b874bba18fd003eab347e8a3cc80343708f8d19e047e87b')

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0']:
        depends_on('hsa-rocr-dev@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type=('build', 'link'), when='@' + ver)

    def patch(self):
        filter_file(r'(<INSTALL_INTERFACE:include>)',  r'\1 {0}/include'.
                    format(self.spec['hsa-rocr-dev'].prefix), 'CMakeLists.txt')
