import os
import platform

from version import Version
from utils import memoized

instances = {}
macos_versions = [
    ('10.8', 'mountain_lion'),
    ('10.7', 'lion'),
    ('10.6', 'snow_leopard'),
    ('10.5', 'leopard')]


class SysType(object):
    def __init__(self, arch_string):
        self.arch_string = arch_string

    def __repr__(self):
        return self.arch_string

    def __str__(self):
        return self.__repr__()

@memoized
def sys_type():
    stype = os.environ.get('SYS_TYPE')
    if stype:
        return SysType(stype)
    elif platform.mac_ver()[0]:
        version = Version(platform.mac_ver()[0])
        for mac_ver, name in macos_versions:
            if version >= Version(mac_ver):
                return SysType(name)
