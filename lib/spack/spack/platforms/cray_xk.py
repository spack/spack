import os
from spack.architecture import Platform, Target
from spack.operating_systems.linux_distro import LinuxDistro
from spack.operating_systems.cnl import Cnl

class CrayXk(Platform):
    priority    = 20
    front_end   = 'istanbul'
    back_end    = 'interlagos'
    default     = 'interlagos'

    front_os    = "SuSE11"
    back_os     = "CNL10"
    default_os  = "CNL10" 

    def __init__(self):
        ''' Since cori doesn't have ivybridge as a front end it's better
            if we use CRAY_CPU_TARGET as the default. This will ensure
            that if we're on a XC-40 or XC-30 then we can detect the target
        '''
        super(CrayXk, self).__init__('cray_xk')

        # Handle the default here so we can check for a key error
        if 'CRAY_CPU_TARGET' in os.environ:
            self.default = os.environ['CRAY_CPU_TARGET']

        # Could switch to use modules and fe targets for front end
        # Currently using compilers by path for front end.
        self.add_target('istanbul', Target('istanbul', 'craype-mc8'))
        self.add_target('interlagos', 
                        Target('interlagos', 'craype-interlagos'))

        self.add_operating_system('SuSE11', LinuxDistro())
        self.add_operating_system('CNL10', Cnl())

    @classmethod
    def detect(self):
        return 'cray-xk' in os.environ.get('SPACK_PLATFORM', '')

