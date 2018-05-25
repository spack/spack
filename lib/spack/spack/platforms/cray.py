##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import re
import llnl.util.tty as tty
from spack.paths import build_env_path
from spack.util.executable import which
from spack.architecture import Platform, Target, NoPlatformError
from spack.operating_systems.cray_frontend import CrayFrontend
from spack.operating_systems.cnl import Cnl
from spack.util.module_cmd import get_module_cmd, unload_module


def _get_modules_in_modulecmd_output(output):
    '''Return list of valid modules parsed from modulecmd output string.'''
    return [i for i in output.splitlines()
            if len(i.split()) == 1]


def _fill_craype_targets_from_modules(targets, modules):
    '''Extend CrayPE CPU targets list with those found in list of modules.'''
    # Craype- module prefixes that are not valid CPU targets.
    non_targets = ('hugepages', 'network', 'target', 'accel', 'xtpe')
    pattern = r'craype-(?!{0})(\S*)'.format('|'.join(non_targets))
    for mod in modules:
        if 'craype-' in mod:
            targets.extend(re.findall(pattern, mod))


class Cray(Platform):
    priority = 10

    def __init__(self):
        ''' Create a Cray system platform.

        Target names should use craype target names but not include the
        'craype-' prefix. Uses first viable target from:
          self
          envars [SPACK_FRONT_END, SPACK_BACK_END]
          configuration file "targets.yaml" with keys 'front_end', 'back_end'
          scanning /etc/bash/bashrc.local for back_end only
        '''
        super(Cray, self).__init__('cray')

        # Make all craype targets available.
        for target in self._avail_targets():
            name = target.replace('-', '_')
            self.add_target(name, Target(name, 'craype-%s' % target))

        # Get aliased targets from config or best guess from environment:
        for name in ('front_end', 'back_end'):
            _target = getattr(self, name, None)
            if _target is None:
                _target = os.environ.get('SPACK_' + name.upper())
            if _target is None and name == 'back_end':
                _target = self._default_target_from_env()
            if _target is not None:
                safe_name = _target.replace('-', '_')
                setattr(self, name, safe_name)
                self.add_target(name, self.targets[safe_name])

        if self.back_end is not None:
            self.default = self.back_end
            self.add_target('default', self.targets[self.back_end])
        else:
            raise NoPlatformError()

        front_distro = CrayFrontend()
        back_distro = Cnl()

        self.default_os = str(back_distro)
        self.back_os = self.default_os
        self.front_os = str(front_distro)

        self.add_operating_system(self.back_os, back_distro)
        self.add_operating_system(self.front_os, front_distro)

    @classmethod
    def setup_platform_environment(cls, pkg, env):
        """ Change the linker to default dynamic to be more
            similar to linux/standard linker behavior
        """
        # Unload these modules to prevent any silent linking or unnecessary
        # I/O profiling in the case of darshan.
        modules_to_unload = ["cray-mpich", "darshan", "cray-libsci"]
        for module in modules_to_unload:
            unload_module(module)

        env.set('CRAYPE_LINK_TYPE', 'dynamic')
        cray_wrapper_names = os.path.join(build_env_path, 'cray')

        if os.path.isdir(cray_wrapper_names):
            env.prepend_path('PATH', cray_wrapper_names)
            env.prepend_path('SPACK_ENV_PATH', cray_wrapper_names)

        # Makes spack installed pkg-config work on Crays
        env.append_path("PKG_CONFIG_PATH", "/usr/lib64/pkgconfig")
        env.append_path("PKG_CONFIG_PATH", "/usr/local/lib64/pkgconfig")

    @classmethod
    def detect(cls):
        return os.environ.get('CRAYPE_VERSION') is not None

    def _default_target_from_env(self):
        '''Set and return the default CrayPE target loaded in a clean login
        session.

        A bash subshell is launched with a wiped environment and the list of
        loaded modules is parsed for the first acceptable CrayPE target.
        '''
        # Based on the incantation:
        # echo "$(env - USER=$USER /bin/bash -l -c 'module list -lt')"
        if getattr(self, 'default', None) is None:
            env = which('env')
            env.add_default_arg('-')
            # CAUTION - $USER is generally needed in the sub-environment.
            # There may be other variables needed for general success.
            output = env('USER=%s' % os.environ['USER'],
                         'HOME=%s' % os.environ['HOME'],
                         '/bin/bash', '--noprofile', '--norc', '-c',
                         '. /etc/profile; module list -lt',
                         output=str, error=str)
            self._defmods = _get_modules_in_modulecmd_output(output)
            targets = []
            _fill_craype_targets_from_modules(targets, self._defmods)
            self.default = targets[0] if targets else None
            tty.debug("Found default modules:",
                      *["     %s" % mod for mod in self._defmods])
        return self.default

    def _avail_targets(self):
        '''Return a list of available CrayPE CPU targets.'''
        if getattr(self, '_craype_targets', None) is None:
            module = get_module_cmd()
            output = module('avail', '-t', 'craype-', output=str, error=str)
            craype_modules = _get_modules_in_modulecmd_output(output)
            self._craype_targets = targets = []
            _fill_craype_targets_from_modules(targets, craype_modules)
        return self._craype_targets
