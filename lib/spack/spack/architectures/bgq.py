import os

from spack.architecture import Architecture, Target

class Bgq(Architecture):
    priority    = 30
    front_end   = 'power7'
    back_end    = 'powerpc'
    default     = 'powerpc'

    def __init__(self):
        super(Bgq, self).__init__('cray')
        self.add_target('power7', Target('power7'))
        self.add_target('powerpc', Target('powerpc'))

    @classmethod
    def detect(self):
        return os.path.exists('/bgsys')
    
