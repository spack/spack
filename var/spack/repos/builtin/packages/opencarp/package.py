# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install opencarp
#
# You can edit this file again by typing:
#
#     spack edit opencarp
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os
from datetime import datetime

from spack import *


class Opencarp(CMakePackage):
    """The openCARP simulation software, an open cardiac electrophysiology simulator for in-silico experiments."""

    homepage = "https://www.opencarp.org"
    git = "https://git.opencarp.org/openCARP/openCARP.git"

    # Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['MarieHouillon']

    version('7.0', commit='78da9195', submodules=False, no_cache=True, preferred=True)
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
    depends_on('python@2.7:2.8,3.6:3.8')
    depends_on('zlib')
    depends_on('perl')

    depends_on('py-carputils')
    depends_on('meshtool')
    # Use specific versions of carputils and meshtool for releases
    for ver in ['7.0']:
        depends_on('py-carputils@oc{}'.format(ver), when='@{} +carputils'.format(ver))
        depends_on('meshtool@oc{}'.format(ver), when='@{} +meshtool'.format(ver))

    def cmake_args(self):
        args = [
                '-DDLOPEN:STRING=ON',
                '-DSPACK_BUILD:STRING=ON'
        ]
        return args

    @run_after('install')
    def post_install(self):
        # If carputils is installed, a new settings file with right executable paths is generated
        if '+carputils' in self.spec:
            settings_prefix = os.path.expanduser('~/.config/carputils')
            settings_file = os.path.join(settings_prefix, 'settings.yaml')
            if os.path.exists(settings_file):
                print('Backup the existing settings.yaml...')
                os.rename(settings_file, os.path.join(settings_prefix, 'settings.yaml.{}'.format(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))))
            os.system('cusettings {} --flavor petsc --software-root {}'.format(settings_file, self.prefix.bin))
