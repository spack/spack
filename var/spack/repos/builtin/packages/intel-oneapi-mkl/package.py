# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
        version('2022.1.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18721/l_onemkl_p_2022.1.0.223_offline.sh',
                sha256='4b325a3c4c56e52f4ce6c8fbb55d7684adc16425000afc860464c0f29ea4563e',
                expand=False)
        version('2022.0.2',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18483/l_onemkl_p_2022.0.2.136_offline.sh',
                sha256='134b748825a474acc862bb4a7fada99741a15b7627cfaa6ba0fb05ec0b902b5e',
                expand=False)
        version('2022.0.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18444/l_onemkl_p_2022.0.1.117_offline.sh',
                sha256='22afafbe2f3762eca052ac21ec40b845ff2f3646077295c88c2f37f80a0cc160',
                expand=False)
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

    variant('shared', default=True, description='Builds shared library')
    variant('ilp64', default=False,
            description='Build with ILP64 support')
    variant('cluster', default=False,
            description='Build with cluster support: scalapack, blacs, etc')

    depends_on('intel-oneapi-tbb')
    # cluster libraries need mpi
    depends_on('mpi', when='+cluster')

    provides('fftw-api@3')
    provides('scalapack', when='+cluster')
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

    # provide cluster libraries if +cluster variant is used or
    # the scalapack virtual package was requested
    def cluster(self):
        return '+cluster' in self.spec

    @property
    def libs(self):
        shared = '+shared' in self.spec
        mkl_libs = []
        if self.cluster():
            mkl_libs += [self.xlp64_lib('libmkl_scalapack'),
                         'libmkl_cdft_core']
        mkl_libs += [self.xlp64_lib('libmkl_intel'),
                     'libmkl_sequential',
                     'libmkl_core']
        if self.cluster():
            mkl_libs += [self.xlp64_lib('libmkl_blacs_intelmpi')]
        libs = find_libraries(mkl_libs,
                              join_path(self.component_path, 'lib', 'intel64'),
                              shared=shared)
        system_libs = find_system_libraries(['libpthread', 'libm', 'libdl'])
        if shared:
            return libs + system_libs
        else:
            return IntelOneApiStaticLibraryList(libs, system_libs)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('MKLROOT', self.component_path)
