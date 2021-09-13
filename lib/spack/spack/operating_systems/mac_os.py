# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform as py_platform

from spack.util.executable import Executable
from spack.version import Version

from ._operating_system import OperatingSystem


# FIXME: store versions inside OperatingSystem as a Version instead of string
def macos_version():
    """temporary workaround to return a macOS version as a Version object
    """
    return Version(py_platform.mac_ver()[0])


def macos_sdk_path():
    """Return SDK path
    """
    xcrun = Executable('xcrun')
    return xcrun('--show-sdk-path', output=str, error=str).rstrip()


class MacOs(OperatingSystem):
    """This class represents the macOS operating system. This will be
    auto detected using the python platform.mac_ver. The macOS
    platform will be represented using the major version operating
    system name, i.e el capitan, yosemite...etc.
    """

    def __init__(self):
        """Autodetects the mac version from a dictionary.

        If the mac version is too old or too new for Spack to recognize,
        will use a generic "macos" version string until Spack is updated.
        """
        mac_releases = {
            '10.0':  'cheetah',
            '10.1':  'puma',
            '10.2':  'jaguar',
            '10.3':  'panther',
            '10.4':  'tiger',
            '10.5':  'leopard',
            '10.6':  'snowleopard',
            '10.7':  'lion',
            '10.8':  'mountainlion',
            '10.9':  'mavericks',
            '10.10': 'yosemite',
            '10.11': 'elcapitan',
            '10.12': 'sierra',
            '10.13': 'highsierra',
            '10.14': 'mojave',
            '10.15': 'catalina',
            '10.16': 'bigsur',
            '11': 'bigsur',
            '12': 'monterey',
        }

        # Big Sur versions go 11.0, 11.0.1, 11.1 (vs. prior versions that
        # only used the minor component)
        part = 1 if macos_version() >= Version('11') else 2

        mac_ver = str(macos_version().up_to(part))
        name = mac_releases.get(mac_ver, "macos")
        super(MacOs, self).__init__(name, mac_ver)

    def __str__(self):
        return self.name
