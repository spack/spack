import os

from spack.architecture import Architecture

class Cray(Architecture):
    priority    = 20
    front_end   = 'sandybridge' 
    back_end    = 'ivybridge'
    default     = os.environ["CRAY_CPU_TARGET"] 

    def __init__(self):
        super(Cray, self).__init__('cray')
        # Back End compiler needs the proper target module loaded.
        self.add_target('ivybridge','craype-ivybridge')
        # Could switch to use modules and fe targets for front end
        # Currently using compilers by path for front end.
        self.add_target('sandybridge')

    @classmethod
    def detect(self):
        return os.path.exists('/opt/cray/craype')
    
