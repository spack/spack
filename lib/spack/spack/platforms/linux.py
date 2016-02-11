import subprocess
from spack.architecture import Platform, Target

class Linux(Platform):
    priority    = 90
    front_end   = 'x86_64'
    back_end    = 'x86_64'
    default     = 'x86_64'

    def __init__(self):
        super(Linux, self).__init__('linux')
        self.add_target(self.default, Target(self.default, 'PATH'))
        self.add_operating_system()

    @classmethod
    def detect(self):
        platform = subprocess.Popen(['uname', '-a'], stdout = subprocess.PIPE)
        platform, _ = platform.communicate()
        return 'linux' in platform.strip().lower()
