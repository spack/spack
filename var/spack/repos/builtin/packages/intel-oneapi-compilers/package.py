# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import platform
import subprocess
from os import path

from spack import *


@IntelOneApiPackage.update_description
class IntelOneapiCompilers(IntelOneApiPackage):
    """Intel oneAPI Compilers. Includes: icc, icpc, ifort, icx, icpx, ifx,
    and dpcpp.

    """

    maintainers = ['rscohn2']

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"

    depends_on('patchelf', type='build')

    if platform.system() == 'Linux':
        version('2022.1.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18717/l_dpcpp-cpp-compiler_p_2022.1.0.137_offline.sh',
                sha256='1027819581ba820470f351abfc2b2658ff2684ed8da9ed0e722a45774a2541d6',
                expand=False)
        resource(name='fortran-installer',
                 url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18703/l_fortran-compiler_p_2022.1.0.134_offline.sh',
                 sha256='583082abe54a657eb933ea4ba3e988eef892985316be13f3e23e18a3c9515020',
                 expand=False,
                 placement='fortran-installer',
                 when='@2022.1.0')
        version('2022.0.2',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18478/l_dpcpp-cpp-compiler_p_2022.0.2.84_offline.sh',
                sha256='ade5bbd203e7226ca096d7bf758dce07857252ec54e83908cac3849e6897b8f3',
                expand=False)
        resource(name='fortran-installer',
                 url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18481/l_fortran-compiler_p_2022.0.2.83_offline.sh',
                 sha256='78532b4118fc3d7afd44e679fc8e7aed1e84efec0d892908d9368e0c7c6b190c',
                 expand=False,
                 placement='fortran-installer',
                 when='@2022.0.2')
        version('2022.0.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18435/l_dpcpp-cpp-compiler_p_2022.0.1.71_offline.sh',
                sha256='c7cddc64c3040eece2dcaf48926ba197bb27e5a46588b1d7b3beddcdc379926a',
                expand=False)
        resource(name='fortran-installer',
                 url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18436/l_fortran-compiler_p_2022.0.1.70_offline.sh',
                 sha256='2cb28a04f93554bfeffd6cad8bd0e7082735f33d73430655dea86df8933f50d1',
                 expand=False,
                 placement='fortran-installer',
                 when='@2022.0.1')
        version('2021.4.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18209/l_dpcpp-cpp-compiler_p_2021.4.0.3201_offline.sh',
                sha256='9206bff1c2fdeb1ca0d5f79def90dcf3e6c7d5711b9b5adecd96a2ba06503828',
                expand=False)
        resource(name='fortran-installer',
                 url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18210/l_fortran-compiler_p_2021.4.0.3224_offline.sh',
                 sha256='de2fcf40e296c2e882e1ddf2c45bb8d25aecfbeff2f75fcd7494068d621eb7e0',
                 expand=False,
                 placement='fortran-installer',
                 when='@2021.4.0')
        version('2021.3.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17928/l_dpcpp-cpp-compiler_p_2021.3.0.3168_offline.sh',
                sha256='f848d81b7cabc76c2841c9757abb2290921efd7b82491d830605f5785600e7a1',
                expand=False)
        resource(name='fortran-installer',
                 url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17959/l_fortran-compiler_p_2021.3.0.3168_offline.sh',
                 sha256='c4553f7e707be8e8e196f625e4e7fbc8eff5474f64ab85fc7146b5ed53ebc87c',
                 expand=False,
                 placement='fortran-installer',
                 when='@2021.3.0')
        version('2021.2.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17749/l_dpcpp-cpp-compiler_p_2021.2.0.118_offline.sh',
                sha256='5d01cbff1a574c3775510cd97ffddd27fdf56d06a6b0c89a826fb23da4336d59',
                expand=False)
        resource(name='fortran-installer',
                 url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17756/l_fortran-compiler_p_2021.2.0.136_offline.sh',
                 sha256='a62e04a80f6d2f05e67cd5acb03fa58857ee22c6bd581ec0651c0ccd5bdec5a1',
                 expand=False,
                 placement='fortran-installer',
                 when='@2021.2.0')
        version('2021.1.2',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17513/l_dpcpp-cpp-compiler_p_2021.1.2.63_offline.sh',
                sha256='68d6cb638091990e578e358131c859f3bbbbfbf975c581fd0b4b4d36476d6f0a',
                expand=False)
        resource(name='fortran-installer',
                 url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17508/l_fortran-compiler_p_2021.1.2.62_offline.sh',
                 sha256='29345145268d08a59fa7eb6e58c7522768466dd98f6d9754540d1a0803596829',
                 expand=False,
                 placement='fortran-installer',
                 when='@2021.1.2')

    @property
    def component_dir(self):
        return 'compiler'

    def _ld_library_path(self):
        dirs = ['lib',
                join_path('lib', 'x64'),
                join_path('lib', 'emu'),
                join_path('lib', 'oclfpga', 'host', 'linux64', 'lib'),
                join_path('lib', 'oclfpga', 'linux64', 'lib'),
                join_path('compiler', 'lib', 'intel64_lin'),
                join_path('compiler', 'lib')]
        for dir in dirs:
            yield join_path(self.component_path, 'linux', dir)

    def install(self, spec, prefix):
        # install cpp
        # Copy instead of install to speed up debugging
        # subprocess.run(f'cp -r /opt/intel/oneapi/compiler {prefix}', shell=True)
        super(IntelOneapiCompilers, self).install(spec, prefix)

        # install fortran
        super(IntelOneapiCompilers, self).install(
            spec,
            prefix,
            installer_path=glob.glob(join_path('fortran-installer', '*'))[0])

        # Some installers have a bug and do not return an error code when failing
        if not path.isfile(join_path(self.component_path, 'linux',
                                     'bin', 'intel64', 'ifort')):
            raise RuntimeError('install failed')

        # set rpath so 'spack compiler add' can check version strings
        # without setting LD_LIBRARY_PATH
        rpath = ':'.join(self._ld_library_path())
        patch_dirs = [join_path('lib'),
                      join_path('compiler', 'lib', 'intel64_lin'),
                      join_path('compiler', 'lib', 'intel64'),
                      'bin']
        for pd in patch_dirs:
            patchables = glob.glob(join_path(self.component_path, 'linux', pd, '*'))
            patchables.append(join_path(self.component_path,
                                        'linux', 'lib', 'icx-lto.so'))
            for file in patchables:
                # Try to patch all files, patchelf will do nothing if
                # file should not be patched
                subprocess.call(['patchelf', '--set-rpath', rpath, file])
