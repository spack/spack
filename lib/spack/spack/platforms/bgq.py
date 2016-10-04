import os
import platform
from spack.architecture import Platform, Target
from spack.operating_systems.linux_distro import LinuxDistro
from spack.operating_systems.bgq import BgqDistro

class Bgq(Platform):
    priority    = 30
    front_end   = 'power7'
    back_end    = 'powerpc'
    default     = 'powerpc'

    def __init__(self):
        super(Bgq, self).__init__('bgq')

        for name in ('front_end', 'back_end'):
            _target = getattr(self, name, None)

            if _target is not None:
                self.add_target(name, Target(_target))

        self.default = platform.machine()

        if self.default not in self.targets:
            self.add_target(self.default, Target(self.default))

        front_distro = LinuxDistro()
        back_distro = BgqDistro()

        self.default_os = str(back_distro)
        self.back_os = self.default_os
        self.front_os = str(front_distro)

        self.add_operating_system(self.back_os, back_distro)
        self.add_operating_system(self.front_os, front_distro)

    @classmethod
    def detect(self):
        return os.path.exists('/bgsys')
