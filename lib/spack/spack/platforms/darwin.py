import subprocess
from spack.architecture import Platform, Target
from spack.operating_system.mac_osx import MacOSX

class Darwin(Platform):
    priority    = 89
    front_end   = 'x86_64'
    back_end    = 'x86_64'
    default     = 'x86_64'

    def __init__(self):
        super(Darwin, self).__init__('darwin')
        self.add_target(self.default, Target(self.default, 'PATH'))
        mac_os = MacOSX()
        self.default_os = mac_os.name
        self.add_operating_system(mac_os.name, mac_os)

    @classmethod
    def detect(self):
        platform = subprocess.Popen(['uname', '-a'], stdout = subprocess.PIPE)
        platform, _ = platform.communicate()
        return 'darwin' in platform.strip().lower()
