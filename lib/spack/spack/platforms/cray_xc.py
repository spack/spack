import os
from spack.architecture import Platform, Target
from spack.operating_systems.linux_distro import LinuxDistro
from spack.operating_systems.cnl import Cnl

class CrayXc(Platform):
    priority    = 20
    front_end   = 'sandybridge'
    back_end    = 'ivybridge'
    default     = 'ivybridge'

    front_os    = "SuSE"
    back_os     = "CNL"
    default_os  = "CNL" 

    def __init__(self):
        ''' Since cori doesn't have ivybridge as a front end it's better
            if we use CRAY_CPU_TARGET as the default. This will ensure
            that if we're on a XC-40 or XC-30 then we can detect the target
        '''
        super(CrayXc, self).__init__('crayxc')

        # Handle the default here so we can check for a key error
        if 'CRAY_CPU_TARGET' in os.environ:
            self.default = os.environ['CRAY_CPU_TARGET']

        # Change the defaults to haswell if we're on an XC40
        if self.default == 'haswell':
            self.front_end = self.default
            self.back_end = self.default

        # Could switch to use modules and fe targets for front end
        # Currently using compilers by path for front end.
        self.add_target('sandybridge', Target('sandybridge'))
        self.add_target('ivybridge', 
                        Target('ivybridge', 'craype-ivybridge'))
        self.add_target('haswell', 
                        Target('haswell','craype-haswell'))         

        self.add_operating_system('SuSE', LinuxDistro())
        self.add_operating_system('CNL', Cnl())

    @classmethod
    def detect(self):
        return os.path.exists('/opt/cray/craype')

