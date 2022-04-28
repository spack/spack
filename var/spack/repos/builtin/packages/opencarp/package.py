# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from datetime import datetime

from spack import *


class Opencarp(CMakePackage):
    """The openCARP simulation software,
       an open cardiac electrophysiology simulator for in-silico experiments."""

    homepage = "https://www.opencarp.org"
    git = "https://git.opencarp.org/openCARP/openCARP.git"

    maintainers = ['MarieHouillon']

    version('9.0', commit='c0167599', submodules=False, no_cache=True, preferred=True)
    version('8.2', commit='dbfd16fd', submodules=False, no_cache=True)
    version('8.1', commit='28eb2e97', submodules=False, no_cache=True)
    version('7.0', commit='78da9195', submodules=False, no_cache=True)
    version('master', branch='master', submodules=False, no_cache=True)

    variant('carputils', default=False, description='Installs the carputils framework')
    variant('meshtool', default=False, description='Installs the meshtool software')

    # Patch removing problematic steps in CMake process
    patch('opencarp7.patch', when='@7.0')

    depends_on('git')
    depends_on('petsc')
    depends_on('binutils')
    depends_on('gengetopt')
    depends_on('pkgconfig')
    depends_on('python')
    depends_on('zlib')
    depends_on('perl')

    depends_on('py-carputils')
    depends_on('meshtool')
    # Use specific versions of carputils and meshtool for releases
    for ver in ['9.0', '8.2', '7.0', '8.1']:
        depends_on('py-carputils@oc' + ver, when='@' + ver + ' +carputils')
        depends_on('meshtool@oc' + ver, when='@' + ver + ' +meshtool')

    def cmake_args(self):
        return [
            self.define('DLOPEN', True),
            self.define('SPACK_BUILD', True)
        ]

    @run_after('install')
    def post_install(self):
        # If carputils has been installed, a new settings file
        # with right executable paths is generated
        if '+carputils' in self.spec:
            settings_prefix = os.path.expanduser(join_path('~', '.config', 'carputils'))
            settings_file = join_path(settings_prefix, 'settings.yaml')
            if os.path.exists(settings_file):
                print('Backup the existing settings.yaml...')
                os.rename(settings_file,
                          join_path(
                              settings_prefix,
                              'settings.yaml.'
                              + datetime.today().strftime('%Y-%m-%d-%H:%M:%S')))
            cusettings = Executable('cusettings')
            cusettings(settings_file, '--flavor', 'petsc',
                       '--software-root', self.prefix.bin)
