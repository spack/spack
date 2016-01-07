import os

from spack.architecture import Platform, Target

class Bgq(Platform):
    priority    = 30
    front_end   = 'power7'
    back_end    = 'powerpc'
    default     = 'powerpc'

    def __init__(self):
        super(Bgq, self).__init__('cray')
        self.add_target(self.front_end, Target(self.front_end, 'PATH'))
        self.add_target(self.back_end, Target(self.back_end, 'PATH'))

    @classmethod
    def detect(self):
        return os.path.exists('/bgsys')
    
