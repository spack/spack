import subprocess
from spack.architecture import Architecture, Target

class Linux(Architecture):
    priority    = 90
    front_end   = 'x86_64'
    back_end    = 'x86_64'
    default     = 'x86_64'

    def __init__(self):
        super(Linux, self).__init__('linux')
        self.add_target(self.default, Target(self.default, 'PATH'))

    @classmethod
    def detect(self):
        arch = subprocess.Popen(['uname', '-a'], stdout = subprocess.PIPE)
        arch, _ = arch.communicate()
        return 'linux' in arch.strip().lower()
