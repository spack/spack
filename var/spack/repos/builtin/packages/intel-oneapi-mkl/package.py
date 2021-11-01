# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import platform

from spack import *


class IntelOneapiMkl(IntelOneApiLibraryPackage):
    """Intel oneAPI MKL."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onemkl.html'

    if platform.system() == 'Linux':
        version('2021.4.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18222/l_onemkl_p_2021.4.0.640_offline.sh',
                sha256='9ad546f05a421b4f439e8557fd0f2d83d5e299b0d9bd84bdd86be6feba0c3915',
                expand=False)
        version('2021.3.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17901/l_onemkl_p_2021.3.0.520_offline.sh',
                sha256='a06e1cdbfd8becc63440b473b153659885f25a6e3c4dcb2907ad9cd0c3ad59ce',
                expand=False)
        version('2021.2.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17757/l_onemkl_p_2021.2.0.296_offline.sh',
                sha256='816e9df26ff331d6c0751b86ed5f7d243f9f172e76f14e83b32bf4d1d619dbae',
                expand=False)
        version('2021.1.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17402/l_onemkl_p_2021.1.1.52_offline.sh',
                sha256='818b6bd9a6c116f4578cda3151da0612ec9c3ce8b2c8a64730d625ce5b13cc0c',
                expand=False)

    variant('ilp64', default=False,
            description='Build with ILP64 support')

    depends_on('intel-oneapi-tbb')

    provides('fftw-api@3')
    provides('scalapack')
    provides('mkl')
    provides('lapack')
    provides('blas')

    @property
    def component_dir(self):
        return 'mkl'

    def xlp64_lib(self, lib):
        return lib + ('_ilp64'
                      if '+ilp64' in self.spec
                      else '_lp64')

    @property
    def headers(self):
        include_path = join_path(self.component_path, 'include')
        return find_headers('*', include_path)

    @property
    def libs(self):
        mkl_libs = [self.xlp64_lib('libmkl_intel'), 'libmkl_sequential', 'libmkl_core']
        libs = find_libraries(mkl_libs,
                              join_path(self.component_path, 'lib', 'intel64'))
        libs += find_system_libraries(['libpthread', 'libm', 'libdl'])
        return libs
