# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import subprocess
from os import path

from spack import *


releases = {'2021.1.0':
            {'irc_id': '17427', 'build': '2684'}}


class IntelOneapiCompilers(IntelOneApiPackage):
    """Intel oneAPI compilers.

    Contains icc, icpc, icx, icpx, dpcpp, ifort, ifx.

    """

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/dpc-compiler.html'

    version('2021.1.0', sha256='666b1002de3eab4b6f3770c42bcf708743ac74efeba4c05b0834095ef27a11b9', expand=False)

    depends_on('patchelf', type='build')

    def __init__(self, spec):
        self.component_info(
            dir_name='compiler',
            components=('intel.oneapi.lin.dpcpp-cpp-compiler-pro'
                        ':intel.oneapi.lin.ifort-compiler'),
            releases=releases,
            url_name='HPCKit')
        super(IntelOneapiCompilers, self).__init__(spec)

    def install(self, spec, prefix):
        super(IntelOneapiCompilers, self).install(spec, prefix)
        # For quick turnaround debugging, copy instead of install
        # copytree('/opt/intel/oneapi/compiler', path.join(prefix, 'compiler'),
        #          symlinks=True)
        rpath_dirs = ['lib',
                      'lib/x64',
                      'lib/emu',
                      'lib/oclfpga/host/linux64/lib',
                      'lib/oclfpga/linux64/lib',
                      'compiler/lib/intel64_lin',
                      'compiler/lib']
        patch_dirs = ['compiler/lib/intel64_lin',
                      'compiler/lib/intel64',
                      'bin']
        eprefix = path.join(prefix, 'compiler', 'latest', 'linux')
        rpath = ':'.join([path.join(eprefix, c) for c in rpath_dirs])
        for pd in patch_dirs:
            for file in glob.glob(path.join(eprefix, pd, '*')):
                # Try to patch all files, patchelf will do nothing if
                # file should not be patched
                subprocess.call(['patchelf', '--set-rpath', rpath, file])

    def setup_run_environment(self, env):
        env.prepend_path('PATH', join_path(self.prefix,
                         'compiler', 'latest', 'linux', 'bin'))
        env.prepend_path('CPATH', join_path(self.prefix,
                         'compiler', 'latest', 'linux', 'include'))
        env.prepend_path('LIBRARY_PATH', join_path(self.prefix,
                         'compiler', 'latest', 'linux', 'lib'))
        env.prepend_path('LD_LIBRARY_PATH', join_path(self.prefix,
                         'compiler', 'latest', 'linux', 'lib'))
