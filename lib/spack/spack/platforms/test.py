import subprocess
from spack.architecture import Platform, Target
from spack.operating_systems.linux_distro import LinuxDistro
from spack.operating_systems.cnl import Cnl


class Test(Platform):
    priority    = 1000000
    front_end   = 'x86_32'
    back_end    = 'x86_64'
    default     = 'x86_64'
    
    back_os = 'CNL10'
    default_os = 'CNL10'

    def __init__(self):
        super(Test, self).__init__('test')
        self.add_target(Target(self.default))
        self.add_target(Target(self.front_end))

        self.add_operating_system(self.default_os, Cnl())
        linux_dist = LinuxDistro()
        self.front_os = linux_dist.name
        self.add_operating_system(self.front_os, linux_dist)

    @classmethod
    def detect(self):
        return True
