# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import subprocess
from os import path

from spack import *

cpp_releases = {
    '2021.1.2': {'irc_id': '17513',
                 'build': '63',
                 'sha256': '68d6cb638091990e578e358131c859f3bbbbfbf975c581fd0b4b4d36476d6f0a'}
}

fortran_releases = {
    '2021.1.2': {'irc_id': '17508',
                 'build': '62',
                 'sha256': '29345145268d08a59fa7eb6e58c7522768466dd98f6d9754540d1a0803596829'}
}


class IntelOneapiCompilers(IntelOneApiPackage):
    """Intel OneAPI compilers

    Provides Classic and Beta compilers for: Fortran, C, C++"""

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"

    depends_on('patchelf', type='build')

    for v in cpp_releases:
        cpp_release = cpp_releases[v]
        fortran_release = fortran_releases[v]
        version(v, cpp_release['sha256'], expand=False)
        # Download matching fortran standalone for this cpp
        resource(name='fortran-installer',
                 url=IntelOneApiPackage.get_url('fortran-compiler', v, fortran_release),
                 sha256=fortran_release['sha256'],
                 expand=False,
                 placement='fortran-installer',
                 when='@' + v)

    def __init__(self, spec):
        self.component_info(
            dir_name='compiler',
            releases=cpp_releases,
            url_name='dpcpp-cpp-compiler')
        super(IntelOneapiCompilers, self).__init__(spec)

    def _join_prefix(self, p):
        return path.join(self.prefix, 'compiler/latest/linux', p)

    def _ld_library_path(self):
        dirs = ['lib',
                'lib/x64',
                'lib/emu',
                'lib/oclfpga/host/linux64/lib',
                'lib/oclfpga/linux64/lib',
                'compiler/lib/intel64_lin',
                'compiler/lib']
        for dir in dirs:
            yield self._join_prefix(dir)

    def install(self, spec, prefix):
        # install cpp
        # Copy instead of install to speed up debugging
        # subprocess.run(f'cp -r /opt/intel/oneapi/compiler {prefix}', shell=True)
        super(IntelOneapiCompilers, self).install(spec, prefix)

        # install fortran in same prefix
        self.install_from_releases(spec, prefix, 'fortran-installer',
                                   'fortran-compiler', fortran_releases)

        # set rpath so 'spack compiler add' can check version strings
        # without setting LD_LIBRARY_PATH
        rpath = ':'.join(self._ld_library_path())
        patch_dirs = ['compiler/lib/intel64_lin',
                      'compiler/lib/intel64',
                      'bin']
        for pd in patch_dirs:
            patchables = glob.glob(self._join_prefix(path.join(pd, '*')))
            patchables.append(self._join_prefix('lib/icx-lto.so'))
            for file in patchables:
                # Try to patch all files, patchelf will do nothing if
                # file should not be patched
                subprocess.call(['patchelf', '--set-rpath', rpath, file])
