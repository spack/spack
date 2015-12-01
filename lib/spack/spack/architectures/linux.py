import subprocess
from spack.architecture import Architecture, Target

class Linux(Architecture):
    priority    = 60
    front_end   = 'linux'
    back_end    = 'linux'
    default     = 'linux'

    def __init__(self):
        super(Linux, self).__init__('linux')
        self.add_target(self.default, Target(self.default))

    @classmethod
    def detect(self):
        arch = subprocess.Popen(['uname', '-i'], stdout = subprocess.PIPE)
        arch, _ = arch.communicate()
        return 'x86_64' in arch.strip()
