import os
import platform as py_platform

import spack
import error as serr
from version import Version
from utils import memoized


class InvalidSysTypeError(serr.SpackError):
    def __init__(self, sys_type):
        super(InvalidSysTypeError, self).__init__(
            "Invalid sys_type value for Spack: " + sys_type)


class NoSysTypeError(serr.SpackError):
    def __init__(self):
        super(NoSysTypeError, self).__init__(
            "Could not determine sys_type for this machine.")


def get_sys_type_from_spack_globals():
    """Return the SYS_TYPE from spack globals, or None if it isn't set."""
    if not hasattr(spack, "sys_type"):
        return None
    elif hasattr(spack.sys_type, "__call__"):
        return spack.sys_type()
    else:
        return spack.sys_type


def get_sys_type_from_environment():
    """Return $SYS_TYPE or None if it's not defined."""
    return os.environ.get('SYS_TYPE')


def get_mac_sys_type():
    """Return a Mac OS SYS_TYPE or None if this isn't a mac."""
    mac_ver = py_platform.mac_ver()[0]
    if not mac_ver:
        return None

    return "macosx_{}_{}".format(
        Version(mac_ver).up_to(2), py_platform.machine())


@memoized
def sys_type():
    """Returns a SysType for the current machine."""
    methods = [get_sys_type_from_spack_globals,
               get_sys_type_from_environment,
               get_mac_sys_type]

    # search for a method that doesn't return None
    sys_type = None
    for method in methods:
        sys_type = method()
        if sys_type: break

    # Couldn't determine the sys_type for this machine.
    if sys_type == None:
        raise NoSysTypeError()

    if not type(sys_type) == str:
        raise InvalidSysTypeError(sys_type)

    return sys_type
