import os

from spack.architecture import Architecture, Target

class Cray(Architecture):
    priority    = 20
    front_end   = 'sandybridge'
    back_end    = 'ivybridge'
    default     = 'ivybridge'

    def __init__(self):
        ''' Since cori doesn't have ivybridge as a front end it's better
            if we use CRAY_CPU_TARGET as the default. This will ensure
            that if we're on a XC-40 or XC-30 then we can detect the target
        '''
        super(Cray, self).__init__('cray')

        # Handle the default here so we can check for a key error
        if 'CRAY_CPU_TARGET' in os.environ:
            default = os.environ['CRAY_CPU_TARGET']

        # Back End compiler needs the proper target module loaded.
        self.add_target(self.back_end, Target(self.front_end,'craype-'+ self.back_end))
        self.add_target(self.default, Target(self.default,'craype-' + self.default))
        # Could switch to use modules and fe targets for front end
        # Currently using compilers by path for front end.
        self.add_target(self.front_end, Target(self.front_end))


    @classmethod
    def detect(self):
        return os.path.exists('/opt/cray/craype')

