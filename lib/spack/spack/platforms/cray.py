import os

from spack.architecture import Platform, Target

class Cray(Platform):
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
            self.default = os.environ['CRAY_CPU_TARGET']

        # Change the defaults to haswell if we're on an XC40
        if self.default == 'haswell':
            self.front_end = self.default
            self.back_end = self.default

        # Could switch to use modules and fe targets for front end
        # Currently using compilers by path for front end.
        self.add_target(self.front_end, Target(self.front_end, 'PATH'))
        # Back End compiler needs the proper target module loaded.
#        self.add_target(self.back_end, Target(self.front_end, 'MODULES', 'craype-'+ self.back_end))
        self.add_target(self.default, Target(self.default, 'MODULES', 'craype-' + self.default))
        # This is kludgy and the order matters when the targets are all haswell
        # This is because the last one overwrites the others when they have the
        # same name.

    @classmethod
    def detect(self):
        return os.path.exists('/opt/cray/craype')

