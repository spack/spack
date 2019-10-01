# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import platform
import llnl.util.cpu as cpu
import llnl.util.tty as tty
from spack.paths import build_env_path
from spack.util.executable import Executable
from spack.architecture import Platform, Target, NoPlatformError
from spack.operating_systems.cray_frontend import CrayFrontend
from spack.operating_systems.cray_backend import CrayBackend
from spack.util.module_cmd import module


def _get_modules_in_modulecmd_output(output):
    '''Return list of valid modules parsed from modulecmd output string.'''
    return [i for i in re.split(r'  |\n', output)
            if len(i.split()) == 1]


def _fill_craype_target_names_from_modules(targets, modules):
    '''Extend CrayPE CPU targets list with those found in list of modules.'''
    # Craype- module prefixes that are not valid CPU targets.
    non_targets = (
        'hugepages', 'network', 'target', 'accel', 'xtpe', 'dl-plugin')
    pattern = r'craype-(?!{0})(\S*)'.format('|'.join(non_targets))
    for mod in modules:
        if 'craype-' in mod:
            targets.extend(re.findall(pattern, mod))


_craype_name_to_target_name = {
    'x86_cascadelake': 'cascadelake',
    'x86_naples': 'zen',
    'x86_skylake': 'skylake-avx512'
}


def _target_name_from_craype_target_name(craype_name):
    name = craype_name.replace('-', '_')
    return _craype_name_to_target_name.get(name, name)


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
            name = _target_name_from_craype_target_name(target)
            self.add_target(name, Target(name, 'craype-%s' % target))

        self.back_end = os.environ.get('SPACK_BACK_END',
                                       self._default_target_from_env())
        self.default = self.back_end
        if self.back_end not in self.targets:
            # We didn't find a target module for the backend
            raise NoPlatformError()

        # Setup frontend targets
        for name in cpu.targets:
            if name not in self.targets:
                self.add_target(name, Target(name))
        self.front_end = os.environ.get('SPACK_FRONT_END', cpu.host().name)
        if self.front_end not in self.targets:
            self.add_target(self.front_end, Target(self.front_end))

        front_distro = CrayFrontend()
        back_distro = CrayBackend()

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
        modules_to_unload = ["cray-mpich", "darshan", "cray-libsci", "altd"]
        for mod in modules_to_unload:
            module('unload', mod)

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
        return 'CRAYPE_VERSION' in os.environ or os.path.exists('/opt/cray/pe')

    def _default_target_from_env(self):
        '''Set and return the default CrayPE target loaded in a clean login
        session.

        A bash subshell is launched with a wiped environment and the list of
        loaded modules is parsed for the first acceptable CrayPE target.
        '''
        # env -i /bin/bash -lc echo $CRAY_CPU_TARGET 2> /dev/null
        if getattr(self, 'default', None) is None:
            bash = Executable('/bin/bash')
            output = bash(
                '--norc', '--noprofile', '-lc', 'echo $CRAY_CPU_TARGET',
                env={'TERM': os.environ.get('TERM', '')},
                output=str, error=os.devnull
            )
            default_from_module = ''.join(output.split())  # rm all whitespace
            if default_from_module:
                tty.debug("Found default module:%s" % default_from_module)
                return default_from_module
            else:
                front_end = cpu.host().name
                if front_end in list(
                        map(lambda x: _target_name_from_craype_target_name(x),
                            self._avail_targets())
                ):
                    tty.debug("default to front-end architecture")
                    return cpu.host().name
                else:
                    return platform.machine()

    def _avail_targets(self):
        '''Return a list of available CrayPE CPU targets.'''
        if getattr(self, '_craype_targets', None) is None:
            output = module('avail', '-t', 'craype-')
            craype_modules = _get_modules_in_modulecmd_output(output)
            self._craype_targets = targets = []
            _fill_craype_target_names_from_modules(targets, craype_modules)
        return self._craype_targets
