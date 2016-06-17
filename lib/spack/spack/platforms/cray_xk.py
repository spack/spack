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
        ''' Create a Cray XK system platform using CRAY_CPU_TARGET as the
        default. 
        '''
        super(CrayXk, self).__init__('cray_xk')

        # Handle the default here so we can check for a key error
        if 'CRAY_CPU_TARGET' in os.environ:
            self.default = os.environ['CRAY_CPU_TARGET']

        # Could switch to use modules and fe targets for front end
        # Currently using compilers by path for front end.
        self.add_target(Target('istanbul', set(('craype-mc8', 'dynamic-link'))))
        self.add_target(Target('interlagos', 'craype-interlagos'))
        self.add_target(Target('interlagos_dynamic',
                               set(('craype-interlagos', 'dynamic-link'))))

        self.add_operating_system('SuSE11', LinuxDistro())
        self.add_operating_system('CNL10', Cnl())

    @classmethod
    def detect(self):
        return 'cray-xk' in os.environ.get('SPACK_PLATFORM', '')

