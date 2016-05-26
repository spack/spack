import subprocess
from spack.architecture import Platform
from spack.operating_systems.pre_v1

class SpackCompatibility(Platform):
    priority    = 9999

    # We don't use the normal target getters for this platform
    # Instead, targets are added directly when parsing the yaml

    # OS is the spack backwards compatibility os.
    front_os = 'PreVersion1.0'
    back_os = 'PreVersion1.0'
    default_os = 'PreVersion1.0'

    def __init__(self):
        super(SpackCompatibility, self).__init__('spack_compatibility')
        sc_os = spack.operating_systems.pre_v1.PreV1()
        self.add_operating_system(sc_os.name, sc_os)

    @classmethod
    def detect(self):
        return True
