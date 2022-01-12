# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import platform
import subprocess
import sys

from spack.error import SpackError
from spack.version import Version

from ._operating_system import OperatingSystem


# FIXME: To get the actual Windows version, we need a python that runs
# natively on Windows, not Cygwin.
def windows_version():
    """temporary workaround to return a Windows version as a Version object
    """
    return Version('10')


class WindowsOs(OperatingSystem):
    """This class represents the Windows operating system.  This will be
    auto detected using the python platform.win32_ver() once we have a
    python setup that runs natively.  The Windows platform will be
    represented using the major version operating system number, e.g.
    10.
    """

    # Find MSVC directories using vswhere
    comp_search_paths = []
    vs_install_paths = []
    root = os.environ.get('ProgramFiles(x86)') or os.environ.get('ProgramFiles')
    if root:
        try:
            extra_args = {}
            if sys.version_info[:3] >= (3, 6, 0):
                extra_args = {'encoding': 'mbcs', 'errors': 'strict'}
            paths = subprocess.check_output([  # type: ignore[call-overload] # novermin
                os.path.join(root, "Microsoft Visual Studio",
                             "Installer", "vswhere.exe"),
                "-prerelease",
                "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                "-property", "installationPath",
                "-products", "*",
            ], **extra_args).strip()
            if (3, 0) <= sys.version_info[:2] <= (3, 5):
                paths = paths.decode()
            vs_install_paths = paths.split('\n')
            msvc_paths = [os.path.join(path, "VC", "Tools", "MSVC")
                          for path in vs_install_paths]
            for p in msvc_paths:
                comp_search_paths.extend(
                    glob.glob(os.path.join(p, '*', 'bin', 'Hostx64', 'x64')))
            if os.getenv("ONEAPI_ROOT"):
                comp_search_paths.extend(glob.glob(os.path.join(
                    str(os.getenv("ONEAPI_ROOT")),
                    'compiler', '*',
                    'windows', 'bin')))
        except (subprocess.CalledProcessError, OSError, UnicodeDecodeError):
            pass
    if comp_search_paths:
        compiler_search_paths = comp_search_paths

    def __init__(self):
        if Version(platform.release()) < Version('10'):
            raise SpackError("Spack is not supported on Windows versions older than 10")
        super(WindowsOs, self).__init__('Windows10', '10')

    def __str__(self):
        return self.name
