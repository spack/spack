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

    depends_on('intel-oneapi-tbb')

    provides('fftw-api@3')
    provides('scalapack')
    provides('mkl')
    provides('lapack')
    provides('blas')

    @property
    def component_dir(self):
        return 'mkl'

    @property
    def libs(self):
        lib_path = join_path(self.component_path, 'lib', 'intel64')
        mkl_libs = ['libmkl_intel_lp64', 'libmkl_sequential', 'libmkl_core']
        libs = find_libraries(mkl_libs, root=lib_path, shared=True, recursive=False)
        libs += find_system_libraries(['libpthread', 'libm', 'libdl'], shared=True)
        return libs
