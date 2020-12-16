# Copyright 2020
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform as py_platform

from spack.architecture import OperatingSystem
from spack.version import Version
from spack.util.executable import Executable

# FIXME: To get the actual Windows version, we need a python that runs
# natively on Windows, not Cygwin.
def windows_version():
    """temporary workaround to return a Windows version as a Version object
    """
    return Version('10')

class WindowsOs(OperatingSystem):
    """This class represents the Windows operating system.  This will be
    auto detected using the python platform.win32_ver() once we have a
    python setup that runs natively.  The Windows platform will be represented
    using the major version operating system number, e.g. 10.
    """

    def __init__(self):
        super(WindowsOs, self).__init__('Windows10', '10')

    def __str__(self):
        return self.name
