import os
import re
import platform as py_platform
#from subprocess import check_output
import spack.config
from spack.util.executable import which
from spack.architecture import Platform, Target, NoPlatformError
from spack.operating_systems.linux_distro import LinuxDistro
from spack.operating_systems.cnl import Cnl


# Craype- module prefixes that are not valid CPU targets.
NON_TARGETS = ('hugepages', 'network', 'target', 'accel', 'xtpe')


def _target_from_init(name):
    matches = []
    if name != 'front_end':
        pattern = 'craype-(?!{0})(\S*)'.format('|'.join(NON_TARGETS))
        with open('/etc/bash.bashrc.local', 'r') as conf:
            for line in conf:
                if re.search('^[^\#]*module[\s]*(?:add|load)', line):
                     matches.extend(re.findall(pattern, line))
    return matches[0] if matches else None


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

        # Get targets from config or make best guess from environment:
        conf = spack.config.get_config('targets')
        for name in ('front_end', 'back_end'):
            _target = getattr(self, name, None)
            if _target is None:
                _target = os.environ.get('SPACK_' + name.upper())
            if _target is None:
                _target = conf.get(name)
            if _target is None:
                _target = _target_from_init(name)
            setattr(self, name, _target)
            
            if _target is not None:
                self.add_target(name, Target(_target, 'craype-' + _target))
                self.add_target(_target, Target(_target, 'craype-' + _target))

        if self.back_end is not None:
            self.default = self.back_end
            self.add_target('default', Target(self.default, 'craype-' + self.default))
        else:
            raise NoPlatformError()

        front_distro = LinuxDistro()
        back_distro = Cnl()

        self.default_os = str(back_distro)
        self.back_os = self.default_os
        self.front_os = str(front_distro)

        self.add_operating_system(self.back_os, back_distro)
        self.add_operating_system(self.front_os, front_distro)

    @classmethod
    def setup_platform_environment(self, pkg, env):
        """ Change the linker to default dynamic to be more
            similar to linux/standard linker behavior
        """
        env.set('CRAYPE_LINK_TYPE', 'dynamic')
        cray_wrapper_names = join_path(spack.build_env_path, 'cray')
        if os.path.isdir(cray_wrapper_names):
            env.prepend_path('PATH', cray_wrapper_names)
            env.prepend_path('SPACK_ENV_PATHS', cray_wrapper_names)

    @classmethod
    def detect(self):
        return os.environ.get('CRAYPE_VERSION') is not None
