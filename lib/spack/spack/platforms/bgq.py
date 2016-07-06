import os
from spack.architecture import Platform, Target

class Bgq(Platform):
    priority    = 30
    front_end   = 'power7'
    back_end    = 'powerpc'
    default     = 'powerpc'

    def __init__(self):
        super(Bgq, self).__init__('bgq')
        self.add_target(Target(self.front_end))
        self.add_target(Target(self.back_end,))

    @classmethod
    def detect(self):
        return os.path.exists('/bgsys')
    
