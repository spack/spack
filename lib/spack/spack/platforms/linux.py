import subprocess
from spack.architecture import Platform, Target
from spack.operating_systems.linux_distro import LinuxDistro

class Linux(Platform):
    priority    = 90
    front_end   = 'x86_64'
    back_end    = 'x86_64'
    default     = 'x86_64'

    def __init__(self):
        super(Linux, self).__init__('linux')
        self.add_target(self.default, Target(self.default))
        linux_dist = LinuxDistro()
        self.default_os = str(linux_dist)
        self.front_os = self.default_os
        self.back_os = self.default._os
        self.add_operating_system(str(linux_dist), linux_dist)

    @classmethod
    def detect(self):
        platform = subprocess.Popen(['uname', '-a'], stdout = subprocess.PIPE)
        platform, _ = platform.communicate()
        return 'linux' in platform.strip().lower()
