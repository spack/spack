import subprocess
from spack.architecture import Architecture, Target

class Darwin(Architecture):
    priority    = 89
    front_end   = 'x86_64'
    back_end    = 'x86_64'
    default     = 'x86_64'

    def __init__(self):
        super(Darwin, self).__init__('darwin')
        self.add_target(self.default, Target(self.default, 'PATH'))

    @classmethod
    def detect(self):
        arch = subprocess.Popen(['uname', '-a'], stdout = subprocess.PIPE)
        arch, _ = arch.communicate()
        return 'darwin' in arch.strip().lower()
