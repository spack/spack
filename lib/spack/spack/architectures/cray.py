import os

from spack.architecture import Architecture

class Cray(Architecture):
    priority    = 20
    front_end   = 'sandybridge' 
    back_end    = 'ivybridge'
    default     = os.environ["CRAY_CPU_TARGET"] 

    def __init__(self):
        super(Cray, self).__init__('cray')

    @classmethod
    def detect(self):
        return os.path.exists('/opt/cray/craype')
    
